"""
GAG2 (Grow a Garden 2) Discord Webhook Predictor
Versi GitHub Actions — kirim 1x per run, dipanggil setiap 5 menit oleh cron
"""

import requests
import random
import os
from datetime import datetime, timezone

WEBHOOK_URL = os.environ.get(
    "WEBHOOK_URL",
    "https://discord.com/api/webhooks/1455445496989745328/BB_6EjQuuRAX_IvfBEcZfpIf66R46GTPZMOJndMvfzoylNZW-K_f98WEhNdI3AXWY8rq"
)

SEEDS = {
    "🟢 COMMON": [
        {"name": "Carrot",          "price": "10",       "chance": "100%"},
        {"name": "Strawberry",      "price": "50",       "chance": "100%"},
        {"name": "Blueberry",       "price": "100",      "chance": "100%"},
        {"name": "Orange Tulip",    "price": "120",      "chance": "90%"},
    ],
    "🔵 UNCOMMON": [
        {"name": "Tomato",          "price": "300",      "chance": "75%"},
        {"name": "Corn",            "price": "500",      "chance": "70%"},
        {"name": "Daffodil",        "price": "600",      "chance": "65%"},
        {"name": "Watermelon",      "price": "800",      "chance": "60%"},
    ],
    "🟣 RARE": [
        {"name": "Pumpkin",         "price": "2,500",    "chance": "40%"},
        {"name": "Apple",           "price": "3,000",    "chance": "38%"},
        {"name": "Bamboo",          "price": "4,000",    "chance": "35%"},
        {"name": "Coconut",         "price": "5,000",    "chance": "30%"},
        {"name": "Cactus",          "price": "5,500",    "chance": "28%"},
        {"name": "Mushroom",        "price": "6,000",    "chance": "25%"},
    ],
    "🟡 EPIC": [
        {"name": "Grape",           "price": "10,000",   "chance": "18%"},
        {"name": "Mango",           "price": "12,000",   "chance": "15%"},
        {"name": "Pepper",          "price": "15,000",   "chance": "12%"},
        {"name": "Cacao",           "price": "18,000",   "chance": "10%"},
        {"name": "Bonsai",          "price": "20,000",   "chance": "8%"},
    ],
    "🟠 LEGENDARY": [
        {"name": "Dragon Fruit",    "price": "120,000",  "chance": "5%"},
        {"name": "Acorn",           "price": "150,000",  "chance": "4%"},
        {"name": "Cherry",          "price": "175,000",  "chance": "3.5%"},
        {"name": "Sunflower",       "price": "200,000",  "chance": "3%"},
        {"name": "Pineapple",       "price": "250,000",  "chance": "2.5%"},
    ],
    "🔴 MYTHIC": [
        {"name": "Rainbow Seed",    "price": "EVENT",    "chance": "1.5%"},
        {"name": "Gold Seed",       "price": "EVENT",    "chance": "1.2%"},
        {"name": "Ghost Pepper",    "price": "PACK",     "chance": "1%"},
        {"name": "Lychee",          "price": "750,000",  "chance": "0.8%"},
    ],
    "⭐ SUPER": [
        {"name": "Moon Bloom",      "price": "∞",        "chance": "0.35%"},
        {"name": "Beanstalk",       "price": "∞",        "chance": "0.35%"},
        {"name": "Poison Apple",    "price": "∞",        "chance": "0.30%"},
        {"name": "Dragon's Breath", "price": "1,499 R",  "chance": "0.27%"},
    ],
}

GEAR = {
    "💧 SPRINKLERS": [
        {"name": "Common Sprinkler",    "price": "3,000",     "rarity": "Common"},
        {"name": "Uncommon Sprinkler",  "price": "10,000",    "rarity": "Uncommon"},
        {"name": "Rare Sprinkler",      "price": "50,000",    "rarity": "Rare"},
        {"name": "Legendary Sprinkler", "price": "100,000",   "rarity": "Legendary"},
        {"name": "Super Sprinkler",     "price": "1,000,000", "rarity": "Super"},
        {"name": "Rainbow Sprinkler",   "price": "∞",         "rarity": "Rainbow"},
    ],
    "🔧 TOOLS": [
        {"name": "Watering Can",        "price": "FREE",      "rarity": "Common"},
        {"name": "Trowel",              "price": "5,000",     "rarity": "Uncommon"},
        {"name": "Shovel",              "price": "15,000",    "rarity": "Rare"},
        {"name": "Basic Pot",           "price": "300,000",   "rarity": "Epic"},
        {"name": "Wheelbarrow",         "price": "500,000",   "rarity": "Legendary"},
    ],
    "⚔️ WEAPONS/DEFENSE": [
        {"name": "Gnome",               "price": "25,000",    "rarity": "Rare"},
        {"name": "Freeze Ray",          "price": "80,000",    "rarity": "Epic"},
        {"name": "Flashbang",           "price": "60,000",    "rarity": "Rare"},
    ],
    "🍄 CONSUMABLES": [
        {"name": "Jump Mushroom",       "price": "2,000",     "rarity": "Common"},
        {"name": "Shrink Mushroom",     "price": "3,000",     "rarity": "Uncommon"},
        {"name": "Speed Mushroom",      "price": "4,000",     "rarity": "Uncommon"},
    ],
}

WEATHER_EVENTS = [
    {"name": "☀️ Clear Sky",       "mutation": "None",       "multiplier": "1x",  "rare": False},
    {"name": "🌧️ Rain",           "mutation": "Wet",        "multiplier": "2x",  "rare": False},
    {"name": "⛈️ Thunderstorm",    "mutation": "Electric",   "multiplier": "25x", "rare": True},
    {"name": "🌈 Rainbow",         "mutation": "Rainbow",    "multiplier": "10x", "rare": True},
    {"name": "🩸 Blood Moon",      "mutation": "Bloodlit",   "multiplier": "80x", "rare": True},
    {"name": "❄️ Snow",            "mutation": "Frozen",     "multiplier": "14x", "rare": True},
    {"name": "🌙 Night",           "mutation": "Night",      "multiplier": "3x",  "rare": False},
    {"name": "🌟 Starfall",        "mutation": "Starstruck", "multiplier": "50x", "rare": True},
    {"name": "☁️ Cloudy",          "mutation": "None",       "multiplier": "1x",  "rare": False},
    {"name": "💛 Gold Moon",       "mutation": "Gold",       "multiplier": "15x", "rare": True},
    {"name": "🌈🌙 Rainbow Moon",  "mutation": "Rainbow",    "multiplier": "40x", "rare": True},
    {"name": "🌬️ Wind",           "mutation": "Windswept",  "multiplier": "5x",  "rare": False},
]

MOON_EVENTS = [
    {"name": "🌑 New Moon",       "note": "Normal night"},
    {"name": "🌕 Full Moon",      "note": "Pets lebih aktif"},
    {"name": "💛 Gold Moon",      "note": "Gold Seeds spawn di map!"},
    {"name": "🌈 Rainbow Moon",   "note": "Rainbow Seeds spawn di map!"},
    {"name": "🩸 Blood Moon",     "note": "Bloodlit mutation 80x — tertinggi di game!"},
]

def get_server_time():
    now = datetime.now(timezone.utc)
    cycle_seconds = now.timestamp() % 300
    time_to_next = 300 - cycle_seconds
    return now, time_to_next

def predict_stock():
    predicted = {}
    for rarity, seeds in SEEDS.items():
        available = []
        for seed in seeds:
            raw = seed["chance"].replace("%", "")
            try:
                chance = float(raw)
            except ValueError:
                continue
            if random.random() * 100 < min(chance, 100):
                available.append(seed)
        if available:
            predicted[rarity] = available
    return predicted

def predict_gear():
    predicted = {}
    for category, items in GEAR.items():
        count = random.randint(1, min(3, len(items)))
        predicted[category] = random.sample(items, count)
    return predicted

def predict_weather():
    common = [w for w in WEATHER_EVENTS if not w["rare"]]
    rare   = [w for w in WEATHER_EVENTS if w["rare"]]
    upcoming = [random.choice(common)]
    upcoming.append(random.choice(rare) if random.random() < 0.25 else random.choice(common))
    upcoming.append(random.choice(rare) if random.random() < 0.15 else random.choice(common))
    return upcoming

def predict_moon():
    if random.random() < 0.12:
        return random.choice(MOON_EVENTS[2:])
    return random.choice(MOON_EVENTS[:2])

def build_embeds(now, time_to_next):
    mins = int(time_to_next // 60)
    secs = int(time_to_next % 60)
    predicted_seeds  = predict_stock()
    predicted_gear   = predict_gear()
    upcoming_weather = predict_weather()
    moon             = predict_moon()

    seed_fields = []
    for rarity, seeds in predicted_seeds.items():
        lines = [f"**{s['name']}** — `{s['price']} S` ┃ Chance: `{s['chance']}`" for s in seeds]
        seed_fields.append({"name": rarity, "value": "\n".join(lines), "inline": False})

    embed_seeds = {
        "title": "🌱 PREDIKSI NEXT STOCK — SEED SHOP",
        "description": (
            f"⏱️ **Next Restock:** `{mins}m {secs}s`\n"
            f"🕐 Server Time: `{now.strftime('%H:%M:%S UTC')}`\n"
            f"🔄 Restock global setiap **5 menit**\n"
            "─────────────────────────────"
        ),
        "color": 0x57f287,
        "fields": seed_fields,
        "footer": {"text": "GAG2 Predictor • Probabilitas berdasarkan data-mined game files"},
    }

    gear_fields = []
    for category, items in predicted_gear.items():
        lines = [f"**{i['name']}** — `{i['price']} S` ┃ [{i['rarity']}]" for i in items]
        gear_fields.append({"name": category, "value": "\n".join(lines), "inline": False})

    embed_gear = {
        "title": "⚙️ PREDIKSI NEXT STOCK — GEAR SHOP (George)",
        "description": (
            f"⏱️ **Next Restock:** `{mins}m {secs}s`\n"
            "📦 Gear shop restock bersamaan dengan seed shop\n"
            "─────────────────────────────"
        ),
        "color": 0xfee75c,
        "fields": gear_fields,
        "footer": {"text": "GAG2 Predictor • George's Gear Shop"},
    }

    labels = ["🔮 SEKARANG / SOON", "🌤️ BERIKUTNYA", "🌥️ SETELAH ITU"]
    weather_fields = []
    for i, w in enumerate(upcoming_weather[:3]):
        alert = " 🚨 **RARE!**" if w["rare"] else ""
        weather_fields.append({
            "name": labels[i],
            "value": f"{w['name']}{alert}\nMutation: `{w['mutation']}` ┃ Multiplier: `{w['multiplier']}`",
            "inline": True,
        })

    embed_weather = {
        "title": "🌦️ PREDIKSI CUACA — Weather Schedule",
        "description": (
            "Cuaca **global** — semua server sama!\n"
            "Cuaca langka = **tanam crop terbaik kamu segera!**\n"
            "─────────────────────────────"
        ),
        "color": 0x5865f2,
        "fields": weather_fields,
        "footer": {"text": "GAG2 Predictor • Weather Events"},
    }

    is_rare = moon in MOON_EVENTS[2:]
    alert_text = "\n\n🚨 **EVENT LANGKA! Siapkan garden sekarang!**" if is_rare else ""
    embed_moon = {
        "title": "🌙 PREDIKSI MOON EVENT",
        "description": (
            f"**{moon['name']}**\n"
            f"📝 {moon['note']}{alert_text}\n"
            "─────────────────────────────\n"
            "💡 Rainbow Moon & Gold Moon → Special Seeds spawn di map!\n"
            "💡 Blood Moon → Bloodlit 80x — mutasi tertinggi di game!"
        ),
        "color": 0xed4245 if is_rare else 0x99aab5,
        "footer": {"text": "GAG2 Predictor • Moon Events"},
    }

    tips = [
        "🌟 Tanam **Moon Bloom/Beanstalk** sebelum Blood Moon untuk 80x!",
        "💰 **Dragon Fruit** Legendary paling worth untuk pemula",
        "🌈 Saat **Rainbow Moon** → cepat ambil Rainbow Seeds di map!",
        "⚡ **Thunderstorm** = Electric 25x — jangan lewatkan!",
        "🍄 **Speed Mushroom** berguna untuk racing rare seeds saat restock",
        "🔒 Pasang **Gnome + Freeze Ray** untuk proteksi dari pencuri",
        "💧 **Super Sprinkler** wajib beli untuk endgame farming",
        "👀 **Moon Bloom & Dragon's Breath** terjual habis dalam detik!",
        "🪙 Gunakan **Gold Seed** pada crop Mythic/Super untuk nilai maksimal",
        "📦 **Ghost Pepper Pack** hanya kalau ekonomi sudah stabil (chance 1%)",
    ]
    random.shuffle(tips)
    embed_tips = {
        "title": "💡 TIPS & STRATEGI GAG2",
        "description": "\n".join(tips[:5]),
        "color": 0x2ecc71,
        "footer": {"text": "GAG2 Predictor • Auto-update setiap 5 menit via GitHub Actions"},
    }

    return [embed_seeds, embed_gear, embed_weather, embed_moon, embed_tips]

def main():
    now, time_to_next = get_server_time()
    print(f"[{now.strftime('%H:%M:%S UTC')}] Sending GAG2 prediction...")
    embeds = build_embeds(now, time_to_next)
    payload = {
        "username": "GAG2 Predictor 🌱",
        "content": (
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🌿 **GAG2 STOCK & WEATHER PREDICTOR** — Auto Update\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ),
        "embeds": embeds,
    }
    resp = requests.post(WEBHOOK_URL, json=payload)
    if resp.status_code in (200, 204):
        print("✅ Berhasil dikirim ke Discord!")
    else:
        print(f"❌ Gagal: HTTP {resp.status_code} — {resp.text}")
        exit(1)

if __name__ == "__main__":
    main()
