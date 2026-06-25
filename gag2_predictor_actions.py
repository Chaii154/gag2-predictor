"""
GAG2 Discord Webhook Predictor - REAL STOCK + SPAM TIAP RESTOCK + TAG USER
By: KiKo15400

FITUR:
- Cek real stock dari API publik
- Kirim pesan baru HANYA saat restock baru terdeteksi (bukan tiap 2 menit terus)
- Auto @mention saat Super/Mythic/Legendary seed atau cuaca rare muncul
- Simpan "last restock slot" di GitHub Gist supaya tidak double-post
"""

import requests
import random
import os
import json
import hashlib
from datetime import datetime, timezone

# ── SECRETS ─────────────────────────────────────────────────────────────────────
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
if not WEBHOOK_URL:
    raise RuntimeError("WEBHOOK_URL env var belum di-set!")

GIST_ID    = os.environ.get("GIST_ID", "")
GIST_TOKEN = os.environ.get("GIST_TOKEN", "")

OWNER_DISCORD_ID = "506380098044297217"
PING = f"<@{OWNER_DISCORD_ID}>"

PRIVATE_SERVER_LINK = "https://www.roblox.com/share?code=803e2bdb19ceda4a8bb381469a30f8ff&type=Server"

# ── API ENDPOINTS ────────────────────────────────────────────────────────────────
STOCK_APIS = [
    "https://growagardenapi.vercel.app/api/stock/GetStock",
    "https://growagardenapi.vercel.app/api/GetStock",
]
WEATHER_APIS = [
    "https://growagardenapi.vercel.app/api/weather/GetWeather",
    "https://growagardenapi.vercel.app/api/GetWeather",
]

HIGH_RARITY  = {"legendary", "mythic", "super", "prismatic", "divine", "godly"}

RARITY_EMOJI = {
    "common":    "⬜", "uncommon": "🟩", "rare":      "🟦",
    "epic":      "🟪", "legendary":"🟧", "mythic":    "🟥",
    "super":     "⭐", "prismatic":"🌈", "divine":    "✨", "godly": "🔱",
}

# ── FALLBACK DATA ────────────────────────────────────────────────────────────────
FB_SEEDS = [
    {"name": "Carrot",        "rarity": "common",    "price": "20 S",       "qty": 99},
    {"name": "Strawberry",    "rarity": "common",    "price": "35 S",       "qty": 99},
    {"name": "Tomato",        "rarity": "uncommon",  "price": "100 S",      "qty": 50},
    {"name": "Blueberry",     "rarity": "uncommon",  "price": "200 S",      "qty": 50},
    {"name": "Watermelon",    "rarity": "rare",      "price": "2,800 S",    "qty": 20},
    {"name": "Pumpkin",       "rarity": "rare",      "price": "3,200 S",    "qty": 20},
    {"name": "Dragon Fruit",  "rarity": "legendary", "price": "15,000 S",   "qty": 5},
    {"name": "Moon Bloom",    "rarity": "super",     "price": "∞ S",        "qty": 1},
    {"name": "Beanstalk",     "rarity": "super",     "price": "∞ S",        "qty": 1},
]
FB_GEAR = [
    {"name": "Watering Can",        "rarity": "common",    "price": "FREE",       "qty": 99},
    {"name": "Common Sprinkler",    "rarity": "common",    "price": "3,000 S",    "qty": 20},
    {"name": "Uncommon Sprinkler",  "rarity": "uncommon",  "price": "10,000 S",   "qty": 10},
    {"name": "Rare Sprinkler",      "rarity": "rare",      "price": "50,000 S",   "qty": 5},
    {"name": "Legendary Sprinkler", "rarity": "legendary", "price": "100,000 S",  "qty": 2},
]
FB_WEATHER = [
    {"name": "Rain",         "mutation": "Wet",       "mult": "2x",  "rare": False},
    {"name": "Wind",         "mutation": "Windswept", "mult": "5x",  "rare": False},
    {"name": "Snow",         "mutation": "Frozen",    "mult": "14x", "rare": True},
    {"name": "Thunderstorm", "mutation": "Electric",  "mult": "25x", "rare": True},
    {"name": "Blood Moon",   "mutation": "Bloodlit",  "mult": "80x", "rare": True},
]
FENCE_PROPS = [
    ("🏠","Default Fence",    "Common",    "~50%"),
    ("🌲","Wooden Fence",     "Common",    "~25%"),
    ("🪨","Stone Fence",      "Uncommon",  "~15%"),
    ("⚙️","Iron Fence",       "Rare",      "~8%"),
    ("🧱","Brick Fence",      "Rare",      "~5%"),
    ("💎","Crystal Fence",    "Epic",      "~3%"),
    ("🥇","Golden Fence",     "Legendary", "~2%"),
    ("🚀","Futuristic Fence", "Legendary", "~1%"),
    ("🌈","Rainbow Fence",    "Rainbow",   "~0.5%"),
]

# ── GIST: simpan last_slot ───────────────────────────────────────────────────────
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

# ── HELPERS ──────────────────────────────────────────────────────────────────────
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
    # slot 5 menit: 0, 5, 10, 15, ...
    slot       = int(now.timestamp()) // 300
    cycle_s    = now.timestamp() % 300
    restock_ts = int(now.timestamp() + (300 - cycle_s))
    return now, wib_str, slot, restock_ts

def try_fetch(urls):
    for url in urls:
        try:
            r = requests.get(url, timeout=8)
            if r.status_code == 200:
                print(f"[API] OK: {url}")
                return r.json()
        except Exception as e:
            print(f"[API] Fail {url}: {e}")
    return None

# ── FALLBACK DETERMINISTIK ───────────────────────────────────────────────────────
def fb_seeds(slot):
    rng = random.Random(int(hashlib.md5(f"seed{slot}".encode()).hexdigest(), 16))
    pool = FB_SEEDS.copy(); rng.shuffle(pool)
    return pool[:rng.randint(4, 7)]

def fb_gear(slot):
    rng = random.Random(int(hashlib.md5(f"gear{slot}".encode()).hexdigest(), 16))
    return [g for g in FB_GEAR if rng.random() < 0.7] or FB_GEAR[:3]

def fb_weather(slot):
    rng    = random.Random(int(hashlib.md5(f"wx{slot}".encode()).hexdigest(), 16))
    common = [w for w in FB_WEATHER if not w["rare"]]
    rare   = [w for w in FB_WEATHER if w["rare"]]
    return rng.choice(rare) if rng.random() < 0.20 else rng.choice(common)

# ── PARSE API ────────────────────────────────────────────────────────────────────
def parse_stock(data):
    seeds, gear = [], []
    if data is None:
        return seeds, gear
    raw_seeds = data.get("seedStock") or data.get("seeds") or data.get("Seed") or []
    raw_gear  = data.get("gearStock") or data.get("gear")  or data.get("Gear")  or []
    if isinstance(data, list):
        raw_seeds = data

    def norm(item):
        if isinstance(item, str):
            return {"name": item, "rarity": "unknown", "price": "?", "qty": "?"}
        return {
            "name":   item.get("name")     or item.get("Name")     or item.get("itemName") or "Unknown",
            "rarity": (item.get("rarity")  or item.get("Rarity")   or "unknown").lower(),
            "price":  str(item.get("price") or item.get("Price")   or item.get("cost") or "?"),
            "qty":    item.get("quantity")  or item.get("qty")     or item.get("stock") or "?",
        }
    return [norm(i) for i in raw_seeds], [norm(i) for i in raw_gear]

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
        rare = float(str(mult).lower().replace("x","")) >= 10
    except Exception:
        rare = False
    return {"name": name, "mutation": mutation, "mult": str(mult), "rare": rare}

# ── FORMAT ───────────────────────────────────────────────────────────────────────
def fmt_items(items):
    if not items:
        return "*Tidak ada item*"
    lines = []
    for i, item in enumerate(items, 1):
        r     = item.get("rarity","").lower()
        emoji = RARITY_EMOJI.get(r, "▫️")
        qty   = f" `x{item['qty']}`" if item.get("qty") not in (None, "?", 1) else ""
        lines.append(f"`{i:02d}.` {emoji} **{item['name']}**{qty} — `{item['price']}` *{r.title()}*")
    return "\n".join(lines)

# ── MAIN ─────────────────────────────────────────────────────────────────────────
def main():
    now, wib_str, slot, restock_ts = get_time_info()
    print(f"[{wib_str}] Slot={slot} | GAG2 Predictor start")

    # ── Cek apakah slot ini sudah pernah dipost ──────────────────────────────
    state = gist_read()
    last_slot = state.get("last_slot", -1)

    if last_slot == slot:
        print(f"[SKIP] Slot {slot} sudah dipost sebelumnya. Skip.")
        return  # Tidak kirim duplikat

    print(f"[NEW] Slot baru! Last={last_slot} → {slot}. Kirim sekarang...")

    # ── Fetch data ───────────────────────────────────────────────────────────
    stock_data      = try_fetch(STOCK_APIS)
    seeds, gear     = parse_stock(stock_data)
    using_real      = bool(seeds or gear)

    weather_data    = try_fetch(WEATHER_APIS)
    weather         = parse_weather(weather_data)

    if not seeds:
        seeds = fb_seeds(slot); print("[FB] Seed fallback")
    if not gear:
        gear  = fb_gear(slot);  print("[FB] Gear fallback")
    if not weather:
        weather = fb_weather(slot); print("[FB] Weather fallback")

    data_label  = "🟢 DATA REAL" if using_real else "🔮 SIMULASI (API down)"
    countdown   = f"<t:{restock_ts}:F>  •  <t:{restock_ts}:R>"

    # ── Cek high rarity ──────────────────────────────────────────────────────
    super_seeds  = [s for s in seeds if s.get("rarity","").lower() in HIGH_RARITY]
    rare_weather = weather and weather.get("rare", False)
    need_ping    = bool(super_seeds) or rare_weather

    # ── PING dulu kalau ada super seed / cuaca rare ──────────────────────────
    if need_ping:
        reasons = []
        if super_seeds:
            names = ", ".join(f"**{s['name']}** ({s['rarity'].title()})" for s in super_seeds)
            reasons.append(f"🌟 Seed Langka: {names}")
        if rare_weather:
            reasons.append(f"⚡ Cuaca Rare: **{weather['name']}** ({weather['mult']})")
        ping_msg = {
            "content": (
                f"🚨 {PING} **RESTOCK ALERT!**\n"
                + "\n".join(reasons)
                + f"\n🔗 Private server: {PRIVATE_SERVER_LINK}"
            )
        }
        r = requests.post(WEBHOOK_URL, json=ping_msg, timeout=10)
        print(f"[PING] {r.status_code}")

    # ── Build embeds ─────────────────────────────────────────────────────────
    w_rare_tag = " 🚨 RARE!" if rare_weather else ""
    w_line = (
        f"**{weather['name']}** → {weather['mutation']} ({weather['mult']})"
        if weather else "*Tidak ada data*"
    )

    embed_header = {
        "color": 0x2ecc71,
        "description": (
            ascii_box("🌿 GAG2 LIVE STOCK — KiKo15400")
            + f"\n🕐 **{wib_str}** | {data_label}\n"
            + f"⏳ **Restock berikutnya:** {countdown}\n"
            + f"📡 *Pesan baru dikirim otomatis tiap restock!*"
        )
    }
    embed_seeds = {
        "color": 0xffd700,
        "description": (
            ascii_box("🌱 SEED SHOP — STOCK SEKARANG")
            + f"\n{fmt_items(seeds)}"
        )
    }
    embed_gear = {
        "color": 0x00bcd4,
        "description": (
            ascii_box("💧 GEAR SHOP — STOCK SEKARANG")
            + f"\n{fmt_items(gear)}"
        )
    }
    embed_weather = {
        "color": 0xe74c3c if rare_weather else 0x5865f2,
        "description": (
            ascii_box(f"🌦️ CUACA AKTIF{w_rare_tag}")
            + f"\n{w_line}\n\n"
            + ("💡 Cuaca RARE! Tanam terbaik sekarang!" if rare_weather else "💡 Cuaca normal, farming santai.")
        )
    }
    fence_lines = "\n".join(
        f"`{i:02d}.` {e} **{n}** — {RARITY_EMOJI.get(r.lower(),'▫️')} {r} ({p})"
        for i,(e,n,r,p) in enumerate(FENCE_PROPS,1)
    )
    embed_fence = {
        "color": 0x8b6914,
        "description": (
            ascii_box("🏠 FENCE PROPS (Referensi Crate)")
            + f"\n{fence_lines}\n\n💡 Beli dari **Fence Crate** di Props Shop."
        )
    }

    p1 = {"username": "GAG2 Live Stock 🌱", "embeds": [embed_header, embed_seeds, embed_gear, embed_weather]}
    p2 = {"username": "GAG2 Live Stock 🌱", "embeds": [embed_fence]}

    r1 = requests.post(WEBHOOK_URL, json=p1, timeout=10)
    r2 = requests.post(WEBHOOK_URL, json=p2, timeout=10)

    ok1 = r1.status_code in (200, 204)
    ok2 = r2.status_code in (200, 204)

    if ok1 and ok2:
        print(f"✅ [{wib_str}] Sukses kirim! Slot={slot}")
        # Simpan slot yang sudah dipost
        gist_write({"last_slot": slot})
    else:
        print(f"❌ Error: {r1.status_code} / {r2.status_code}")
        if not ok1: print(r1.text[:300])
        if not ok2: print(r2.text[:300])
        exit(1)

if __name__ == "__main__":
    main()
