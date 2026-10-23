import json, os, random
import pandas as pd
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "Dungeon_data.json"
SAVE_FILE = Path(__file__).resolve().parent / "dungeon_save.json"
ROOM_LOG_FILE = Path(__file__).resolve().parent / "room_log.csv"
STATS_FILE = Path(__file__).resolve().parent / "dungeon_stats.csv"
EVENT_LOG_FILE = Path(__file__).resolve().parent / "event_log.csv"

ROOM_TYPES = ["combat", "chest", "trap", "rest", "quiet"]
ROOM_COLUMNS = ["room_number","room_type","encounter","outcome","damage_taken",
                "gold_found","potions_found","health_start","health_end",
                "health_restored","potions_used"]
EVENT_COLUMNS = ["step","room_number","room_type","phase","event","encounter",
                 "health_before","health_after","max_health","health_change",
                 "damage_taken","health_restored","potions_used",
                 "potions_remaining","gold_total"]
STATS_COLUMNS = ["room_type","room_count","room_percent","gold_found","damage_taken"]

D = {}
P = {}
HISTORY = []
EVENTS = []
STATUS = "active"


def load_data():
    global D
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            D = json.load(f)
        required = ["settings","player_start","rooms","enemies","elite_enemies",
                    "bosses","chests","traps","weapons","potions","perks"]
        if any(x not in D for x in required):
            raise ValueError("missing required section")
        if len(D["enemies"]) < 5 or len(D["chests"]) < 4 or len(D["traps"]) < 3:
            raise ValueError("not enough enemies, chests, or traps")
        if len(D["rooms"]) < 5 or not all(x in D["rooms"] for x in ROOM_TYPES):
            raise ValueError("all five room types and five descriptions are required")
        s = D["settings"]
        ps = D["player_start"]
        if s["potion_heal"] <= 0 or ps["max_health"] <= 0:
            raise ValueError("health/healing settings must be positive")
    except Exception as e:
        raise SystemExit(f"Could not load {DATA_FILE}: {e}")


def new_player():
    global P, HISTORY, EVENTS, STATUS
    name = input("Enter your name: ").strip()
    while not name:
        print("Name cannot be blank.")
        name = input("Enter your name: ").strip()
    ps = D["player_start"]
    P = {
        "name": name, "health": ps["max_health"], "max_health": ps["max_health"],
        "attack_min": ps["attack_min"], "attack_max": ps["attack_max"],
        "starting_gold": ps["starting_gold"], "gold": ps["starting_gold"],
        "potions": ps["potions"], "room": 0, "equipped_weapon": ps["weapon"],
        "weapons": {w["id"]: w.copy() for w in D["weapons"][:1]},
        "perks": [], "effects": {"strength": 0, "speed": 0, "toughness": 0}
    }
    HISTORY, EVENTS, STATUS = [], [], "active"
    event("start", 0, "none", "start", P["health"], P["health"])


def event(name, room, room_type, phase, before, after, damage=0,
          restored=0, used=0, encounter="none", gold_before=None):
    EVENTS.append({
        "step": len(EVENTS), "room_number": room, "room_type": room_type,
        "phase": phase, "event": name, "encounter": encounter,
        "health_before": before, "health_after": after,
        "max_health": P["max_health"], "health_change": after-before,
        "damage_taken": damage, "health_restored": restored,
        "potions_used": used, "potions_remaining": P["potions"],
        "gold_total": P["gold"]
    })


def damage(amount):
    before = P["health"]
    actual = min(max(0, amount), before)
    P["health"] -= actual
    if P["health"] < 0:
        P["health"] = 0
    return actual, before, P["health"]


def heal(amount):
    before = P["health"]
    actual = min(max(0, amount), P["max_health"] - before)
    P["health"] += actual
    return actual, before, P["health"]


def weapon():
    return next((w for w in P["weapons"].values()
                  if w["id"] == P["equipped_weapon"]), None)


def player_damage():
    w = weapon()
    bonus = sum(D["perks"][i]["damage_bonus"] for i in [] if False)
    bonus += D["settings"]["strength_bonus"] if P["effects"]["strength"] else 0
    low, high = P["attack_min"], P["attack_max"]
    if w:
        low += w["damage"][0]
        high += w["damage"][1]
    return random.randint(low, high) + bonus

def scale_enemy(e):
    level = (P["room"] - 1) // 5
    h = e["health"] + level * D["settings"]["health_increase"]
    a = [e["attack"][0] + level * D["settings"]["attack_increase"],
         e["attack"][1] + level * D["settings"]["attack_increase"]]
    return {"name": e["name"], "health": h, "max_health": h,
            "attack": a, "gold": e["gold"], "kind": e.get("kind", "normal")}


def make_room():
    typ = random.choice(ROOM_TYPES)
    r = {"type": typ, "description": random.choice(D["rooms"][typ])}
    if typ == "combat":
        pool = D["enemies"][:]
        # Elites and bosses become possible without creating extra room types.
        if P["room"] >= 5 and random.random() < D["settings"]["elite_chance"]:
            pool = D["elite_enemies"]
        if P["room"] >= 10 and random.random() < D["settings"]["boss_chance"]:
            pool = D["bosses"]
        r["enemy"] = scale_enemy(random.choice(pool))
    elif typ == "chest":
        r["chest"] = random.choice(D["chests"])
    elif typ == "trap":
        r["trap"] = random.choice(D["traps"])
    return r


def room_record(room, encounter, outcome, start, damage_taken, gold_found,
                potions_found, restored, potions_used):
    end = P["health"]
    # Keep the required equation true even if a future rule is changed.
    if start - damage_taken + restored != end:
        restored = end - start + damage_taken
    HISTORY.append({
        "room_number": P["room"], "room_type": room, "encounter": encounter,
        "outcome": outcome, "damage_taken": damage_taken,
        "gold_found": gold_found, "potions_found": potions_found,
        "health_start": start, "health_end": end,
        "health_restored": restored, "potions_used": potions_used
    })


def use_potion(combat=False, enemy_name="none"):
    if P["potions"] <= 0:
        print("You have no potions.")
        return False, 0
    if P["health"] >= P["max_health"]:
        print("You are already at full health.")
        return False, 0

    # Let the player choose which potion to use.
    potions = D["potions"]
    print("\\nAvailable potions:")
    for index, potion in enumerate(potions, start=1):
        effect = potion.get("effect", "unknown")
        value = potion.get("value", "")
        details = f" - {effect}"
        if value != "":
            details += f" ({value})"
        print(f"{index}. {potion['name']}{details}")
    print("0. Cancel")

    while True:
        choice = input("Choose a potion: ").strip()
        if choice == "0":
            print("Potion use cancelled.")
            return False, 0
        if choice.isdigit() and 1 <= int(choice) <= len(potions):
            potion = potions[int(choice) - 1]
            break
        print(f"Enter a number from 1 to {len(potions)}, or 0 to cancel.")

    if potion["effect"] == "heal":
        amount = potion["value"]
        restored, before, after = heal(amount)
    elif potion["effect"] == "strength":
        restored, before, after = 0, P["health"], P["health"]
        P["effects"]["strength"] = 1
        print("Strength increased.")
    elif potion["effect"] == "speed":
        restored, before, after = 0, P["health"], P["health"]
        P["effects"]["speed"] = 1
        print("Speed increased; dodge chance is now higher.")
    else:
        restored, before, after = 0, P["health"], P["health"]
        print(f"No effect is configured for {potion['name']}.")

    P["potions"] -= 1
    event("potion", P["room"], "combat" if combat else "between",
          "in_room" if combat else "between_rooms", before, after,
          restored=restored, used=1, encounter=enemy_name)
    print(f"Used {potion['name']}.")
    if restored:
        print(f"Healed {restored} HP.")
    return True, restored


def enemy_attack(e):
    if P["effects"]["speed"] and random.random() < D["settings"]["dodge_chance"]:
        event("dodge", P["room"], "combat", "in_room", P["health"], P["health"],
              encounter=e["name"])
        print("You dodged the attack!")
        return 0
    raw = random.randint(*e["attack"])
    if P["effects"]["toughness"]:
        raw = max(0, raw - D["settings"]["toughness_reduction"])
    actual, before, after = damage(raw)
    event("enemy_attack", P["room"], "combat", "in_room", before, after,
          damage=actual, encounter=e["name"])
    print(f"{e['name']} hits you for {actual}.")
    return actual

def combat(r):
    e = r["enemy"]
    start, taken, restored, used, gold_found = P["health"], 0, 0, 0, 0
    print(f"\n{r['description']}\nA {e['kind']} {e['name']} appears!")
    while e["health"] > 0 and P["health"] > 0:
        print(f"\nYou: {P['health']}/{P['max_health']} HP | "
              f"{e['name']}: {e['health']}/{e['max_health']} HP")
        choice = input("[A]ttack [P]otion [F]lee: ").strip().lower()
        if choice in ("a", "attack"):
            dmg = player_damage()
            e["health"] = max(0, e["health"] - dmg)
            event("player_attack", P["room"], "combat", "in_room",
                  P["health"], P["health"], encounter=e["name"])
            if e["health"] <= 0:
                gold_found = random.randint(*e["gold"])
                P["gold"] += gold_found
                print(f"You defeated {e['name']} and found {gold_found} gold.")
                outcome = "defeated"
                break
            taken += enemy_attack(e)
        elif choice in ("p", "potion"):
            ok, h = use_potion(True, e["name"])
            if ok:
                used += 1
                restored += h
                taken += enemy_attack(e)
        elif choice in ("f", "flee"):
            before = P["health"]
            success = random.random() < D["settings"]["flee_chance"]
            event("flee_attempt", P["room"], "combat", "in_room",
                  before, before, encounter=e["name"])
            if success:
                print("You escaped!")
                outcome = "fled"
                break
            print("You failed to escape!")
            taken += enemy_attack(e)
        else:
            print("Invalid choice. No turn is used.")
    else:
        outcome = "died"
    if P["health"] <= 0:
        outcome = "died"
    room_record("combat", e["name"], outcome, start, taken, gold_found,
                0, restored, used)
    return P["health"] > 0


def chest(r):
    c = r["chest"]
    start = P["health"]
    print(f"\n{r['description']}\nYou find {c['name']}.")
    while True:
        x = input("[O]pen or [L]eave: ").strip().lower()
        if x in ("o", "open"):
            gold = random.randint(*c["gold"])
            found_potions = random.randint(*c["potions"])
            P["gold"] += gold
            P["potions"] += found_potions
            event("chest_opened", P["room"], "chest", "in_room",
                  P["health"], P["health"], encounter=c["name"])
            print(f"You found {gold} gold and {found_potions} potion(s).")
            room_record("chest", c["name"], "opened", start, 0, gold,
                        found_potions, 0, 0)
            return True
        if x in ("l", "leave"):
            event("chest_left", P["room"], "chest", "in_room",
                  P["health"], P["health"], encounter=c["name"])
            room_record("chest", c["name"], "skipped", start, 0, 0, 0, 0, 0)
            return True
        print("Invalid choice.")


def trap(r):
    t = r["trap"]
    start = P["health"]
    raw = random.randint(*t["damage"])
    actual, before, after = damage(raw)
    event("trap", P["room"], "trap", "in_room", before, after,
          damage=actual, encounter=t["name"])
    print(f"\n{r['description']}\nThe {t['name']} deals {actual} damage!")
    room_record("trap", t["name"], "triggered", start, actual, 0, 0, 0, 0)
    return P["health"] > 0


def rest(r):
    start = P["health"]
    amount = random.randint(*D["settings"]["rest_heal"])
    actual, before, after = heal(amount)
    event("rest", P["room"], "rest", "in_room", before, after,
          restored=actual, encounter="rest")
    print(f"\n{r['description']}\nYou rest and recover {actual} HP.")
    room_record("rest", "rest", "rested", start, 0, 0, 0, actual, 0)
    return True

def quiet(r):
    print(f"\n{r['description']}")
    event("quiet", P["room"], "quiet", "in_room",
          P["health"], P["health"], encounter="quiet")
    room_record("quiet", "none", "passed", P["health"], 0, 0, 0, 0, 0)
    return True


def explore():
    while True:
        direction = input("Choose [L]eft, [R]ight, or [F]orward: ").strip().lower()
        if direction in ("l", "left", "r", "right", "f", "forward"):
            break
        print("Invalid direction.")
    P["room"] += 1
    r = make_room()
    event("room_entry", P["room"], r["type"], "in_room",
          P["health"], P["health"], encounter=r.get("description", ""))
    if r["type"] == "combat":
        alive = combat(r)
    elif r["type"] == "chest":
        alive = chest(r)
    elif r["type"] == "trap":
        alive = trap(r)
    elif r["type"] == "rest":
        alive = rest(r)
    else:
        alive = quiet(r)
    if not alive:
        finish("dead")


def stats():
    w = weapon()
    print(f"\n{P['name']} | Room {P['room']} | HP {P['health']}/{P['max_health']}")
    print(f"Attack: {P['attack_min']}-{P['attack_max']} | Gold: {P['gold']} | Potions: {P['potions']}")
    print(f"Weapon: {w['name'] if w else P['equipped_weapon']}")


def save():
    # Save the current game state to the JSON save file.
    data = {
        "player": P,
        "room_history": HISTORY,
        "event_timeline": EVENTS,
        "run_status": STATUS
    }

    try:
        # Use the same direct Path.open() approach as the working food truck game.
        with SAVE_FILE.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print(f"Game saved to {SAVE_FILE.name}.")
        return True

    except (OSError, TypeError, ValueError) as e:
        print("Save failed.")
        print(f"Error: {e}")
        return False


def validate_save(d):
    """Reject edited or inconsistent save files before using their values.

    These checks detect common save-file edits (such as changing health and
    max_health to 900). They are validation, not cryptographic protection:
    a person who can edit the game code can also remove these checks.
    """
    if not isinstance(d, dict) or not all(k in d for k in
            ("player", "room_history", "event_timeline", "run_status")):
        raise ValueError("missing save sections")
    if d["run_status"] not in ("active", "dead", "retired"):
        raise ValueError("invalid run status")

    p = d["player"]
    if not isinstance(p, dict):
        raise ValueError("player data must be an object")
    required = ("name", "health", "max_health", "attack_min", "attack_max",
                "starting_gold", "gold", "potions", "room",
                "equipped_weapon", "weapons", "perks", "effects")
    for k in required:
        if k not in p:
            raise ValueError(f"missing player field: {k}")

    def whole_number(value, label, minimum=0):
        # bool is a subclass of int in Python, so reject it explicitly.
        if type(value) is not int or value < minimum:
            raise ValueError(f"invalid {label}; expected an integer >= {minimum}")
        return value

    if not isinstance(p["name"], str) or not p["name"].strip():
        raise ValueError("invalid player name")

    ps = D["player_start"]
    expected_max = whole_number(ps["max_health"], "configured max health", 1)
    max_health = whole_number(p["max_health"], "max health", 1)
    if max_health != expected_max:
        raise ValueError(f"max health was changed (expected {expected_max})")

    health = whole_number(p["health"], "health")
    if health > max_health:
        raise ValueError("health cannot exceed the configured maximum")
    if d["run_status"] == "dead" and health != 0:
        raise ValueError("a dead run must have 0 health")
    if d["run_status"] == "active" and health == 0:
        raise ValueError("an active run cannot have 0 health")

    room = whole_number(p["room"], "room")
    gold = whole_number(p["gold"], "gold")
    starting_gold = whole_number(p["starting_gold"], "starting gold")
    potions = whole_number(p["potions"], "potions")
    attack_min = whole_number(p["attack_min"], "minimum attack")
    attack_max = whole_number(p["attack_max"], "maximum attack")
    if starting_gold != ps["starting_gold"]:
        raise ValueError("starting gold does not match the game settings")
    if attack_min != ps["attack_min"] or attack_max != ps["attack_max"]:
        raise ValueError("player attack range was changed from the configured values")
    if attack_min > attack_max:
        raise ValueError("minimum attack cannot exceed maximum attack")

    # Only weapons/perks defined by the game data are accepted. This prevents
    # edited weapon damage or invented weapon IDs from granting extra power.
    if not isinstance(p["weapons"], dict):
        raise ValueError("weapons must be an object")
    known_weapons = {w["id"]: w for w in D["weapons"]}
    for weapon_id, saved_weapon in p["weapons"].items():
        if weapon_id not in known_weapons or not isinstance(saved_weapon, dict):
            raise ValueError("save contains an unknown or invalid weapon")
        canonical = known_weapons[weapon_id]
        for field in ("id", "name", "damage", "perks"):
            if saved_weapon.get(field) != canonical.get(field):
                raise ValueError(f"weapon data was modified: {weapon_id}")
        durability = whole_number(saved_weapon.get("durability"),
                                  f"{weapon_id} durability")
        if durability > canonical["durability"]:
            raise ValueError(f"weapon durability exceeds its maximum: {weapon_id}")
    if p["equipped_weapon"] not in p["weapons"]:
        raise ValueError("equipped weapon is not in the player's inventory")

    if not isinstance(p["perks"], list) or any(
            perk not in [x["id"] for x in D["perks"]] for perk in p["perks"]):
        raise ValueError("save contains an unknown perk")
    if not isinstance(p["effects"], dict):
        raise ValueError("effects must be an object")
    for effect in ("strength", "speed", "toughness"):
        if type(p["effects"].get(effect)) is not int or p["effects"][effect] not in (0, 1):
            raise ValueError(f"invalid {effect} effect")

    history = d["room_history"]
    events = d["event_timeline"]
    if not isinstance(history, list) or not isinstance(events, list):
        raise ValueError("room history and event timeline must be lists")
    if len(history) != room:
        raise ValueError("room history does not match room number")

    # Bound resources by the best possible rewards for the number of rooms
    # recorded. This catches implausible edits without imposing an arbitrary
    # small cap on a legitimately long run.
    max_enemy_gold = max((max(e["gold"]) for group in
        (D["enemies"], D["elite_enemies"], D["bosses"]) for e in group), default=0)
    max_chest_gold = max((max(c["gold"]) for c in D["chests"]), default=0)
    max_chest_potions = max((max(c["potions"]) for c in D["chests"]), default=0)
    combat_count = sum(1 for r in history if isinstance(r, dict) and r.get("room_type") == "combat")
    chest_count = sum(1 for r in history if isinstance(r, dict) and r.get("room_type") == "chest")
    if gold > starting_gold + combat_count * max_enemy_gold + chest_count * max_chest_gold:
        raise ValueError("gold total is too high for the recorded rooms")
    if potions > ps["potions"] + chest_count * max_chest_potions:
        raise ValueError("potion count is too high for the recorded rooms")

    numeric_room_fields = ("damage_taken", "gold_found", "potions_found",
                           "health_start", "health_end", "health_restored", "potions_used")
    for i, r in enumerate(history, 1):
        if not isinstance(r, dict) or r.get("room_number") != i:
            raise ValueError("room numbers are not consecutive")
        if r.get("room_type") not in ROOM_TYPES:
            raise ValueError(f"invalid room type in room {i}")
        for field in numeric_room_fields:
            whole_number(r.get(field), f"room {i} {field}")
        if r["health_start"] > max_health or r["health_end"] > max_health:
            raise ValueError(f"health exceeds maximum in room {i}")
        if r["health_start"] - r["damage_taken"] + r["health_restored"] != r["health_end"]:
            raise ValueError(f"health equation failed in room {i}")

    event_numeric_fields = ("room_number", "health_before", "health_after",
                            "max_health", "damage_taken", "health_restored",
                            "potions_used", "potions_remaining", "gold_total")
    for i, e in enumerate(events):
        if not isinstance(e, dict) or e.get("step") != i:
            raise ValueError("event steps are not consecutive")
        for field in event_numeric_fields:
            whole_number(e.get(field), f"event {i} {field}")
        if e["max_health"] != max_health:
            raise ValueError(f"max health mismatch in event {i}")
        if e["health_before"] > max_health or e["health_after"] > max_health:
            raise ValueError(f"health exceeds maximum in event {i}")
        if e["health_change"] != e["health_after"] - e["health_before"]:
            raise ValueError(f"health change mismatch in event {i}")
        if e["health_before"] - e["damage_taken"] + e["health_restored"] != e["health_after"]:
            raise ValueError(f"health equation failed in event {i}")
    if not events or events[0].get("event") != "start":
        raise ValueError("event timeline is missing its starting snapshot")
    if events[0].get("health_after") != max_health:
        raise ValueError("starting health does not match configured max health")

    return True


def load_save():
    global P, HISTORY, EVENTS, STATUS

    try:
        with SAVE_FILE.open("r", encoding="utf-8") as f:
            d = json.load(f)

        validate_save(d)

        P = d["player"]
        HISTORY = d["room_history"]
        EVENTS = d["event_timeline"]
        STATUS = d["run_status"]
        return True

    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        raise SystemExit(f"Could not load save file {SAVE_FILE.name}: {e}")


def reports():
    rooms = pd.DataFrame(HISTORY, columns=ROOM_COLUMNS)
    events = pd.DataFrame(EVENTS, columns=EVENT_COLUMNS)
    if rooms.empty:
        grouped = pd.DataFrame(columns=STATS_COLUMNS)
    else:
        grouped = rooms.groupby("room_type").agg(
            room_count=("room_number","count"),
            gold_found=("gold_found","sum"),
            damage_taken=("damage_taken","sum")).reset_index()
        grouped["room_percent"] = (grouped["room_count"] / len(rooms) * 100).round(1)
        grouped = grouped[STATS_COLUMNS]
    rooms.to_csv(ROOM_LOG_FILE, index=False)
    grouped.to_csv(STATS_FILE, index=False)
    events.to_csv(EVENT_LOG_FILE, index=False)

    combat_rooms = rooms[rooms["room_type"] == "combat"]
    defeated = int((combat_rooms["outcome"] == "defeated").sum()) if not combat_rooms.empty else 0
    escaped = int((combat_rooms["outcome"] == "fled").sum()) if not combat_rooms.empty else 0
    total_gold = int(rooms["gold_found"].sum()) if not rooms.empty else 0
    total_damage = int(rooms["damage_taken"].sum()) if not rooms.empty else 0
    found_potions = int(rooms["potions_found"].sum()) if not rooms.empty else 0
    used = int(events["potions_used"].sum()) if not events.empty else 0
    restored = int(events["health_restored"].sum()) if not events.empty else 0

    print("\n========== FINAL REPORT ==========")
    print(f"Player: {P['name']}")
    print(f"Run ended: {STATUS}")
    print(f"Rooms entered: {len(rooms)}")
    print(f"Deepest room: {P['room'] if P['room'] else 'No rooms explored'}")
    print(f"Enemies defeated: {defeated}")
    print(f"Enemies escaped: {escaped}")
    print(f"Gold collected: {total_gold}")
    print(f"Damage taken: {total_damage}")
    print(f"Potions found: {found_potions}")
    print(f"Potions used: {used}")
    print(f"Health restored: {restored}")
    if rooms.empty:
        print("Highest-gold room: None")
    else:
        top = rooms.iloc[int(rooms["gold_found"].to_numpy().argmax())]
        print(f"Highest-gold room: {int(top.room_number)} ({int(top.gold_found)} gold)")
    print("\nRoom statistics:")
    print(grouped.to_string(index=False) if not grouped.empty else "No rooms explored.")
    print(f"\nReports written to {ROOM_LOG_FILE}, {STATS_FILE}, {EVENT_LOG_FILE}")


def finish(status):
    global STATUS
    STATUS = status
    event("retirement" if status == "retired" else "death",
          P["room"], "none", "between_rooms",
          P["health"], P["health"], encounter="run_end")
    save()
    reports()


def menu():
    while STATUS == "active":
        print(f"\n--- Room {P['room']} ---")
        print("1. Explore\n2. Stats\n3. Use potion\n4. Save\n5. Save and quit\n6. Retire")
        x = input("> ").strip()
        if x == "1":
            explore()
        elif x == "2":
            stats()
        elif x == "3":
            use_potion()
        elif x == "4":
            save()
        elif x == "5":
            if save():
                return
        elif x == "6":
            finish("retired")
        else:
            print("Invalid choice.")


def main():
    load_data()
    if SAVE_FILE.exists():
        load_save()
        if STATUS != "active":
            reports()
            return
        print(f"Save found for {P['name']} at room {P['room']}.")
        if input("Resume it? [Y/N]: ").strip().lower() != "y":
            print("Move or rename dungeon_save.json to start a fresh run.")
            return
    else:
        new_player()
    menu()


if __name__ == "__main__":
    main()