"""
GAG2 Discord Webhook Predictor - REAL STOCK + NOW & NEXT + DATA-MINED ODDS
By: KiKo15400

FITUR:
- Cek real stock dari banyak API publik
- NEXT STOCK pakai probabilitas data-mined dari growagarden2wiki.net
- Kirim 2 pesan: NOW STOCK (real/fallback) dan NEXT STOCK (simulasi berbobot)
- Auto @mention saat Super/Mythic/Legendary seed atau cuaca rare muncul
- Simpan last_slot di GitHub Gist supaya tidak double-post
"""

import requests
import random
import os
import json
import hashlib
from datetime import datetime, timezone

# ── SECRETS ──────────────────────────────────────────────────────────────────────
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
if not WEBHOOK_URL:
    raise RuntimeError("WEBHOOK_URL env var belum di-set!")

GIST_ID    = os.environ.get("GIST_ID", "")
GIST_TOKEN = os.environ.get("GIST_TOKEN", "")

OWNER_DISCORD_ID = "506380098044297217"
PING = f"<@{OWNER_DISCORD_ID}>"
PRIVATE_SERVER_LINK = "https://www.roblox.com/share?code=803e2bdb19ceda4a8bb381469a30f8ff&type=Server"

# ── API ENDPOINTS ─────────────────────────────────────────────────────────────────
STOCK_APIS = [
    "https://growagardenapi.vercel.app/api/stock/GetStock",
    "https://growagardenapi.vercel.app/api/GetStock",
    "https://gag-api.vercel.app/api/stock",
    "https://grow-a-garden-stock.vercel.app/api/stock",
]
WEATHER_APIS = [
    "https://growagardenapi.vercel.app/api/weather/GetWeather",
    "https://growagardenapi.vercel.app/api/GetWeather",
    "https://gag-api.vercel.app/api/weather",
    "https://grow-a-garden-stock.vercel.app/api/weather",
]

HIGH_RARITY = {"legendary", "mythic", "super", "prismatic", "divine", "godly"}

RARITY_EMOJI = {
    "common":    "⬜", "uncommon":  "🟩", "rare":      "🟦",
    "epic":      "🟪", "legendary": "🟧", "mythic":    "🟥",
    "super":     "⭐", "prismatic": "🌈", "divine":    "✨", "godly": "🔱",
}

# ── DATA-MINED SEED POOL (dari growagarden2wiki.net/stock/predictions/) ───────────
# Format: (name, rarity, price, restock_chance_0_to_1)
# 5 seed GUARANTEED tiap restock: Carrot, Strawberry, Blueberry, Tomato, Tulip
# Sisanya muncul berdasarkan probabilitas data-mined
SEED_POOL = [
    # name                  rarity       price          chance
    ("Carrot",              "common",    "20 S",        1.0000),   # 100% guaranteed
    ("Strawberry",          "common",    "35 S",        1.0000),   # 100% guaranteed
    ("Blueberry",           "uncommon",  "80 S",        1.0000),   # 100% guaranteed
    ("Tomato",              "uncommon",  "100 S",       1.0000),   # 100% guaranteed
    ("Tulip",               "uncommon",  "120 S",       1.0000),   # 100% guaranteed
    ("Bamboo",              "rare",      "500 S",       0.8000),   # 80%
    ("Apple",               "uncommon",  "300 S",       0.5263),   # 52.63%
    ("Corn",                "rare",      "1,200 S",     0.3500),   # 35%
    ("Cactus",              "rare",      "2,500 S",     0.1667),   # 16.67%
    ("Green Bean",          "epic",      "5,000 S",     0.1500),   # 15%
    ("Pineapple",           "rare",      "3,000 S",     0.1250),   # 12.5%
    ("Mushroom",            "epic",      "8,000 S",     0.0909),   # 9.09%
    ("Banana",              "epic",      "7,500 S",     0.0900),   # 9%
    ("Grape",               "epic",      "10,000 S",    0.0667),   # 6.67%
    ("Mango",               "epic",      "12,000 S",    0.0500),   # 5%
    ("Coconut",             "epic",      "12,000 S",    0.0500),   # 5%
    ("Dragon Fruit",        "legendary", "15,000 S",    0.0400),   # 4%
    ("Acorn",               "legendary", "25,000 S",    0.0294),   # 2.94%
    ("Cherry",              "legendary", "30,000 S",    0.0227),   # 2.27%
    ("Sunflower",           "legendary", "35,000 S",    0.0179),   # 1.79%
    ("Venus Flytrap",       "mythic",    "75,000 S",    0.0143),   # 1.43%
    ("Pomegranate",         "mythic",    "100,000 S",   0.0093),   # 0.93%
    ("Poison Apple",        "mythic",    "150,000 S",   0.0053),   # 0.53%
    ("Venom Spitter",       "mythic",    "200,000 S",   0.0048),   # 0.48%
    ("Moon Bloom",          "super",     "∞ S",         0.0035),   # 0.35%
    ("Dragon's Breath",     "super",     "∞ S",         0.00275),  # 0.275%
]

# ── GEAR POOL (referensi, pakai fallback karena tidak ada odds resmi) ─────────────
FB_GEAR = [
    {"name": "Watering Can",        "rarity": "common",    "price": "FREE",       "qty": 99},
    {"name": "Basic Sprinkler",     "rarity": "common",    "price": "3,000 S",    "qty": 20},
    {"name": "Advanced Sprinkler",  "rarity": "uncommon",  "price": "10,000 S",   "qty": 10},
    {"name": "Godly Sprinkler",     "rarity": "rare",      "price": "50,000 S",   "qty": 5},
    {"name": "Trowel",              "rarity": "common",    "price": "500 S",      "qty": 30},
    {"name": "Recall Wrench",       "rarity": "uncommon",  "price": "8,000 S",    "qty": 10},
    {"name": "Favorite Tool",       "rarity": "rare",      "price": "30,000 S",   "qty": 5},
    {"name": "Master Sprinkler",    "rarity": "legendary", "price": "100,000 S",  "qty": 2},
]

# ── WEATHER POOL ──────────────────────────────────────────────────────────────────
WEATHER_POOL = [
    {"name": "Clear",        "mutation": "None",      "mult": "1x",   "rare": False, "chance": 0.35},
    {"name": "Rain",         "mutation": "Wet",       "mult": "2x",   "rare": False, "chance": 0.25},
    {"name": "Wind",         "mutation": "Windswept", "mult": "5x",   "rare": False, "chance": 0.18},
    {"name": "Fog",          "mutation": "Misty",     "mult": "6x",   "rare": False, "chance": 0.10},
    {"name": "Snow",         "mutation": "Frozen",    "mult": "14x",  "rare": True,  "chance": 0.06},
    {"name": "Thunderstorm", "mutation": "Electric",  "mult": "25x",  "rare": True,  "chance": 0.03},
    {"name": "Blood Moon",   "mutation": "Bloodlit",  "mult": "80x",  "rare": True,  "chance": 0.02},
    {"name": "Rainbow",      "mutation": "Rainbowed", "mult": "100x", "rare": True,  "chance": 0.01},
]

FENCE_PROPS = [
    ("🏠", "Default Fence",    "Common",    "~50%"),
    ("🌲", "Wooden Fence",     "Common",    "~25%"),
    ("🪨", "Stone Fence",      "Uncommon",  "~15%"),
    ("⚙️", "Iron Fence",       "Rare",      "~8%"),
    ("🧱", "Brick Fence",      "Rare",      "~5%"),
    ("💎", "Crystal Fence",    "Epic",      "~3%"),
    ("🥇", "Golden Fence",     "Legendary", "~2%"),
    ("🚀", "Futuristic Fence", "Legendary", "~1%"),
    ("🌈", "Rainbow Fence",    "Rainbow",   "~0.5%"),
]

# ── GIST ──────────────────────────────────────────────────────────────────────────
GIST_FILE = "gag2_state.json"

def gist_read():
    if not GIST_ID or not GIST_TOKEN:
        return {}
    try:
        r = requests.get(
            f"https://api.github.com/gists/{GIST_ID}",
            headers={"Authorization": f"token {GIST_TOKEN}"},
            timeout=8
        )
        if r.status_code == 200:
            content = r.json().get("files", {}).get(GIST_FILE, {}).get("content", "{}")
            return json.loads(content)
    except Exception as e:
        print(f"[Gist] Read error: {e}")
    return {}

def gist_write(data):
    if not GIST_ID or not GIST_TOKEN:
        return
    try:
        requests.patch(
            f"https://api.github.com/gists/{GIST_ID}",
            headers={"Authorization": f"token {GIST_TOKEN}"},
            json={"files": {GIST_FILE: {"content": json.dumps(data)}}},
            timeout=8
        )
    except Exception as e:
        print(f"[Gist] Write error: {e}")

# ── HELPERS ───────────────────────────────────────────────────────────────────────
def ascii_box(label, width=46):
    inner = f"  {label}"
    pad   = max(width - len(inner) - 2, 0)
    line  = f"║{inner}{' ' * pad}║"
    top   = "╔" + "═" * width + "╗"
    bot   = "╚" + "═" * width + "╝"
    return f"```ansi\n\u001b[1;32m{top}\u001b[0m\n\u001b[1;32m{line}\u001b[0m\n\u001b[1;32m{bot}\u001b[0m\n```"

def get_time_info():
    now       = datetime.now(timezone.utc)
    wib_hour  = (now.hour + 7) % 24
    wib_str   = f"{wib_hour:02d}:{now.minute:02d} WIB"
    slot      = int(now.timestamp()) // 300
    cycle_s   = now.timestamp() % 300
    restock_ts = int(now.timestamp() + (300 - cycle_s))
    next_slot  = slot + 1
    next_ts    = restock_ts + 300
    return now, wib_str, slot, next_slot, restock_ts, next_ts

def try_fetch(urls):
    for url in urls:
        try:
            r = requests.get(url, timeout=8)
            if r.status_code == 200:
                data = r.json()
                if data and data != {} and data != []:
                    print(f"[API] OK: {url}")
                    return data
                else:
                    print(f"[API] Empty: {url}")
        except Exception as e:
            print(f"[API] Fail {url}: {e}")
    print("[API] Semua endpoint gagal.")
    return None

# ── WEIGHTED RANDOM SEED GENERATOR (pakai data-mined odds) ───────────────────────
def generate_seeds_weighted(slot):
    """
    Simulasi restock berdasarkan data-mined probability dari growagarden2wiki.net.
    5 seed guaranteed, lalu seed lain muncul sesuai chance masing-masing.
    """
    rng = random.Random(int(hashlib.md5(f"seed_v2_{slot}".encode()).hexdigest(), 16))
    
    guaranteed = []
    optional   = []
    
    for name, rarity, price, chance in SEED_POOL:
        item = {"name": name, "rarity": rarity, "price": price, "qty": "?"}
        if chance >= 1.0:
            guaranteed.append(item)
        else:
            optional.append((item, chance))
    
    # Roll tiap optional seed berdasarkan chance-nya
    appeared = []
    for item, chance in optional:
        if rng.random() < chance:
            appeared.append(item)
    
    result = guaranteed + appeared
    
    # Atur qty berdasarkan rarity
    qty_map = {
        "common": 99, "uncommon": 50, "rare": 20,
        "epic": 10, "legendary": 5, "mythic": 2, "super": 1
    }
    for item in result:
        item["qty"] = qty_map.get(item["rarity"], "?")
    
    return result

def generate_gear_weighted(slot):
    rng = random.Random(int(hashlib.md5(f"gear_v2_{slot}".encode()).hexdigest(), 16))
    result = []
    for g in FB_GEAR:
        # Watering Can selalu ada, sisanya random
        if g["name"] == "Watering Can" or rng.random() < 0.65:
            result.append(g.copy())
    return result if result else FB_GEAR[:3]

def generate_weather_weighted(slot):
    """Pilih cuaca berdasarkan weighted probability."""
    rng = random.Random(int(hashlib.md5(f"wx_v2_{slot}".encode()).hexdigest(), 16))
    names   = [w["name"]   for w in WEATHER_POOL]
    weights = [w["chance"] for w in WEATHER_POOL]
    chosen_name = rng.choices(names, weights=weights, k=1)[0]
    return next(w for w in WEATHER_POOL if w["name"] == chosen_name)

# ── PARSE REAL API ────────────────────────────────────────────────────────────────
def parse_stock(data):
    seeds, gear = [], []
    if data is None:
        return seeds, gear
    raw_seeds = (
        data.get("seedStock") or data.get("seeds") or
        data.get("Seed")      or data.get("SeedStock") or
        data.get("seed_stock") or []
    )
    raw_gear = (
        data.get("gearStock") or data.get("gear") or
        data.get("Gear")      or data.get("GearStock") or
        data.get("gear_stock") or []
    )
    if isinstance(data, list):
        raw_seeds = data

    def norm(item):
        if isinstance(item, str):
            return {"name": item, "rarity": "unknown", "price": "?", "qty": "?"}
        return {
            "name":   item.get("name")    or item.get("Name")   or "Unknown",
            "rarity": (item.get("rarity") or item.get("Rarity") or "unknown").lower(),
            "price":  str(item.get("price") or item.get("Price") or item.get("cost") or "?"),
            "qty":    item.get("quantity") or item.get("qty")   or item.get("stock") or "?",
        }
    parsed_seeds = [norm(i) for i in raw_seeds] if isinstance(raw_seeds, list) else []
    parsed_gear  = [norm(i) for i in raw_gear]  if isinstance(raw_gear,  list) else []
    return parsed_seeds, parsed_gear

def parse_weather(data):
    if data is None:
        return None
    if isinstance(data, list):
        data = data[0] if data else {}
    name     = data.get("name") or data.get("weather") or data.get("Weather") or "Unknown"
    mutation = data.get("mutation") or data.get("Mutation") or "Unknown"
    mult     = data.get("multiplier") or data.get("mult") or data.get("Multiplier") or "1x"
    if isinstance(mult, (int, float)):
        mult = f"{mult}x"
    try:
        rare = float(str(mult).lower().replace("x", "")) >= 10
    except Exception:
        rare = False
    return {"name": name, "mutation": mutation, "mult": str(mult), "rare": rare}

# ── FORMAT ────────────────────────────────────────────────────────────────────────
def fmt_items(items):
    if not items:
        return "*Tidak ada item*"
    lines = []
    for i, item in enumerate(items, 1):
        r     = item.get("rarity", "").lower()
        emoji = RARITY_EMOJI.get(r, "▫️")
        qty   = f" `x{item['qty']}`" if item.get("qty") not in (None, "?", 1) else ""
        lines.append(f"`{i:02d}.` {emoji} **{item['name']}**{qty} — `{item['price']}` *{r.title()}*")
    return "\n".join(lines)

def fmt_weather(w):
    if not w:
        return "*Tidak ada data*"
    return f"**{w['name']}** → {w.get('mutation','?')} ({w.get('mult','?')})"

def send_webhook(payload):
    r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
    print(f"[Webhook] {r.status_code}")
    if r.status_code not in (200, 204):
        print(f"[Webhook] Error: {r.text[:300]}")
        return False
    return True

# ── MAIN ──────────────────────────────────────────────────────────────────────────
def main():
    now, wib_str, slot, next_slot, restock_ts, next_ts = get_time_info()
    print(f"[{wib_str}] Slot={slot} | Next={next_slot}")

    # Cek duplikat
    state     = gist_read()
    last_slot = state.get("last_slot", -1)
    if last_slot == slot:
        print(f"[SKIP] Slot {slot} sudah dipost.")
        return
    print(f"[NEW] {last_slot} → {slot}. Proses...")

    # ── Fetch NOW (real API) ───────────────────────────────────────────────
    stock_data          = try_fetch(STOCK_APIS)
    now_seeds, now_gear = parse_stock(stock_data)
    using_real          = bool(now_seeds or now_gear)

    weather_data = try_fetch(WEATHER_APIS)
    now_weather  = parse_weather(weather_data)

    # Fallback NOW pakai weighted random
    if not now_seeds:
        now_seeds = generate_seeds_weighted(slot)
        print("[FB] NOW seeds - weighted fallback")
    if not now_gear:
        now_gear = generate_gear_weighted(slot)
        print("[FB] NOW gear - weighted fallback")
    if not now_weather:
        now_weather = generate_weather_weighted(slot)
        print("[FB] NOW weather - weighted fallback")

    # ── Generate NEXT (selalu simulasi berbobot) ───────────────────────────
    next_seeds   = generate_seeds_weighted(next_slot)
    next_gear    = generate_gear_weighted(next_slot)
    next_weather = generate_weather_weighted(next_slot)

    data_label = "🟢 DATA REAL" if using_real else "🔮 SIMULASI (API down)"

    # ── Cek high rarity → PING ────────────────────────────────────────────
    now_super    = [s for s in now_seeds if s.get("rarity","").lower() in HIGH_RARITY]
    rare_weather = now_weather and now_weather.get("rare", False)
    need_ping    = bool(now_super) or rare_weather

    if need_ping:
        reasons = []
        if now_super:
            names = ", ".join(f"**{s['name']}** ({s['rarity'].title()})" for s in now_super)
            reasons.append(f"🌟 Seed Langka: {names}")
        if rare_weather:
            reasons.append(f"⚡ Cuaca Rare: **{now_weather['name']}** ({now_weather['mult']})")
        send_webhook({
            "content": (
                f"🚨 {PING} **RESTOCK ALERT!**\n"
                + "\n".join(reasons)
                + f"\n🔗 {PRIVATE_SERVER_LINK}"
            )
        })

    # ══════════════════════════════════════════════════════════════════════
    # PESAN 1: NOW STOCK
    # ══════════════════════════════════════════════════════════════════════
    rare_now = now_weather.get("rare", False) if isinstance(now_weather, dict) else False
    ok1 = send_webhook({
        "username": "GAG2 Live Stock 🌱",
        "embeds": [
            {
                "color": 0x2ecc71,
                "description": (
                    ascii_box("🟢 NOW STOCK — SEDANG AKTIF SEKARANG", 46)
                    + f"\n🕐 **{wib_str}** | {data_label}\n"
                    + f"⏳ **Restock berikutnya:** <t:{restock_ts}:F> • <t:{restock_ts}:R>\n"
                )
            },
            {
                "color": 0xffd700,
                "description": (
                    ascii_box("🌱 SEED SHOP — NOW STOCK", 46)
                    + f"\n{fmt_items(now_seeds)}"
                )
            },
            {
                "color": 0x00bcd4,
                "description": (
                    ascii_box("💧 GEAR SHOP — NOW STOCK", 46)
                    + f"\n{fmt_items(now_gear)}"
                )
            },
            {
                "color": 0xe74c3c if rare_now else 0x5865f2,
                "description": (
                    ascii_box(f"🌦️ CUACA AKTIF{'  🚨 RARE!' if rare_now else ''}", 46)
                    + f"\n{fmt_weather(now_weather)}\n\n"
                    + ("💡 Cuaca RARE! Tanam terbaik sekarang!" if rare_now else "💡 Cuaca normal, farming santai.")
                )
            },
        ]
    })

    # ══════════════════════════════════════════════════════════════════════
    # PESAN 2: NEXT STOCK (prediksi berbobot)
    # ══════════════════════════════════════════════════════════════════════
    next_super  = [s for s in next_seeds if s.get("rarity","").lower() in HIGH_RARITY]
    rare_next   = next_weather.get("rare", False) if isinstance(next_weather, dict) else False

    warn_lines = []
    if next_super:
        names = ", ".join(f"**{s['name']}** ({s['rarity'].title()})" for s in next_super)
        warn_lines.append(f"⚠️ Prediksi seed langka: {names}")
    if rare_next:
        warn_lines.append(f"⚠️ Prediksi cuaca rare: **{next_weather['name']}** ({next_weather['mult']})")
    warn_str = "\n".join(warn_lines) + "\n\n" if warn_lines else ""

    ok2 = send_webhook({
        "username": "GAG2 Live Stock 🌱",
        "embeds": [
            {
                "color": 0x9b59b6,
                "description": (
                    ascii_box("🔮 NEXT STOCK — PREDIKSI SLOT BERIKUTNYA", 46)
                    + f"\n🕐 **{wib_str}** | 🔮 SIMULASI BERBOBOT\n"
                    + f"⏳ **Prediksi restock pada:** <t:{next_ts}:F> • <t:{next_ts}:R>\n\n"
                    + warn_str
                    + "📊 *Berdasarkan data-mined odds dari growagarden2wiki.net*\n"
                    + "📡 *Bukan data real — tunggu pesan NOW STOCK berikutnya!*"
                )
            },
            {
                "color": 0xb8860b,
                "description": (
                    ascii_box("🌱 SEED SHOP — PREDIKSI NEXT", 46)
                    + f"\n{fmt_items(next_seeds)}\n\n"
                    + "⚠️ *Prediksi berdasarkan probabilitas, bukan data real!*"
                )
            },
            {
                "color": 0x006994,
                "description": (
                    ascii_box("💧 GEAR SHOP — PREDIKSI NEXT", 46)
                    + f"\n{fmt_items(next_gear)}\n\n"
                    + "⚠️ *Prediksi berdasarkan probabilitas, bukan data real!*"
                )
            },
            {
                "color": 0x8b0000 if rare_next else 0x483d8b,
                "description": (
                    ascii_box(f"🌦️ PREDIKSI CUACA{'  🚨 RARE!' if rare_next else ''}", 46)
                    + f"\n{fmt_weather(next_weather)}\n\n"
                    + ("💡 Prediksi cuaca RARE! Bersiap!" if rare_next else "💡 Prediksi cuaca normal next slot.")
                    + "\n⚠️ *Prediksi — bukan data real!*"
                )
            },
        ]
    })

    # ══════════════════════════════════════════════════════════════════════
    # PESAN 3: FENCE PROPS
    # ══════════════════════════════════════════════════════════════════════
    fence_lines = "\n".join(
        f"`{i:02d}.` {e} **{n}** — {RARITY_EMOJI.get(r.lower(), '▫️')} {r} ({p})"
        for i, (e, n, r, p) in enumerate(FENCE_PROPS, 1)
    )
    ok3 = send_webhook({
        "username": "GAG2 Live Stock 🌱",
        "embeds": [{
            "color": 0x8b6914,
            "description": (
                ascii_box("🏠 FENCE PROPS (Referensi Crate)", 46)
                + f"\n{fence_lines}\n\n💡 Beli dari **Fence Crate** di Props Shop."
            )
        }]
    })

    if ok1 and ok2 and ok3:
        print(f"✅ [{wib_str}] Sukses! Slot={slot}")
        gist_write({"last_slot": slot})
    else:
        print("❌ Ada pesan gagal.")
        exit(1)

if __name__ == "__main__":
    main()
