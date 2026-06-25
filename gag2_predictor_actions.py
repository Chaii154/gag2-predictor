"""
GAG2 Discord Webhook Predictor - REAL STOCK + SPAM TIAP RESTOCK + TAG USER
Fokus: Super Seeds, Watering Can, All Sprinklers, Cuaca Mutasi, Fence Props, Pet Spawn, Fruit Price
By: KiKo15400

FITUR:
- Fetch stock REAL dari API publik (growagardenapi.vercel.app / fallback)
- Spam pesan BARU tiap restock (bukan edit)
- Auto @mention user saat Super/Mythic/Legendary seed muncul
- Cuaca real dari API (jika tersedia), fallback ke simulasi
"""

import requests
import random
import os
import hashlib
from datetime import datetime, timezone

# ── SECRETS (set di GitHub Actions) ────────────────────────────────────────────
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
if not WEBHOOK_URL:
    raise RuntimeError("WEBHOOK_URL env var belum di-set!")

# Discord User ID kamu — tag otomatis saat Super/Mythic muncul
OWNER_DISCORD_ID = "506380098044297217"
PING = f"<@{OWNER_DISCORD_ID}>"

PRIVATE_SERVER_LINK = "https://www.roblox.com/share?code=803e2bdb19ceda4a8bb381469a30f8ff&type=Server"

# ── API ENDPOINTS (coba satu per satu) ─────────────────────────────────────────
STOCK_APIS = [
    "https://growagardenapi.vercel.app/api/stock/GetStock",
    "https://growagardenapi.vercel.app/api/GetStock",
]
WEATHER_APIS = [
    "https://growagardenapi.vercel.app/api/weather/GetWeather",
    "https://growagardenapi.vercel.app/api/GetWeather",
]

# ── RARITY RANKS (untuk deteksi Super/Mythic) ──────────────────────────────────
HIGH_RARITY = {"legendary", "mythic", "super", "prismatic", "divine", "godly"}
SUPER_RARITY = {"super", "prismatic", "divine", "godly"}

RARITY_EMOJI = {
    "common":    "⬜",
    "uncommon":  "🟩",
    "rare":      "🟦",
    "epic":      "🟪",
    "legendary": "🟧",
    "mythic":    "🟥",
    "super":     "⭐",
    "prismatic": "🌈",
    "divine":    "✨",
    "godly":     "🔱",
}

# ── FALLBACK DATA (jika API down) ───────────────────────────────────────────────
FB_SEEDS = [
    {"name": "Carrot",       "rarity": "common",    "price": "20 S"},
    {"name": "Strawberry",   "rarity": "common",    "price": "35 S"},
    {"name": "Tomato",       "rarity": "uncommon",  "price": "100 S"},
    {"name": "Blueberry",    "rarity": "uncommon",  "price": "200 S"},
    {"name": "Watermelon",   "rarity": "rare",      "price": "2,800 S"},
    {"name": "Pumpkin",      "rarity": "rare",      "price": "3,200 S"},
    {"name": "Dragon Fruit", "rarity": "legendary", "price": "15,000 S"},
    {"name": "Moon Bloom",   "rarity": "super",     "price": "∞ S"},
    {"name": "Beanstalk",    "rarity": "super",     "price": "∞ S"},
]

FB_GEAR = [
    {"name": "Watering Can",       "rarity": "common",    "price": "FREE"},
    {"name": "Common Sprinkler",   "rarity": "common",    "price": "3,000 S"},
    {"name": "Uncommon Sprinkler", "rarity": "uncommon",  "price": "10,000 S"},
    {"name": "Rare Sprinkler",     "rarity": "rare",      "price": "50,000 S"},
    {"name": "Legendary Sprinkler","rarity": "legendary", "price": "100,000 S"},
]

FB_WEATHER = [
    {"name": "Rain",         "mutation": "Wet",       "mult": "2x",  "rare": False},
    {"name": "Wind",         "mutation": "Windswept", "mult": "5x",  "rare": False},
    {"name": "Snow",         "mutation": "Frozen",    "mult": "14x", "rare": True},
    {"name": "Thunderstorm", "mutation": "Electric",  "mult": "25x", "rare": True},
    {"name": "Blood Moon",   "mutation": "Bloodlit",  "mult": "80x", "rare": True},
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

# ── HELPERS ─────────────────────────────────────────────────────────────────────
def ascii_box(label, width=44):
    inner = f"  {label}"
    pad   = max(width - len(inner) - 2, 0)
    line  = f"║{inner}{' ' * pad}║"
    top   = "╔" + "═" * width + "╗"
    bot   = "╚" + "═" * width + "╝"
    return f"```ansi\n\u001b[1;32m{top}\u001b[0m\n\u001b[1;32m{line}\u001b[0m\n\u001b[1;32m{bot}\u001b[0m\n```"

def get_time_info():
    now      = datetime.now(timezone.utc)
    wib_hour = (now.hour + 7) % 24
    wib_str  = f"{wib_hour:02d}:{now.minute:02d} WIB"
    cycle_s  = now.timestamp() % 300
    restock_ts = int(now.timestamp() + (300 - cycle_s))
    return now, wib_str, restock_ts

def try_fetch(urls):
    """Coba fetch satu per satu URL, return JSON atau None."""
    for url in urls:
        try:
            r = requests.get(url, timeout=8)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"[API] {url} gagal: {e}")
    return None

def fallback_seed(now):
    """Deterministik fallback berdasarkan slot waktu."""
    slot = int(now.timestamp()) // 300
    rng  = random.Random(int(hashlib.md5(str(slot).encode()).hexdigest(), 16))
    pool = FB_SEEDS.copy()
    rng.shuffle(pool)
    return pool[:rng.randint(4, 7)]

def fallback_gear(now):
    slot = int(now.timestamp()) // 300
    rng  = random.Random(int(hashlib.md5(f"gear{slot}".encode()).hexdigest(), 16))
    return [g for g in FB_GEAR if rng.random() < 0.7] or FB_GEAR[:3]

def fallback_weather(now):
    slot = int(now.timestamp()) // 300
    rng  = random.Random(int(hashlib.md5(f"wx{slot}".encode()).hexdigest(), 16))
    common = [w for w in FB_WEATHER if not w["rare"]]
    rare   = [w for w in FB_WEATHER if w["rare"]]
    return rng.choice(rare) if rng.random() < 0.20 else rng.choice(common)

# ── PARSE API RESPONSE ───────────────────────────────────────────────────────────
def parse_stock(data):
    """
    Normalisasi respons API ke list of dicts [{name, rarity, price, qty}].
    API format bervariasi — kita handle beberapa kemungkinan.
    """
    seeds, gear = [], []
    if data is None:
        return seeds, gear

    # Coba format blaircdonald / Just3itx style
    raw_seeds = (
        data.get("seedStock") or
        data.get("seeds") or
        data.get("Seed") or
        []
    )
    raw_gear = (
        data.get("gearStock") or
        data.get("gear") or
        data.get("Gear") or
        []
    )

    # Kalau top-level list
    if isinstance(data, list):
        raw_seeds = data

    def norm(item):
        if isinstance(item, str):
            return {"name": item, "rarity": "unknown", "price": "?", "qty": 1}
        name   = item.get("name") or item.get("Name") or item.get("itemName") or "Unknown"
        rarity = (item.get("rarity") or item.get("Rarity") or "unknown").lower()
        price  = item.get("price") or item.get("Price") or item.get("cost") or "?"
        qty    = item.get("quantity") or item.get("qty") or item.get("stock") or 1
        return {"name": name, "rarity": rarity, "price": str(price), "qty": qty}

    seeds = [norm(i) for i in raw_seeds]
    gear  = [norm(i) for i in raw_gear]
    return seeds, gear

def parse_weather(data):
    """Normalisasi weather API response."""
    if data is None:
        return None
    if isinstance(data, list) and data:
        data = data[0]
    name     = data.get("name") or data.get("weather") or data.get("Weather") or "Unknown"
    mutation = data.get("mutation") or data.get("Mutation") or data.get("effect") or "Unknown"
    mult     = data.get("multiplier") or data.get("mult") or data.get("Multiplier") or "1x"
    if isinstance(mult, (int, float)):
        mult = f"{mult}x"
    rare = str(mult).replace("x", "").replace("X", "") not in ("1", "2", "5")
    return {"name": name, "mutation": mutation, "mult": str(mult), "rare": rare}

# ── FORMAT ───────────────────────────────────────────────────────────────────────
def fmt_items(items, show_qty=True):
    if not items:
        return "*Tidak ada item tersedia*"
    lines = []
    for i, item in enumerate(items, 1):
        r = item.get("rarity", "").lower()
        emoji = RARITY_EMOJI.get(r, "▫️")
        qty   = f" x{item['qty']}" if show_qty and item.get("qty") else ""
        lines.append(
            f"`{i:02d}.` {emoji} **{item['name']}**{qty} — `{item['price']}`  *{r.title()}*"
        )
    return "\n".join(lines)

def check_super_seeds(seeds):
    """Return list nama seed yang tergolong Super/Mythic/Legendary ke atas."""
    found = [s for s in seeds if s.get("rarity", "").lower() in HIGH_RARITY]
    return found

def check_rare_weather(weather):
    return weather and weather.get("rare", False)

# ── BUILD & SEND ─────────────────────────────────────────────────────────────────
def send_to_discord(now, wib_str, restock_ts):

    # ── Fetch data real ──────────────────────────────────────────────────────
    print("[API] Fetching stock...")
    stock_data   = try_fetch(STOCK_APIS)
    seeds, gear  = parse_stock(stock_data)
    using_real   = stock_data is not None

    print("[API] Fetching weather...")
    weather_data = try_fetch(WEATHER_APIS)
    weather      = parse_weather(weather_data)

    # ── Fallback jika API down ───────────────────────────────────────────────
    if not seeds:
        seeds = fallback_seed(now)
        print("[FALLBACK] Pakai seed simulasi")
    if not gear:
        gear  = fallback_gear(now)
        print("[FALLBACK] Pakai gear simulasi")
    if not weather:
        weather = fallback_weather(now)
        print("[FALLBACK] Pakai weather simulasi")

    # ── Cek apakah perlu ping ────────────────────────────────────────────────
    super_seeds   = check_super_seeds(seeds)
    rare_weather  = check_rare_weather(weather)
    need_ping     = bool(super_seeds) or rare_weather

    countdown  = f"<t:{restock_ts}:F>  •  <t:{restock_ts}:R>"
    data_label = "🟢 REAL" if using_real else "🔮 SIMULASI"

    # ── Ping message (kirim dulu jika ada super seed / cuaca rare) ───────────
    if need_ping:
        reasons = []
        if super_seeds:
            names = ", ".join(f"**{s['name']}**" for s in super_seeds)
            reasons.append(f"🌟 Super/Legendary Seed: {names}")
        if rare_weather:
            reasons.append(f"⚡ Cuaca Rare: **{weather['name']}** ({weather['mult']})")
        ping_payload = {
            "content": (
                f"{PING} 🚨 **ALERT RESTOCK!**\n"
                + "\n".join(reasons)
                + f"\nPrivate server: {PRIVATE_SERVER_LINK}"
            )
        }
        r = requests.post(WEBHOOK_URL, json=ping_payload, timeout=10)
        print(f"[PING] Status: {r.status_code}")

    # ═══════════════════════════════════════════════════════════════════════════
    # EMBED 1: HEADER + SEED + GEAR + CUACA
    # ═══════════════════════════════════════════════════════════════════════════
    seed_lines = fmt_items(seeds)
    gear_lines = fmt_items(gear)

    w_rare_tag = " 🚨RARE" if rare_weather else ""
    w_line = (
        f"{weather.get('emoji', '🌤️')} **{weather['name']}** → "
        f"{weather['mutation']} ({weather['mult']})"
        if weather else "*Tidak ada data cuaca*"
    )

    embed1 = {
        "color": 0x2ecc71,
        "description": (
            ascii_box("🌿 GAG2 LIVE STOCK — KiKo15400")
            + f"\n🕐 **{wib_str}** | Data: {data_label}\n"
            + f"⏳ **Restock berikutnya:** {countdown}\n"
            + f"📡 *Setiap restock = pesan baru dikirim otomatis!*"
        )
    }

    embed_seeds = {
        "color": 0xffd700,
        "description": (
            ascii_box("🌱 SEED SHOP — STOCK SEKARANG")
            + f"\n{seed_lines}"
        )
    }

    embed_gear = {
        "color": 0x00bcd4,
        "description": (
            ascii_box("💧 GEAR SHOP — STOCK SEKARANG")
            + f"\n{gear_lines}"
        )
    }

    embed_weather = {
        "color": 0x5865f2,
        "description": (
            ascii_box(f"🌦️ CUACA AKTIF{w_rare_tag}")
            + f"\n{w_line}\n\n"
            + (f"💡 Tanam yang terbaik sekarang!" if rare_weather else "💡 Cuaca normal, farming biasa.")
        )
    }

    # ═══════════════════════════════════════════════════════════════════════════
    # EMBED 2: FENCE PROPS
    # ═══════════════════════════════════════════════════════════════════════════
    fence_lines = "\n".join(
        f"`{i:02d}.` {e} **{name}** — {RARITY_EMOJI.get(r.lower(), '▫️')} {r} ({pct})"
        for i, (e, name, r, pct) in enumerate(FENCE_PROPS, 1)
    )
    embed_fence = {
        "color": 0x8b6914,
        "description": (
            ascii_box("🏠 FENCE PROPS (Referensi Crate)")
            + f"\n{fence_lines}\n\n"
            + "💡 Beli dari **Fence Crate** di Props Shop. Kosmetik saja."
        )
    }

    # ═══════════════════════════════════════════════════════════════════════════
    # KIRIM
    # ═══════════════════════════════════════════════════════════════════════════
    p1 = {
        "username": "GAG2 Live Stock 🌱",
        "embeds":   [embed1, embed_seeds, embed_gear, embed_weather]
    }
    p2 = {
        "username": "GAG2 Live Stock 🌱",
        "embeds":   [embed_fence]
    }

    r1 = requests.post(WEBHOOK_URL, json=p1, timeout=10)
    r2 = requests.post(WEBHOOK_URL, json=p2, timeout=10)

    ok1 = r1.status_code in (200, 204)
    ok2 = r2.status_code in (200, 204)

    if ok1 and ok2:
        print(f"✅ [{wib_str}] Sukses! Data: {data_label}")
    else:
        print(f"❌ [{wib_str}] Error: {r1.status_code} / {r2.status_code}")
        if not ok1: print(r1.text[:300])
        if not ok2: print(r2.text[:300])
        exit(1)


def main():
    now, wib_str, restock_ts = get_time_info()
    print(f"[{wib_str}] GAG2 Predictor mulai untuk KiKo15400...")
    send_to_discord(now, wib_str, restock_ts)


if __name__ == "__main__":
    main()
