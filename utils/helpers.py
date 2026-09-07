"""
=============================================================
Helpers  —  General Utility Functions
=============================================================
Day 1  |  Part 1D

Sub-parts implemented here
--------------------------
  1D-i   Date utilities
  1D-ii  Currency formatting
  1D-iii Budget business logic
  1D-iv  Text utilities
  1D-v   UI display helpers  (emojis, icon dicts)
  1D-vi  Optional weather fetch
=============================================================
"""

import os
import re
import requests
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()


# =============================================================
# SUB-PART 1D-i  |  DATE UTILITIES
# =============================================================

def generate_date_list(start_date: date, num_days: int) -> list[str]:
    """
    Return a formatted date string for each trip day.

    Example:
        generate_date_list(date(2025, 3, 10), 3)
        → ["Monday, 10 March 2025",
           "Tuesday, 11 March 2025",
           "Wednesday, 12 March 2025"]
    """
    return [
        (start_date + timedelta(days=i)).strftime("%A, %d %B %Y")
        for i in range(num_days)
    ]


def format_date_range(start_date: date, num_days: int) -> str:
    """Return a human-readable date range string like '10 Mar – 12 Mar 2025'."""
    end_date = start_date + timedelta(days=num_days - 1)
    return f"{start_date.strftime('%d %b')} – {end_date.strftime('%d %b %Y')}"


# =============================================================
# SUB-PART 1D-ii  |  CURRENCY FORMATTING
# =============================================================

_CURRENCY_SYMBOLS: dict[str, str] = {
    "INR": "₹", "USD": "$", "EUR": "€",
    "GBP": "£", "JPY": "¥", "AUD": "A$", "CAD": "C$",
}


def format_currency(amount: float, currency: str = "INR") -> str:
    """
    Format a number as a readable currency string.

    Uses the Indian numbering system for INR (e.g. ₹1,00,000).
    Uses standard international comma format for other currencies.

    Examples:
        format_currency(100000, "INR")  →  "₹1,00,000"
        format_currency(1500,   "USD")  →  "$1,500"
    """
    symbol = _CURRENCY_SYMBOLS.get(currency, currency + " ")
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        amount = 0.0

    if currency == "INR":
        return symbol + _indian_format(int(amount))
    return f"{symbol}{amount:,.0f}"


def _indian_format(n: int) -> str:
    """Convert an integer to Indian numbering (e.g. 150000 → '1,50,000')."""
    s = str(abs(n))
    if len(s) <= 3:
        return s
    last3 = s[-3:]
    rest  = s[:-3]
    parts = []
    while len(rest) > 2:
        parts.append(rest[-2:])
        rest = rest[:-2]
    if rest:
        parts.append(rest)
    parts.reverse()
    return ",".join(parts) + "," + last3


# =============================================================
# SUB-PART 1D-iii  |  BUDGET BUSINESS LOGIC
# =============================================================

def estimate_per_person(total_budget: float, num_travelers: int) -> float:
    """Return the per-person budget share."""
    if num_travelers <= 0:
        return total_budget
    return round(total_budget / num_travelers, 2)


def calculate_budget_status(estimated: float, budgeted: float) -> dict:
    """
    Compare estimated trip cost against the user's total budget.

    Returns a dict with:
        status     : "under" | "tight" | "over"
        difference : absolute difference amount (float)
        percentage : how much over/under as a percentage (float)
        message    : human-readable one-line summary (str)
        emoji      : ✅  ⚠️  or  ❌  (str)
        color      : "green" | "orange" | "red" — for UI styling (str)

    Rules:
        over   → estimated > budgeted
        tight  → estimated <= budgeted but within 10% margin
        under  → more than 10% budget remaining
    """
    diff = budgeted - estimated
    pct  = abs(diff / budgeted * 100) if budgeted > 0 else 0.0

    if diff < 0:
        return {
            "status":     "over",
            "difference": abs(diff),
            "percentage": round(pct, 1),
            "message":    f"Estimated cost exceeds budget by {pct:.1f}%. Consider optimizing.",
            "emoji":      "❌",
            "color":      "red",
        }
    elif pct < 10:
        return {
            "status":     "tight",
            "difference": diff,
            "percentage": round(pct, 1),
            "message":    f"Budget is tight — only {pct:.1f}% buffer remaining.",
            "emoji":      "⚠️",
            "color":      "orange",
        }
    else:
        return {
            "status":     "under",
            "difference": diff,
            "percentage": round(pct, 1),
            "message":    f"Great! You're within budget with {pct:.1f}% to spare.",
            "emoji":      "✅",
            "color":      "green",
        }


def calculate_total_from_days(itinerary: dict) -> float:
    """
    Sum all day_total_cost fields across all days in an itinerary dict.
    Safer than relying on budget_breakdown.total_estimated alone.
    """
    total = 0.0
    for day in itinerary.get("days", []):
        try:
            total += float(day.get("day_total_cost", 0))
        except (TypeError, ValueError):
            pass
    return total


# =============================================================
# SUB-PART 1D-iv  |  TEXT UTILITIES
# =============================================================

def truncate_text(text: str, max_len: int = 200) -> str:
    """Shorten text to max_len characters and append '…' if trimmed."""
    if not text:
        return ""
    text = str(text)
    if len(text) <= max_len:
        return text
    return text[:max_len].rstrip() + "…"


def interests_to_string(interests: list[str]) -> str:
    """
    Convert a list of interests to a natural-language string.

    Examples:
        ["Beaches"]                         → "Beaches"
        ["Beaches", "Food"]                 → "Beaches and Food"
        ["Beaches", "Food", "History"]      → "Beaches, Food and History"
    """
    if not interests:
        return "General sightseeing"
    if len(interests) == 1:
        return interests[0]
    return ", ".join(interests[:-1]) + f" and {interests[-1]}"


def safe_get(d: dict, *keys, default=None):
    """
    Navigate a nested dict safely without raising KeyError.

    Example:
        safe_get(data, "days", 0, "morning", "food", default="N/A")
    """
    for key in keys:
        if not isinstance(d, dict):
            return default
        d = d.get(key, default)
    return d


def list_to_bullets(items: list, prefix: str = "•") -> str:
    """Convert a list of strings into a bulleted multi-line string."""
    if not items:
        return "None listed."
    return "\n".join(f"{prefix} {item}" for item in items)


# =============================================================
# SUB-PART 1D-v  |  UI DISPLAY HELPERS
# =============================================================

# Rotating emojis for each trip day header
_DAY_EMOJIS = [
    "🌅", "🌞", "🌴", "🗺️", "🎒", "🏕️",
    "✈️", "🌊", "🏔️", "🌆", "🎭", "🍽️",
    "🏛️", "🛍️", "📸", "🦁", "🙏", "😌", "🎉", "🌿",
]


def get_day_emoji(day_index: int) -> str:
    """Return a rotating emoji for a day (0-based index)."""
    return _DAY_EMOJIS[day_index % len(_DAY_EMOJIS)]


# Interest name → emoji mapping
INTEREST_ICONS: dict[str, str] = {
    "Beaches":     "🏖️",
    "Adventure":   "🧗",
    "Nature":      "🌿",
    "History":     "🏛️",
    "Culture":     "🎭",
    "Food":        "🍽️",
    "Shopping":    "🛍️",
    "Nightlife":   "🎉",
    "Photography": "📸",
    "Wildlife":    "🦁",
    "Spiritual":   "🙏",
    "Relaxation":  "😌",
}

# Travel style → emoji mapping
STYLE_ICONS: dict[str, str] = {
    "Budget":      "💰",
    "Standard":    "⭐",
    "Luxury":      "👑",
    "Backpacker":  "🎒",
    "Family":      "👨‍👩‍👧‍👦",
    "Couple":      "💑",
    "Solo":        "🧍",
    "Friends":     "👫",
}

# Accommodation → emoji mapping
ACCOMMODATION_ICONS: dict[str, str] = {
    "Hostel":       "🏠",
    "Budget Hotel": "🏨",
    "3-Star Hotel": "⭐⭐⭐",
    "4-Star Hotel": "⭐⭐⭐⭐",
    "5-Star Hotel": "⭐⭐⭐⭐⭐",
    "Resort":       "🏝️",
    "Homestay":     "🏡",
}


# =============================================================
# SUB-PART 1D-vi  |  OPTIONAL WEATHER FETCH
# =============================================================

def get_weather(city: str, target_date: date | None = None) -> dict | None:
    """
    Fetch current weather for a city using OpenWeatherMap API.

    This is an OPTIONAL feature. If the WEATHER_API_KEY is not set
    in .env, this function returns None silently — the app continues
    working normally. No crash, no error message.

    Args:
        city        : City name (e.g. "Goa", "Paris").
        target_date : Unused for current weather, reserved for forecast.

    Returns:
        dict with: temperature, feels_like, description, icon_url, humidity
        OR None if the feature is unavailable.
    """
    api_key = os.getenv("WEATHER_API_KEY", "")
    if not api_key or api_key == "your_weather_api_key_here":
        return None     # Feature not configured — skip silently

    try:
        url    = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": api_key, "units": "metric"}
        resp   = requests.get(url, params=params, timeout=5)

        if resp.status_code != 200:
            return None     # API error — skip silently

        data = resp.json()
        return {
            "temperature":  round(data["main"]["temp"]),
            "feels_like":   round(data["main"]["feels_like"]),
            "description":  data["weather"][0]["description"].capitalize(),
            "icon_url":     f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
            "humidity":     data["main"]["humidity"],
        }
    except Exception:
        return None     # Network/parse error — NEVER crash the app for optional feature
