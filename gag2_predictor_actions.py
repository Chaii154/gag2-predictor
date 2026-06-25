"""
GAG2 Discord Webhook Predictor - FOCUSED & CLEAN
Fokus: Super Seeds, Watering Can, All Sprinklers, Cuaca Mutasi, Fence Props, Pet Spawn
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
        "set lewat environment variable supaya tidak ke-leak kalau script dibagikan/di-upload."
    )

# Link private server (dipasang di embed pet spawn)
PRIVATE_SERVER_LINK = "https://www.roblox.com/share?code=803e2bdb19ceda4a8bb381469a30f8ff&type=Server"

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
    {"name": "🌧️ Rain",           "mutation": "Wet",        "mult": "2x",   "rare": False, "tip": "Tanaman basah, bonus kecil"},
    {"name": "🌬️ Wind",          "mutation": "Windswept",  "mult": "5x",   "rare": False, "tip": "Angin kencang, bonus sedang"},
    {"name": "🌈 Rainbow",        "mutation": "Rainbow",    "mult": "10x",  "rare": True,  "tip": "🌈 Rainbow Seeds spawn di map!"},
    {"name": "❄️ Snow",           "mutation": "Frozen",     "mult": "14x",  "rare": True,  "tip": "❄️ Frozen mutation, nilai 14x!"},
    {"name": "💛 Gold Moon",      "mutation": "Gold",       "mult": "15x",  "rare": True,  "tip": "💛 Gold Seeds spawn di map!"},
    {"name": "⛈️ Thunderstorm",  "mutation": "Electric",   "mult": "25x",  "rare": True,  "tip": "⚡ Electric! Tanam crop terbaik!"},
    {"name": "🌈🌙 Rainbow Moon","mutation": "Rainbow",    "mult": "40x",  "rare": True,  "tip": "🌈 Rainbow Seeds! Sangat langka!"},
    {"name": "🌟 Starfall",       "mutation": "Starstruck", "mult": "50x",  "rare": True,  "tip": "🌟 Starstruck! Hanya via event!"},
    {"name": "🩸 Blood Moon",     "mutation": "Bloodlit",   "mult": "80x",  "rare": True,  "tip": "🚨 TERTINGGI! Tanam Super Seeds!"},
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
    {"name": "Frog",             "emoji": "🐸", "rarity": "Common",    "price": "10,000 S",      "spawn": 11.9, "ability": "+Jump Height (bantu ambil tanaman tinggi)", "tier": "B"},
    {"name": "Bunny",            "emoji": "🐰", "rarity": "Common",    "price": "20,000 S",      "spawn": 10.0, "ability": "+Walk Speed (bisa stack!)", "tier": "A"},
    {"name": "Robin",            "emoji": "🐦", "rarity": "Common",    "price": "15,000 S",      "spawn": 9.0,  "ability": "Panen otomatis (tapi juga makan tanaman kamu)", "tier": "C"},
    {"name": "Owl",              "emoji": "🦉", "rarity": "Uncommon",  "price": "30,000 S",      "spawn": 7.0,  "ability": "Alert saat Legendary/Mythic/Super pet spawn!", "tier": "B"},
    {"name": "Deer",             "emoji": "🦌", "rarity": "Rare",      "price": "50,000 S",      "spawn": 5.0,  "ability": "-10% Growth Time (panen lebih cepat!)", "tier": "A"},
    {"name": "Monkey",           "emoji": "🐒", "rarity": "Mythic",    "price": "1,000,000 S",   "spawn": 2.0,  "ability": "Panen buah otomatis sesekali", "tier": "B"},
    {"name": "Bee",              "emoji": "🐝", "rarity": "Legendary", "price": "1,000,000 S",   "spawn": 1.5,  "ability": "Sengat pencuri yang masuk garden!", "tier": "S"},
    {"name": "Raccoon",          "emoji": "🦝", "rarity": "Legendary", "price": "2,000,000 S",   "spawn": 1.2,  "ability": "Curi buah dari garden kosong di malam hari", "tier": "S"},
    {"name": "Golden Dragonfly", "emoji": "✨", "rarity": "Legendary", "price": "5,000,000 S",   "spawn": 0.8,  "ability": "2x peluang Gold mutation di tanaman!", "tier": "S"},
    {"name": "Unicorn",          "emoji": "🦄", "rarity": "Legendary", "price": "12,000,000 S",  "spawn": 0.5,  "ability": "2x peluang Rainbow mutation! (terbaik untuk profit!)", "tier": "S"},
    {"name": "Black Dragon",     "emoji": "🐲", "rarity": "Mythic",    "price": "TBA",           "spawn": 0.3,  "ability": "Semburkan api ke pencuri garden!", "tier": "S"},
    {"name": "Ice Serpent",      "emoji": "🐍", "rarity": "Super",     "price": "TBA",           "spawn": 0.1,  "ability": "Pertahanan terkuat, bekukan pencuri!", "tier": "S"},
    {"name": "Strawberry Sniper","emoji": "🍓", "rarity": "Super",     "price": "TBA",           "spawn": 0.05, "ability": "Sniper! Tembak pencuri dari jauh!", "tier": "S"},
]

RARITY_COLOR = {
    "Common": "⬜", "Uncommon": "🟩", "Rare": "🟦",
    "Epic": "🟪", "Legendary": "🟧", "Mythic": "🟥", "Super": "⭐", "Rainbow": "🌈"
}

# ══════════════════════════════════════════════════════
# 🍎 FRUIT BASE SELL PRICE (buat hitung mana yang "OP" saat mutasi aktif)
# Base price = harga normal jual per buah (tanpa mutasi)
# ══════════════════════════════════════════════════════
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

def get_time_info():
    now = datetime.now(timezone.utc)
    wib_hour = (now.hour + 7) % 24
    wib_str = f"{wib_hour:02d}:{now.minute:02d} WIB"
    cycle_s = now.timestamp() % 300
    time_to_next = 300 - cycle_s
    mins = int(time_to_next // 60)
    secs = int(time_to_next % 60)
    restock_ts = int(now.timestamp() + time_to_next)
    return now, wib_str, mins, secs, restock_ts

def pick_weather():
    common_w = [w for w in MUTATION_WEATHERS if not w["rare"]]
    rare_w   = [w for w in MUTATION_WEATHERS if w["rare"]]
    active = random.choice(rare_w) if random.random() < 0.20 else random.choice(common_w)
    upcoming = []
    for _ in range(3):
        if random.random() < 0.18:
            upcoming.append(random.choice(rare_w))
        else:
            upcoming.append(random.choice(common_w))
    return active, upcoming

def pick_super_seeds_available():
    available = []
    for s in SUPER_SEEDS:
        if random.random() * 100 < s["chance"]:
            available.append(s)
    for s in MYTHIC_SEEDS:
        if random.random() * 100 < s["chance"]:
            available.append(s)
    return available

def pick_next_super_seeds():
    available = []
    for s in SUPER_SEEDS:
        if random.random() * 100 < s["chance"] * 1.2:
            available.append(s)
    for s in MYTHIC_SEEDS:
        if random.random() * 100 < s["chance"] * 1.1:
            available.append(s)
    return available

def pick_sprinklers_stock():
    stocked = []
    for g in WATERING_GEAR:
        if random.random() * 100 < g["stock_chance"]:
            stocked.append(g)
    return stocked if stocked else WATERING_GEAR[:3]

def pick_pet_spawns():
    spawning = []
    for p in ALL_PETS:
        roll = random.random() * 100
        if roll < p["spawn"] * 3:
            spawning.append(p)
    if len(spawning) < 2:
        commons = [p for p in ALL_PETS if p["rarity"] == "Common"]
        spawning = random.sample(commons, min(2, len(commons))) + spawning
    return spawning[:6]

def get_active_mult_value(active_weather):
    """Ambil multiplier numerik dari teks mult (e.g. '80x' -> 80)."""
    try:
        return float(active_weather["mult"].replace("x", ""))
    except (ValueError, KeyError):
        return 1.0

def compute_fruit_prices(active_weather):
    """Hitung harga jual fruit sekarang = base price x multiplier cuaca aktif.
    Diurutkan dari paling mahal (paling OP) ke paling murah."""
    mult = get_active_mult_value(active_weather)
    mutation_name = active_weather.get("mutation", "Normal")
    priced = []
    for f in FRUIT_BASE_PRICE:
        current_price = int(f["base"] * mult)
        priced.append({**f, "current_price": current_price, "mutation": mutation_name, "mult": active_weather["mult"]})
    priced.sort(key=lambda x: x["current_price"], reverse=True)
    return priced

def send_to_discord(now, wib_str, mins, secs, restock_ts):
    active_weather, next_weathers = pick_weather()
    super_now   = pick_super_seeds_available()
    super_next  = pick_next_super_seeds()
    sprinklers  = pick_sprinklers_stock()
    pet_spawns  = pick_pet_spawns()
    fruit_prices = compute_fruit_prices(active_weather)

    header = (
        "```ansi\n"
        "\u001b[1;32m╔══════════════════════════════════════════╗\u001b[0m\n"
        "\u001b[1;32m║   🌿  GAG2 PREDICTOR — KiKo15400 Server  ║\u001b[0m\n"
        "\u001b[1;32m╚══════════════════════════════════════════╝\u001b[0m\n"
        "```"
    )

    countdown_txt = f"<t:{restock_ts}:F>  •  <t:{restock_ts}:R>"

    rare_tag = " 🚨 **[ RARE! ]**" if active_weather["rare"] else ""
    embed_status = {
        "title": "📡  STOCK & STATUS SEKARANG",
        "color": 0x57f287,
        "fields": [
            {
                "name": "🕐  Waktu & Restock Berikutnya",
                "value": (
                    f"```\nJam (WIB) : {wib_str}\nSiklus    : Setiap 5 menit (global)\n```"
                    f"⏳ Restock di: {countdown_txt}"
                ),
                "inline": False
            },
            {
                "name": f"🌦️  Cuaca Aktif{rare_tag}",
                "value": (
                    f"```\nCuaca    : {active_weather['name']}\n"
                    f"Mutation : {active_weather['mutation']}\n"
                    f"Multiplier: {active_weather['mult']}\n```\n"
                    f"💡 {active_weather['tip']}"
                ),
                "inline": False
            }
        ],
        "footer": {"text": "GAG2 Predictor for KiKo15400 • Update tiap 5 menit"}
    }

    def fmt_seeds(seed_list, label):
        if not seed_list:
            return f"*Tidak ada {label} yang tersedia saat ini*"
        lines = []
        for i, s in enumerate(seed_list, 1):
            lines.append(
                f"`{i}.` {s['emoji']} **{s['name']}**\n"
                f"     💰 Harga: `{s['price']}` | Chance: `{s['chance']}%`\n"
                f"     💡 {s['tip']}"
            )
        return "\n".join(lines)

    embed_seeds_now = {
        "title": "⭐  SUPER & MYTHIC SEEDS — TERSEDIA SEKARANG",
        "color": 0xffd700,
        "description": fmt_seeds(super_now, "Super/Mythic"),
        "fields": [
            {"name": "⏳  Restock Slot Ini Berakhir", "value": countdown_txt, "inline": False}
        ],
        "footer": {"text": "⭐ Super seeds = rarity tertinggi di GAG2"}
    }

    sprinkler_lines = []
    for i, g in enumerate(WATERING_GEAR, 1):
        rc = RARITY_COLOR.get(g["rarity"], "")
        in_stock = "✅" if any(s["name"] == g["name"] for s in sprinklers) else "❌"
        sprinkler_lines.append(
            f"`{i}.` {g['emoji']} **{g['name']}** {in_stock}\n"
            f"     💰 `{g['price']}` | {rc} {g['rarity']}\n"
            f"     ⚡ {g['effect']}"
        )

    embed_sprinklers = {
        "title": "💧  WATERING CAN & ALL SPRINKLERS — STOCK SEKARANG",
        "color": 0x00bcd4,
        "description": "\n".join(sprinkler_lines),
        "fields": [
            {"name": "📌  Keterangan", "value": "✅ = Tersedia sekarang di shop  |  ❌ = Tidak ada stok", "inline": False},
            {"name": "⏳  Restock Berikutnya", "value": countdown_txt, "inline": False},
        ],
        "footer": {"text": "George's Gear Shop • Restock tiap 5 menit"}
    }

    pet_lines = []
    for i, p in enumerate(pet_spawns, 1):
        rc = RARITY_COLOR.get(p["rarity"], "")
        tier_color = "🔴" if p["tier"] == "S" else "🟡" if p["tier"] == "A" else "🟢" if p["tier"] == "B" else "⚪"
        pet_lines.append(
            f"`{i}.` {p['emoji']} **{p['name']}** {tier_color} Tier {p['tier']}\n"
            f"     {rc} {p['rarity']} | 💰 `{p['price']}`\n"
            f"     ⚡ {p['ability']}"
        )

    all_pet_ref = []
    for i, p in enumerate(ALL_PETS, 1):
        rc = RARITY_COLOR.get(p["rarity"], "")
        all_pet_ref.append(f"`{i:02d}.` {p['emoji']} {p['name']} — {rc} {p['rarity']} | {p['price']}")

    has_sniper = any(p["name"] == "Strawberry Sniper" for p in pet_spawns)
    sniper_alert = (
        f"🚨 **Strawberry Sniper kemungkinan spawn sekarang!** Cepat join private server:\n{PRIVATE_SERVER_LINK}"
        if has_sniper else
        f"🔗 Join private server buat cek langsung: {PRIVATE_SERVER_LINK}"
    )

    embed_pets = {
        "title": "🐾  PET SPAWN PREDICTOR — Server KiKo15400 (SEKARANG)",
        "color": 0xe91e63,
        "description": (
            "⚠️ *Prediksi berdasarkan spawn rate per pet. Spawn bersifat random per server.*\n\n"
            "**🟢 Pet yang kemungkinan SPAWN sekarang:**\n\n"
            + "\n".join(pet_lines)
            + f"\n\n{sniper_alert}"
        ),
        "fields": [
            {"name": "📋  Semua Pet GAG2 (Referensi)", "value": "\n".join(all_pet_ref[:8]), "inline": False},
            {"name": "\u200b", "value": "\n".join(all_pet_ref[8:]), "inline": False},
        ],
        "footer": {"text": "🐾 Pet spawn bisa di-steal sebelum sampai garden — jaga baik-baik!"}
    }

    next_seeds_txt = fmt_seeds(super_next, "Super/Mythic")
    embed_seeds_next = {
        "title": "🔮  PREDIKSI SUPER & MYTHIC SEEDS — RESTOCK BERIKUTNYA",
        "color": 0xb8860b,
        "description": next_seeds_txt,
        "fields": [
            {"name": "⏳  Estimasi Restock", "value": countdown_txt, "inline": False},
            {
                "name": "📋  Referensi Semua Super Seeds",
                "value": (
                    "```\n"
                    "No  Nama              Harga       Chance\n"
                    "─────────────────────────────────────────\n"
                    "01  🌸 Moon Bloom     ∞ S         0.35%\n"
                    "02  🌿 Beanstalk      ∞ S         0.35%\n"
                    "03  🍏 Poison Apple   ∞ S         0.30%\n"
                    "04  🔥 Dragon's Breath 1,499 R    0.27%\n"
                    "─────────────────────────────────────────\n"
                    "⚠️  Super seeds TERJUAL HABIS dalam detik!\n"
                    "```"
                ),
                "inline": False
            }
        ],
        "footer": {"text": "🔮 Prediksi, bukan kepastian — cuaca & shop tetap random"}
    }

    weather_lines = []
    labels = ["1️⃣  Berikutnya", "2️⃣  Setelah itu", "3️⃣  Perkiraan ke-3"]
    for i, w in enumerate(next_weathers):
        rare_mark = " 🚨 RARE!" if w["rare"] else ""
        weather_lines.append(
            f"**{labels[i]}{rare_mark}**\n"
            f"```\nCuaca     : {w['name']}\nMutation  : {w['mutation']}\nMultiplier: {w['mult']}\n```"
            f"💡 {w['tip']}"
        )

    embed_weather_next = {
        "title": "🌦️  PREDIKSI CUACA SELANJUTNYA",
        "color": 0x5865f2,
        "description": "\n\n".join(weather_lines) + f"\n\n⏳  Estimasi cuaca berganti: {countdown_txt}",
        "fields": [
            {
                "name": "📋  Semua Cuaca Mutasi (dari terkecil ke terbesar)",
                "value": (
                    "```\n"
                    "No  Cuaca           Mutation     Mult\n"
                    "────────────────────────────────────────\n"
                    "01  🌧️ Rain          Wet           2x\n"
                    "02  🌬️ Wind          Windswept     5x\n"
                    "03  🌈 Rainbow       Rainbow      10x\n"
                    "04  ❄️ Snow          Frozen        14x\n"
                    "05  💛 Gold Moon     Gold          15x\n"
                    "06  ⛈️ Thunderstorm  Electric      25x\n"
                    "07  🌈🌙 Rainbow Moon Rainbow      40x\n"
                    "08  🌟 Starfall      Starstruck    50x\n"
                    "09  🩸 Blood Moon    Bloodlit    80x ⚠️\n"
                    "────────────────────────────────────────\n"
                    "❌ Clear Sky & Night = tidak ada mutasi\n"
                    "```"
                ),
                "inline": False
            }
        ],
        "footer": {"text": "Cuaca bersifat global — semua server sama!"}
    }

    fence_lines = []
    for i, f in enumerate(FENCE_PROPS, 1):
        rc = RARITY_COLOR.get(f["rarity"], "")
        fence_lines.append(
            f"`{i:02d}.` {f['emoji']} **{f['name']}**\n"
            f"      {rc} {f['rarity']} | Drop: `{f['chance']}` | 📦 {f['source']}"
        )

    embed_fences = {
        "title": "🏠  FENCE PROPS — Referensi Semua Jenis Pagar",
        "color": 0x8b6914,
        "description": (
            "Props pagar didapat dari **Fence Crate** di Props Shop.\n"
            "Semakin langka = semakin kecil chance dari crate!\n\n"
            + "\n".join(fence_lines)
        ),
        "fields": [
            {
                "name": "💡  Tips Fence",
                "value": (
                    "• Beli **Fence Crate** di Props Shop untuk rolling pagar\n"
                    "• **Rainbow Fence** = paling langka (~0.5%)\n"
                    "• **Futuristic Fence** = Legendary (1.03% chance)\n"
                    "• Fence hanya kosmetik, tidak mempengaruhi farming"
                ),
                "inline": False
            }
        ],
        "footer": {"text": "Props Shop • Fence Crate"}
    }

    # ════════════════════════════════════════════════
    # EMBED: FRUIT PRICE / "BUAH OP" SAAT INI
    # Harga = base price x multiplier cuaca aktif sekarang
    # ════════════════════════════════════════════════
    fruit_lines = []
    for i, fr in enumerate(fruit_prices[:8], 1):
        op_tag = " 🔥 **OP!**" if i <= 3 else ""
        fruit_lines.append(
            f"`{i}.` {fr['emoji']} **{fr['name']}**{op_tag}\n"
            f"     💰 Harga sekarang: `{fr['current_price']:,} S` (base `{fr['base']:,}` × {fr['mult']})"
        )

    embed_fruit_prices = {
        "title": "🍎  FRUIT PRICE — Harga Jual Sekarang",
        "color": 0xff6b35,
        "description": (
            f"Mutasi aktif: **{fruit_prices[0]['mutation']}** ({active_weather['mult']})\n"
            "Harga di bawah = base price tiap buah dikali multiplier cuaca yang sedang aktif.\n\n"
            + "\n".join(fruit_lines)
        ),
        "fields": [
            {"name": "🔥  Top 3 paling OP buat dijual sekarang", "value": "\n".join(f"{fr['emoji']} {fr['name']}" for fr in fruit_prices[:3]), "inline": False},
            {"name": "⏳  Mutasi berganti", "value": countdown_txt, "inline": False},
        ],
        "footer": {"text": "Harga dasar referensi komunitas — bisa beda sedikit dari in-game"}
    }

    p1 = {
        "username": "GAG2 Predictor 🌱",
        "content": header,
        "embeds": [embed_status, embed_seeds_now, embed_sprinklers, embed_pets, embed_fruit_prices]
    }
    p2 = {
        "username": "GAG2 Predictor 🌱",
        "content": "🔽 **PREDIKSI & REFERENSI** 🔽",
        "embeds": [embed_seeds_next, embed_weather_next, embed_fences]
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
    now, wib_str, mins, secs, restock_ts = get_time_info()
    print(f"[{wib_str}] Mengirim prediksi GAG2 untuk KiKo15400...")
    send_to_discord(now, wib_str, mins, secs, restock_ts)

if __name__ == "__main__":
    main()
