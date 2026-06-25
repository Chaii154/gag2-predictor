"""
GAG2 Discord Webhook Predictor - FOCUSED & CLEAN
Fokus: Super Seeds, Watering Can, All Sprinklers, Cuaca Mutasi, Fence Props, Pet Spawn
By: KiKo15400
"""

import requests
import random
import os
from datetime import datetime, timezone

WEBHOOK_URL = os.environ.get(
    "WEBHOOK_URL",
    "https://discord.com/api/webhooks/1455445496989745328/BB_6EjQuuRAX_IvfBEcZfpIf66R46GTPZMOJndMvfzoylNZW-K_f98WEhNdI3AXWY8rq"
)

# ══════════════════════════════════════════════════════
# 🌱 SUPER SEEDS (fokus utama)
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

# ══════════════════════════════════════════════════════
# 💧 WATERING CAN & ALL SPRINKLERS
# ══════════════════════════════════════════════════════
WATERING_GEAR = [
    {"name": "Watering Can",        "emoji": "🪣", "price": "FREE",         "rarity": "Common",    "effect": "Manual siram 1 tanaman", "stock_chance": 100},
    {"name": "Common Sprinkler",    "emoji": "💧", "price": "3,000 S",      "rarity": "Common",    "effect": "Area kecil, otomatis siram", "stock_chance": 90},
    {"name": "Uncommon Sprinkler",  "emoji": "💧", "price": "10,000 S",     "rarity": "Uncommon",  "effect": "Area sedang, lebih cepat", "stock_chance": 70},
    {"name": "Rare Sprinkler",      "emoji": "💧", "price": "50,000 S",     "rarity": "Rare",      "effect": "Area besar, growth boost", "stock_chance": 45},
    {"name": "Legendary Sprinkler", "emoji": "💧", "price": "100,000 S",    "rarity": "Legendary", "effect": "Area sangat luas + size luck", "stock_chance": 20},
    {"name": "Super Sprinkler",     "emoji": "💧", "price": "1,000,000 S",  "rarity": "Super",     "effect": "Coverage maksimal + 5x speed", "stock_chance": 8},
    {"name": "Rainbow Sprinkler",   "emoji": "🌈", "price": "∞ / Event",    "rarity": "Rainbow",   "effect": "Terbaik di game, rainbow boost", "stock_chance": 2},
]

# ══════════════════════════════════════════════════════
# 🌦️ CUACA DENGAN MUTASI (tanpa Clear & Night)
# ══════════════════════════════════════════════════════
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

# ══════════════════════════════════════════════════════
# 🏠 FENCE PROPS (dari Fence Crate)
# ══════════════════════════════════════════════════════
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

# ══════════════════════════════════════════════════════
# 🐾 SEMUA PET GAG2
# ══════════════════════════════════════════════════════
ALL_PETS = [
    # (nama, emoji, rarity, harga, spawn_chance%, ability, tier)
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

def get_time_info():
    now = datetime.now(timezone.utc)
    wib_hour = (now.hour + 7) % 24
    wib_str = f"{wib_hour:02d}:{now.minute:02d} WIB"
    cycle_s = now.timestamp() % 300
    time_to_next = 300 - cycle_s
    mins = int(time_to_next // 60)
    secs = int(time_to_next % 60)
    return now, wib_str, mins, secs

def pick_weather():
    common_w = [w for w in MUTATION_WEATHERS if not w["rare"]]
    rare_w   = [w for w in MUTATION_WEATHERS if w["rare"]]
    # cuaca aktif sekarang (80% common, 20% rare)
    active = random.choice(rare_w) if random.random() < 0.20 else random.choice(common_w)
    # prediksi 3 berikutnya
    upcoming = []
    for _ in range(3):
        if random.random() < 0.18:
            upcoming.append(random.choice(rare_w))
        else:
            upcoming.append(random.choice(common_w))
    return active, upcoming

def pick_super_seeds_available():
    """Cek Super & Mythic seed mana yang mungkin available sekarang"""
    available = []
    for s in SUPER_SEEDS:
        if random.random() * 100 < s["chance"]:
            available.append(s)
    for s in MYTHIC_SEEDS:
        if random.random() * 100 < s["chance"]:
            available.append(s)
    return available

def pick_next_super_seeds():
    """Prediksi next restock super/mythic"""
    available = []
    for s in SUPER_SEEDS:
        if random.random() * 100 < s["chance"] * 1.2:
            available.append(s)
    for s in MYTHIC_SEEDS:
        if random.random() * 100 < s["chance"] * 1.1:
            available.append(s)
    return available

def pick_sprinklers_stock():
    """Simulasi stock sprinkler sekarang"""
    stocked = []
    for g in WATERING_GEAR:
        if random.random() * 100 < g["stock_chance"]:
            stocked.append(g)
    return stocked if stocked else WATERING_GEAR[:3]

def pick_pet_spawns():
    """Simulasi pet yang spawn di server KiKo15400"""
    spawning = []
    for p in ALL_PETS:
        # Simulasikan apakah pet ini sedang/akan spawn
        roll = random.random() * 100
        if roll < p["spawn"] * 3:  # dikali 3 biar lebih realistis per sesi
            spawning.append(p)
    # Selalu ada minimal 2-3 common pet
    if len(spawning) < 2:
        commons = [p for p in ALL_PETS if p["rarity"] == "Common"]
        spawning = random.sample(commons, min(2, len(commons))) + spawning
    return spawning[:6]  # max 6 pet ditampilkan

def send_to_discord(now, wib_str, mins, secs):
    active_weather, next_weathers = pick_weather()
    super_now   = pick_super_seeds_available()
    super_next  = pick_next_super_seeds()
    sprinklers  = pick_sprinklers_stock()
    pet_spawns  = pick_pet_spawns()

    # ────────────────────────────────────────
    # HEADER MESSAGE
    # ────────────────────────────────────────
    header = (
        "```ansi\n"
        "\u001b[1;32m╔══════════════════════════════════════════╗\u001b[0m\n"
        "\u001b[1;32m║   🌿  GAG2 PREDICTOR — KiKo15400 Server  ║\u001b[0m\n"
        "\u001b[1;32m╚══════════════════════════════════════════╝\u001b[0m\n"
        "```"
    )

    # ────────────────────────────────────────
    # EMBED 1: STATUS SEKARANG
    # ────────────────────────────────────────
    rare_tag = " 🚨 **[ RARE! ]**" if active_weather["rare"] else ""
    embed_status = {
        "title": "📡  STATUS SERVER SEKARANG",
        "color": 0x57f287,
        "fields": [
            {
                "name": "🕐  Waktu & Restock",
                "value": (
                    f"```\n"
                    f"Jam      : {wib_str}\n"
                    f"Restock  : {mins}m {secs}s lagi\n"
                    f"Siklus   : Setiap 5 menit (global)\n"
                    f"```"
                ),
                "inline": False
            },
            {
                "name": f"🌦️  CUACA AKTIF SEKARANG{rare_tag}",
                "value": (
                    f"```\n"
                    f"Cuaca    : {active_weather['name']}\n"
                    f"Mutation : {active_weather['mutation']}\n"
                    f"Multiplier: {active_weather['mult']}\n"
                    f"```\n"
                    f"💡 {active_weather['tip']}"
                ),
                "inline": False
            }
        ],
        "footer": {"text": "GAG2 Predictor for KiKo15400 • Update tiap 5 menit"}
    }

    # ────────────────────────────────────────
    # EMBED 2: SUPER & MYTHIC SEEDS
    # ────────────────────────────────────────
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

    now_seeds_txt  = fmt_seeds(super_now, "Super/Mythic")
    next_seeds_txt = fmt_seeds(super_next, "Super/Mythic")

    embed_seeds = {
        "title": "⭐  SUPER & MYTHIC SEEDS",
        "color": 0xffd700,
        "fields": [
            {
                "name": "🟢  TERSEDIA SEKARANG",
                "value": now_seeds_txt,
                "inline": False
            },
            {
                "name": f"🔮  PREDIKSI NEXT RESTOCK ({mins}m {secs}s)",
                "value": next_seeds_txt,
                "inline": False
            },
            {
                "name": "📋  REFERENSI SEMUA SUPER SEEDS",
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
        "footer": {"text": "⭐ Super seeds = rarity tertinggi di GAG2"}
    }

    # ────────────────────────────────────────
    # EMBED 3: WATERING CAN & ALL SPRINKLERS
    # ────────────────────────────────────────
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
        "title": "💧  WATERING CAN & ALL SPRINKLERS",
        "color": 0x00bcd4,
        "description": "\n".join(sprinkler_lines),
        "fields": [
            {
                "name": "📌  Keterangan",
                "value": "✅ = Tersedia sekarang di shop  |  ❌ = Tidak ada stok",
                "inline": False
            }
        ],
        "footer": {"text": "George's Gear Shop • Restock tiap 5 menit"}
    }

    # ────────────────────────────────────────
    # EMBED 4: PREDIKSI CUACA SELANJUTNYA
    # ────────────────────────────────────────
    weather_lines = []
    labels = ["1️⃣  Berikutnya", "2️⃣  Setelah itu", "3️⃣  Perkiraan ke-3"]
    for i, w in enumerate(next_weathers):
        rare_mark = " 🚨 RARE!" if w["rare"] else ""
        weather_lines.append(
            f"**{labels[i]}{rare_mark}**\n"
            f"```\n"
            f"Cuaca     : {w['name']}\n"
            f"Mutation  : {w['mutation']}\n"
            f"Multiplier: {w['mult']}\n"
            f"```"
            f"💡 {w['tip']}"
        )

    embed_weather = {
        "title": "🌦️  PREDIKSI CUACA SELANJUTNYA",
        "color": 0x5865f2,
        "description": "\n\n".join(weather_lines),
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

    # ────────────────────────────────────────
    # EMBED 5: FENCE PROPS
    # ────────────────────────────────────────
    fence_lines = []
    for i, f in enumerate(FENCE_PROPS, 1):
        rc = RARITY_COLOR.get(f["rarity"], "")
        fence_lines.append(
            f"`{i:02d}.` {f['emoji']} **{f['name']}**\n"
            f"      {rc} {f['rarity']} | Drop: `{f['chance']}` | 📦 {f['source']}"
        )

    embed_fences = {
        "title": "🏠  FENCE PROPS — Semua Jenis Pagar",
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

    # ────────────────────────────────────────
    # EMBED 6: PET SPAWN PREDICTOR
    # ────────────────────────────────────────
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

    embed_pets = {
        "title": f"🐾  PET SPAWN PREDICTOR — Server KiKo15400",
        "color": 0xe91e63,
        "description": (
            "⚠️ *Prediksi berdasarkan spawn rate per pet. Spawn bersifat random per server.*\n\n"
            "**🟢 Pet yang kemungkinan SPAWN sekarang:**\n\n"
            + "\n".join(pet_lines)
        ),
        "fields": [
            {
                "name": "📋  Semua Pet GAG2 (Referensi Lengkap)",
                "value": "\n".join(all_pet_ref[:8]),
                "inline": False
            },
            {
                "name": "\u200b",
                "value": "\n".join(all_pet_ref[8:]),
                "inline": False
            },
            {
                "name": "🏆  Best Pets Ranking",
                "value": (
                    "```\n"
                    "S Tier: Unicorn, Ice Serpent, Raccoon, Bee,\n"
                    "        Golden Dragonfly, Black Dragon, Strawberry Sniper\n"
                    "A Tier: Deer, Bunny\n"
                    "B Tier: Owl, Frog, Monkey\n"
                    "C Tier: Robin\n"
                    "```\n"
                    "💡 Saat pet **Legendary/Mythic/Super** spawn → game akan notif di layar!"
                ),
                "inline": False
            }
        ],
        "footer": {"text": "🐾 Pet spawn bisa di-steal sebelum sampai garden — jaga baik-baik!"}
    }

    # ════════════════════════════════════════
    # KIRIM KE DISCORD (2 pesan, 3 embed each)
    # ════════════════════════════════════════
    p1 = {
        "username": "GAG2 Predictor 🌱",
        "content": header,
        "embeds": [embed_status, embed_seeds, embed_sprinklers]
    }
    p2 = {
        "username": "GAG2 Predictor 🌱",
        "content": "",
        "embeds": [embed_weather, embed_fences, embed_pets]
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
    now, wib_str, mins, secs = get_time_info()
    print(f"[{wib_str}] Mengirim prediksi GAG2 untuk KiKo15400...")
    send_to_discord(now, wib_str, mins, secs)

if __name__ == "__main__":
    main()
