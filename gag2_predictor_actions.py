"""
GAG2 Discord Webhook Predictor - PER-KATEGORI, KOTAK ASCII, COUNTDOWN JELAS
Fokus: Super Seeds, Watering Can, All Sprinklers, Cuaca Mutasi, Fence Props, Pet Spawn, Fruit Price
By: KiKo15400
"""

import requests
import random
import os
from datetime import datetime, timezone

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
if not WEBHOOK_URL:
    raise RuntimeError(
        "WEBHOOK_URL env var belum di-set. Jangan hardcode webhook URL di kode, "
        "set lewat environment variable / GitHub secret supaya tidak ke-leak."
    )

PRIVATE_SERVER_LINK = "https://www.roblox.com/share?code=803e2bdb19ceda4a8bb381469a30f8ff&type=Server"

# ══════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════
SUPER_SEEDS = [
    {"name": "Moon Bloom",      "emoji": "🌸", "price": "∞ S",      "chance": 0.35, "tip": "Terbaik untuk Blood Moon!"},
    {"name": "Beanstalk",       "emoji": "🌿", "price": "∞ S",      "chance": 0.35, "tip": "Tinggi & nilai jual besar"},
    {"name": "Poison Apple",    "emoji": "🍏", "price": "∞ S",      "chance": 0.30, "tip": "Langka & berharga"},
    {"name": "Dragon's Breath", "emoji": "🔥", "price": "1,499 R",  "chance": 0.27, "tip": "Defense + harvest, Robux only"},
]

MYTHIC_SEEDS = [
    {"name": "Rainbow Seed",  "emoji": "🌈", "price": "EVENT",    "chance": 1.5, "tip": "Spawn saat Rainbow Moon"},
    {"name": "Gold Seed",     "emoji": "💛", "price": "EVENT",    "chance": 1.2, "tip": "Spawn saat Gold Moon"},
    {"name": "Ghost Pepper",  "emoji": "👻", "price": "PACK",     "chance": 1.0, "tip": "Dari Ghost Pepper Pack (1%)"},
    {"name": "Lychee",        "emoji": "🔴", "price": "750,000 S","chance": 0.8, "tip": "Nilai jual tinggi"},
]

WATERING_GEAR = [
    {"name": "Watering Can",        "emoji": "🪣", "price": "FREE",         "rarity": "Common",    "effect": "Manual siram 1 tanaman", "stock_chance": 100},
    {"name": "Common Sprinkler",    "emoji": "💧", "price": "3,000 S",      "rarity": "Common",    "effect": "Area kecil, otomatis siram", "stock_chance": 90},
    {"name": "Uncommon Sprinkler",  "emoji": "💧", "price": "10,000 S",     "rarity": "Uncommon",  "effect": "Area sedang, lebih cepat", "stock_chance": 70},
    {"name": "Rare Sprinkler",      "emoji": "💧", "price": "50,000 S",     "rarity": "Rare",      "effect": "Area besar, growth boost", "stock_chance": 45},
    {"name": "Legendary Sprinkler", "emoji": "💧", "price": "100,000 S",    "rarity": "Legendary", "effect": "Area sangat luas + size luck", "stock_chance": 20},
    {"name": "Super Sprinkler",     "emoji": "💧", "price": "1,000,000 S",  "rarity": "Super",     "effect": "Coverage maksimal + 5x speed", "stock_chance": 8},
    {"name": "Rainbow Sprinkler",   "emoji": "🌈", "price": "∞ / Event",    "rarity": "Rainbow",   "effect": "Terbaik di game, rainbow boost", "stock_chance": 2},
]

MUTATION_WEATHERS = [
    {"name": "Rain",           "emoji": "🌧️", "mutation": "Wet",        "mult": "2x",   "rare": False, "tip": "Tanaman basah, bonus kecil"},
    {"name": "Wind",           "emoji": "🌬️", "mutation": "Windswept",  "mult": "5x",   "rare": False, "tip": "Angin kencang, bonus sedang"},
    {"name": "Rainbow",        "emoji": "🌈", "mutation": "Rainbow",    "mult": "10x",  "rare": True,  "tip": "Rainbow Seeds spawn di map!"},
    {"name": "Snow",           "emoji": "❄️", "mutation": "Frozen",     "mult": "14x",  "rare": True,  "tip": "Frozen mutation, nilai 14x!"},
    {"name": "Gold Moon",      "emoji": "💛", "mutation": "Gold",       "mult": "15x",  "rare": True,  "tip": "Gold Seeds spawn di map!"},
    {"name": "Thunderstorm",   "emoji": "⛈️", "mutation": "Electric",   "mult": "25x",  "rare": True,  "tip": "Electric! Tanam crop terbaik!"},
    {"name": "Rainbow Moon",   "emoji": "🌈🌙","mutation": "Rainbow",   "mult": "40x",  "rare": True,  "tip": "Rainbow Seeds! Sangat langka!"},
    {"name": "Starfall",       "emoji": "🌟", "mutation": "Starstruck", "mult": "50x",  "rare": True,  "tip": "Starstruck! Hanya via event!"},
    {"name": "Blood Moon",     "emoji": "🩸", "mutation": "Bloodlit",   "mult": "80x",  "rare": True,  "tip": "TERTINGGI! Tanam Super Seeds!"},
]

FENCE_PROPS = [
    {"name": "Default Fence",       "emoji": "🏠", "chance": "~50%",   "rarity": "Common",    "source": "Default / Gratis"},
    {"name": "Wooden Fence",        "emoji": "🌲", "chance": "~25%",   "rarity": "Common",    "source": "Fence Crate"},
    {"name": "Stone Fence",         "emoji": "🪨", "chance": "~15%",   "rarity": "Uncommon",  "source": "Fence Crate"},
    {"name": "Iron Fence",          "emoji": "⚙️", "chance": "~8%",    "rarity": "Rare",      "source": "Fence Crate"},
    {"name": "Brick Fence",         "emoji": "🧱", "chance": "~5%",    "rarity": "Rare",      "source": "Fence Crate"},
    {"name": "Crystal Fence",       "emoji": "💎", "chance": "~3%",    "rarity": "Epic",      "source": "Fence Crate"},
    {"name": "Golden Fence",        "emoji": "🥇", "chance": "~2%",    "rarity": "Legendary", "source": "Fence Crate"},
    {"name": "Futuristic Fence",    "emoji": "🚀", "chance": "~1.03%", "rarity": "Legendary", "source": "Fence Crate"},
    {"name": "Rainbow Fence",       "emoji": "🌈", "chance": "~0.5%",  "rarity": "Rainbow",   "source": "Fence Crate (sangat langka!)"},
]

ALL_PETS = [
    {"name": "Frog",             "emoji": "🐸", "rarity": "Common",    "price": "10,000 S",      "spawn": 11.9, "ability": "+Jump Height", "tier": "B"},
    {"name": "Bunny",            "emoji": "🐰", "rarity": "Common",    "price": "20,000 S",      "spawn": 10.0, "ability": "+Walk Speed (bisa stack!)", "tier": "A"},
    {"name": "Robin",            "emoji": "🐦", "rarity": "Common",    "price": "15,000 S",      "spawn": 9.0,  "ability": "Panen otomatis (juga makan tanaman)", "tier": "C"},
    {"name": "Owl",              "emoji": "🦉", "rarity": "Uncommon",  "price": "30,000 S",      "spawn": 7.0,  "ability": "Alert pet Legendary/Mythic/Super spawn!", "tier": "B"},
    {"name": "Deer",             "emoji": "🦌", "rarity": "Rare",      "price": "50,000 S",      "spawn": 5.0,  "ability": "-10% Growth Time", "tier": "A"},
    {"name": "Monkey",           "emoji": "🐒", "rarity": "Mythic",    "price": "1,000,000 S",   "spawn": 2.0,  "ability": "Panen buah otomatis sesekali", "tier": "B"},
    {"name": "Bee",              "emoji": "🐝", "rarity": "Legendary", "price": "1,000,000 S",   "spawn": 1.5,  "ability": "Sengat pencuri garden!", "tier": "S"},
    {"name": "Raccoon",          "emoji": "🦝", "rarity": "Legendary", "price": "2,000,000 S",   "spawn": 1.2,  "ability": "Curi buah garden kosong malam hari", "tier": "S"},
    {"name": "Golden Dragonfly", "emoji": "✨", "rarity": "Legendary", "price": "5,000,000 S",   "spawn": 0.8,  "ability": "2x peluang Gold mutation!", "tier": "S"},
    {"name": "Unicorn",          "emoji": "🦄", "rarity": "Legendary", "price": "12,000,000 S",  "spawn": 0.5,  "ability": "2x peluang Rainbow mutation!", "tier": "S"},
    {"name": "Black Dragon",     "emoji": "🐲", "rarity": "Mythic",    "price": "TBA",           "spawn": 0.3,  "ability": "Semburkan api ke pencuri!", "tier": "S"},
    {"name": "Ice Serpent",      "emoji": "🐍", "rarity": "Super",     "price": "TBA",           "spawn": 0.1,  "ability": "Bekukan pencuri!", "tier": "S"},
    {"name": "Strawberry Sniper","emoji": "🍓", "rarity": "Super",     "price": "TBA",           "spawn": 0.05, "ability": "Tembak pencuri dari jauh!", "tier": "S"},
]

FRUIT_BASE_PRICE = [
    {"name": "Carrot",        "emoji": "🥕", "base": 20},
    {"name": "Strawberry",    "emoji": "🍓", "base": 35},
    {"name": "Tomato",        "emoji": "🍅", "base": 60},
    {"name": "Blueberry",     "emoji": "🫐", "base": 90},
    {"name": "Watermelon",    "emoji": "🍉", "base": 2800},
    {"name": "Pumpkin",       "emoji": "🎃", "base": 3200},
    {"name": "Mango",         "emoji": "🥭", "base": 4500},
    {"name": "Coconut",       "emoji": "🥥", "base": 6000},
    {"name": "Cactus",        "emoji": "🌵", "base": 7500},
    {"name": "Dragon Fruit",  "emoji": "🐉", "base": 15000},
    {"name": "Lychee",        "emoji": "🔴", "base": 25000},
    {"name": "Moon Bloom",    "emoji": "🌸", "base": 60000},
    {"name": "Beanstalk",     "emoji": "🌿", "base": 75000},
    {"name": "Poison Apple",  "emoji": "🍏", "base": 90000},
]

RARITY_COLOR = {
    "Common": "⬜", "Uncommon": "🟩", "Rare": "🟦",
    "Epic": "🟪", "Legendary": "🟧", "Mythic": "🟥", "Super": "⭐", "Rainbow": "🌈"
}

# ══════════════════════════════════════════════════════
# HELPER: kotak ASCII per kategori (gaya sama kaya header utama)
# ══════════════════════════════════════════════════════
def ascii_box(label, width=44):
    inner = f"  {label}"
    pad = max(width - len(inner) - 2, 0)
    line = f"║{inner}{' ' * pad}║"
    top = "╔" + "═" * width + "╗"
    bottom = "╚" + "═" * width + "╝"
    return f"```ansi\n\u001b[1;32m{top}\u001b[0m\n\u001b[1;32m{line}\u001b[0m\n\u001b[1;32m{bottom}\u001b[0m\n```"

def get_time_info():
    now = datetime.now(timezone.utc)
    wib_hour = (now.hour + 7) % 24
    wib_str = f"{wib_hour:02d}:{now.minute:02d} WIB"
    cycle_s = now.timestamp() % 300
    time_to_next = 300 - cycle_s
    restock_ts = int(now.timestamp() + time_to_next)
    return now, wib_str, restock_ts

def pick_weather():
    common_w = [w for w in MUTATION_WEATHERS if not w["rare"]]
    rare_w   = [w for w in MUTATION_WEATHERS if w["rare"]]
    active = random.choice(rare_w) if random.random() < 0.20 else random.choice(common_w)
    nxt = random.choice(rare_w) if random.random() < 0.18 else random.choice(common_w)
    return active, nxt

def pick_super_seeds_available():
    avail = [s for s in SUPER_SEEDS if random.random() * 100 < s["chance"]]
    avail += [s for s in MYTHIC_SEEDS if random.random() * 100 < s["chance"]]
    return avail

def pick_next_super_seeds():
    avail = [s for s in SUPER_SEEDS if random.random() * 100 < s["chance"] * 1.2]
    avail += [s for s in MYTHIC_SEEDS if random.random() * 100 < s["chance"] * 1.1]
    return avail

def pick_sprinklers_stock():
    stocked = [g for g in WATERING_GEAR if random.random() * 100 < g["stock_chance"]]
    return stocked if stocked else WATERING_GEAR[:3]

def pick_next_sprinklers_stock():
    stocked = [g for g in WATERING_GEAR if random.random() * 100 < g["stock_chance"] * 0.9]
    return stocked if stocked else WATERING_GEAR[:2]

def pick_pet_spawns():
    spawning = [p for p in ALL_PETS if random.random() * 100 < p["spawn"] * 3]
    if len(spawning) < 2:
        commons = [p for p in ALL_PETS if p["rarity"] == "Common"]
        spawning = random.sample(commons, min(2, len(commons))) + spawning
    return spawning[:6]

def pick_next_pet_spawns():
    spawning = [p for p in ALL_PETS if random.random() * 100 < p["spawn"] * 2.5]
    if len(spawning) < 1:
        commons = [p for p in ALL_PETS if p["rarity"] == "Common"]
        spawning = random.sample(commons, 1)
    return spawning[:4]

def fmt_seeds(seed_list):
    if not seed_list:
        return "*Tidak ada Super/Mythic seed*"
    return "\n".join(
        f"`{i}.` {s['emoji']} **{s['name']}** — 💰 `{s['price']}` | {s['chance']}%"
        for i, s in enumerate(seed_list, 1)
    )

def fmt_gear(gear_list):
    if not gear_list:
        return "*Tidak ada gear di stock*"
    return "\n".join(
        f"`{i}.` {g['emoji']} **{g['name']}** — 💰 `{g['price']}`"
        for i, g in enumerate(gear_list, 1)
    )

def fmt_pets(pet_list):
    if not pet_list:
        return "*Tidak ada pet spawn*"
    return "\n".join(
        f"`{i}.` {p['emoji']} **{p['name']}** ({p['rarity']}) — Tier {p['tier']}"
        for i, p in enumerate(pet_list, 1)
    )

def get_mult_value(weather):
    try:
        return float(weather["mult"].replace("x", ""))
    except (ValueError, KeyError):
        return 1.0

def compute_fruit_prices(weather):
    mult = get_mult_value(weather)
    priced = []
    for f in FRUIT_BASE_PRICE:
        priced.append({**f, "current_price": int(f["base"] * mult)})
    priced.sort(key=lambda x: x["current_price"], reverse=True)
    return priced

def send_to_discord(now, wib_str, restock_ts):
    active_weather, next_weather = pick_weather()
    super_now    = pick_super_seeds_available()
    super_next   = pick_next_super_seeds()
    gear_now     = pick_sprinklers_stock()
    gear_next    = pick_next_sprinklers_stock()
    pets_now     = pick_pet_spawns()
    pets_next    = pick_next_pet_spawns()
    fruit_now    = compute_fruit_prices(active_weather)
    fruit_next   = compute_fruit_prices(next_weather)

    countdown = f"<t:{restock_ts}:F>  •  <t:{restock_ts}:R>"

    # ────────────────────────────────────────
    # EMBED: HEADER / WAKTU
    # ────────────────────────────────────────
    embed_header = {
        "color": 0x2ecc71,
        "description": (
            ascii_box("🌿 GAG2 PREDICTOR — KiKo15400")
            + f"\n🕐 Jam (WIB): `{wib_str}`  |  Siklus: setiap 5 menit (global)\n"
            + f"⏳ **Restock berikutnya:** {countdown}"
        )
    }

    # ────────────────────────────────────────
    # EMBED: SEED
    # ────────────────────────────────────────
    embed_seeds = {
        "color": 0xffd700,
        "description": (
            ascii_box("⭐ SUPER & MYTHIC SEEDS")
            + f"\n🟢 **SEKARANG** (abis {countdown})\n{fmt_seeds(super_now)}\n\n"
            + f"🔮 **NEXT** (mulai {countdown})\n{fmt_seeds(super_next)}"
        )
    }

    # ────────────────────────────────────────
    # EMBED: GEAR / SPRINKLER
    # ────────────────────────────────────────
    embed_gear = {
        "color": 0x00bcd4,
        "description": (
            ascii_box("💧 WATERING CAN & SPRINKLERS")
            + f"\n🟢 **SEKARANG** (abis {countdown})\n{fmt_gear(gear_now)}\n\n"
            + f"🔮 **NEXT** (mulai {countdown})\n{fmt_gear(gear_next)}"
        )
    }

    # ────────────────────────────────────────
    # EMBED: WEATHER
    # ────────────────────────────────────────
    rare_now  = " 🚨RARE" if active_weather["rare"] else ""
    rare_next = " 🚨RARE" if next_weather["rare"] else ""
    embed_weather = {
        "color": 0x5865f2,
        "description": (
            ascii_box("🌦️ CUACA & MUTASI")
            + f"\n🟢 **SEKARANG**{rare_now} (ganti {countdown})\n"
            + f"{active_weather['emoji']} **{active_weather['name']}** → {active_weather['mutation']} ({active_weather['mult']})\n"
            + f"💡 {active_weather['tip']}\n\n"
            + f"🔮 **NEXT**{rare_next} (mulai {countdown})\n"
            + f"{next_weather['emoji']} **{next_weather['name']}** → {next_weather['mutation']} ({next_weather['mult']})\n"
            + f"💡 {next_weather['tip']}"
        )
    }

    # ────────────────────────────────────────
    # EMBED: FRUIT PRICE
    # ────────────────────────────────────────
    top_now  = "\n".join(f"{f['emoji']} **{f['name']}** — `{f['current_price']:,} S`" for f in fruit_now[:5])
    top_next = "\n".join(f"{f['emoji']} **{f['name']}** — `{f['current_price']:,} S`" for f in fruit_next[:5])
    embed_fruit = {
        "color": 0xff6b35,
        "description": (
            ascii_box("🍎 FRUIT PRICE (TOP 5)")
            + f"\n🟢 **SEKARANG** — mutasi {active_weather['mutation']} ({active_weather['mult']}), abis {countdown}\n{top_now}\n\n"
            + f"🔮 **NEXT** — prediksi mutasi {next_weather['mutation']} ({next_weather['mult']})\n{top_next}"
        )
    }

    # ────────────────────────────────────────
    # EMBED: PETS
    # ────────────────────────────────────────
    has_sniper_now = any(p["name"] == "Strawberry Sniper" for p in pets_now)
    sniper_line = (
        f"\n🚨 **Strawberry Sniper kemungkinan ADA sekarang!** Cek private server:\n{PRIVATE_SERVER_LINK}"
        if has_sniper_now else
        f"\n🔗 Private server: {PRIVATE_SERVER_LINK}"
    )
    embed_pets = {
        "color": 0xe91e63,
        "description": (
            ascii_box("🐾 PET SPAWN")
            + f"\n🟢 **SEKARANG** (update {countdown})\n{fmt_pets(pets_now)}\n\n"
            + f"🔮 **NEXT**\n{fmt_pets(pets_next)}"
            + sniper_line
        )
    }

    # ────────────────────────────────────────
    # EMBED: FENCE (referensi, jarang berubah)
    # ────────────────────────────────────────
    fence_lines = "\n".join(
        f"`{i:02d}.` {f['emoji']} **{f['name']}** — {RARITY_COLOR.get(f['rarity'],'')} {f['rarity']} ({f['chance']})"
        for i, f in enumerate(FENCE_PROPS, 1)
    )
    embed_fence = {
        "color": 0x8b6914,
        "description": (
            ascii_box("🏠 FENCE PROPS (Referensi Crate)")
            + f"\n{fence_lines}\n\n💡 Dari **Fence Crate** di Props Shop. Kosmetik, tidak pengaruhi farming."
        )
    }

    # ════════════════════════════════════════
    # KIRIM — pesan 1: stock & cuaca utama, pesan 2: pet & referensi
    # ════════════════════════════════════════
    p1 = {
        "username": "GAG2 Predictor 🌱",
        "embeds": [embed_header, embed_seeds, embed_gear, embed_weather]
    }
    p2 = {
        "username": "GAG2 Predictor 🌱",
        "embeds": [embed_fruit, embed_pets, embed_fence]
    }

    r1 = requests.post(WEBHOOK_URL, json=p1)
    r2 = requests.post(WEBHOOK_URL, json=p2)

    ok1 = r1.status_code in (200, 204)
    ok2 = r2.status_code in (200, 204)

    if ok1 and ok2:
        print(f"✅ [{wib_str}] Sukses kirim ke Discord!")
    else:
        print(f"❌ Error: {r1.status_code} / {r2.status_code}")
        if not ok1: print(r1.text[:300])
        if not ok2: print(r2.text[:300])
        exit(1)

def main():
    now, wib_str, restock_ts = get_time_info()
    print(f"[{wib_str}] Mengirim prediksi GAG2 untuk KiKo15400...")
    send_to_discord(now, wib_str, restock_ts)

if __name__ == "__main__":
    main()
