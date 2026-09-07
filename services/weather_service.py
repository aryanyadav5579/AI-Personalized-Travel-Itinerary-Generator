"""
=============================================================
Weather Service  —  Optional Weather Integration
=============================================================
Day 4  |  Part 4E

Wraps all weather-related logic in one place.
Every function returns None gracefully if the API key
is not configured — the app never crashes for this feature.

Sub-parts:
  4E-i   get_current_weather()      → temperature, humidity, icon
  4E-ii  get_weather_forecast()     → 5-day forecast list
  4E-iii get_clothing_tips()        → packing suggestions from weather
  4E-iv  get_rainy_day_alternatives() → AI prompt for bad-weather plan
  4E-v   render_weather_widget()    → drop-in Streamlit component
         (call from any page — safe if no API key)
=============================================================
"""

import os
import requests
import streamlit as st
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()

# ── OpenWeatherMap endpoints ───────────────────────────────────
_CURRENT_URL  = "https://api.openweathermap.org/data/2.5/weather"
_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
_TIMEOUT      = 6   # seconds


def _get_api_key() -> str | None:
    key = os.getenv("WEATHER_API_KEY", "")
    if not key or key == "your_weather_api_key_here":
        return None
    return key


# =============================================================
# SUB-PART 4E-i  |  CURRENT WEATHER
# =============================================================

def get_current_weather(city: str) -> dict | None:
    """
    Fetch current weather for a city.

    Returns dict with:
        temperature   : int (°C)
        feels_like    : int (°C)
        description   : str (e.g. "Partly cloudy")
        icon_url      : str (OpenWeatherMap icon URL)
        humidity      : int (%)
        wind_speed    : float (m/s)
        condition     : str — one of: clear, clouds, rain, snow, extreme
        emoji         : str — weather emoji matching condition

    Returns None if API key missing or any error occurs.
    """
    key = _get_api_key()
    if not key:
        return None

    try:
        resp = requests.get(
            _CURRENT_URL,
            params={"q": city, "appid": key, "units": "metric"},
            timeout=_TIMEOUT,
        )
        if resp.status_code != 200:
            return None

        data      = resp.json()
        main_cond = data["weather"][0]["main"].lower()

        return {
            "temperature": round(data["main"]["temp"]),
            "feels_like":  round(data["main"]["feels_like"]),
            "description": data["weather"][0]["description"].capitalize(),
            "icon_url":    f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
            "humidity":    data["main"]["humidity"],
            "wind_speed":  round(data["wind"].get("speed", 0), 1),
            "condition":   _normalize_condition(main_cond),
            "emoji":       _condition_emoji(main_cond),
        }
    except Exception:
        return None


# =============================================================
# SUB-PART 4E-ii  |  5-DAY FORECAST
# =============================================================

def get_weather_forecast(city: str, num_days: int = 5) -> list[dict] | None:
    """
    Fetch up to 5-day weather forecast for a city (one entry per day).

    Returns list of dicts, one per day, with:
        date          : str (e.g. "Mon, 10 Mar")
        temp_max      : int (°C)
        temp_min      : int (°C)
        description   : str
        emoji         : str
        condition     : str
        rain_chance   : int (%) — probability of precipitation

    Returns None if API key missing or any error occurs.
    """
    key = _get_api_key()
    if not key:
        return None

    try:
        resp = requests.get(
            _FORECAST_URL,
            params={"q": city, "appid": key, "units": "metric", "cnt": 40},
            timeout=_TIMEOUT,
        )
        if resp.status_code != 200:
            return None

        # OWM returns 3-hour intervals — group into daily summaries
        daily: dict[str, dict] = {}
        for entry in resp.json().get("list", []):
            day_str = entry["dt_txt"][:10]   # "YYYY-MM-DD"
            if day_str not in daily:
                daily[day_str] = {
                    "temps": [], "descriptions": [],
                    "conditions": [], "rain_probs": [],
                }
            daily[day_str]["temps"].append(entry["main"]["temp"])
            daily[day_str]["descriptions"].append(
                entry["weather"][0]["description"].capitalize()
            )
            daily[day_str]["conditions"].append(
                entry["weather"][0]["main"].lower()
            )
            daily[day_str]["rain_probs"].append(
                int(entry.get("pop", 0) * 100)
            )

        result = []
        for day_str, vals in list(daily.items())[:num_days]:
            d       = date.fromisoformat(day_str)
            cond    = max(set(vals["conditions"]), key=vals["conditions"].count)
            result.append({
                "date":        d.strftime("%a, %d %b"),
                "temp_max":    round(max(vals["temps"])),
                "temp_min":    round(min(vals["temps"])),
                "description": vals["descriptions"][0],
                "emoji":       _condition_emoji(cond),
                "condition":   _normalize_condition(cond),
                "rain_chance": max(vals["rain_probs"]),
            })

        return result if result else None

    except Exception:
        return None


# =============================================================
# SUB-PART 4E-iii  |  CLOTHING TIPS FROM WEATHER
# =============================================================

def get_clothing_tips(weather: dict | None, destination: str = "") -> list[str]:
    """
    Return practical clothing/packing tips based on current weather data.

    Works even without live weather data — falls back to destination-based tips.
    Always returns a list (never None).

    Args:
        weather     : dict from get_current_weather(), or None.
        destination : City/country name for fallback tips.

    Returns:
        List of clothing tip strings.
    """
    if weather is None:
        # Destination-based fallback tips
        dest = destination.lower()
        if any(k in dest for k in ["goa", "beach", "kerala", "bali", "thailand"]):
            return [
                "Pack light, breathable cotton clothes.",
                "Bring a light waterproof layer for evening rain.",
                "Sunscreen SPF 50+ is essential.",
                "Flip-flops or waterproof sandals recommended.",
            ]
        if any(k in dest for k in ["manali", "leh", "ladakh", "shimla", "darjeeling"]):
            return [
                "Carry warm layers — temperatures drop at night.",
                "A waterproof jacket is essential.",
                "Thermal innerwear is recommended.",
                "Sturdy, waterproof trekking shoes needed.",
            ]
        return [
            "Check local weather before packing.",
            "Carry layers to adapt to changing weather.",
            "A light jacket is always useful.",
        ]

    temp      = weather.get("temperature", 25)
    condition = weather.get("condition", "clear")
    humidity  = weather.get("humidity", 50)

    tips = []

    # Temperature-based
    if temp >= 35:
        tips += ["Very hot — wear loose, light-coloured, breathable clothes.",
                 "Carry a portable fan or cooling towel."]
    elif temp >= 28:
        tips += ["Warm weather — cotton or linen clothes are ideal.",
                 "Sunscreen SPF 50+ is a must."]
    elif temp >= 20:
        tips += ["Pleasant temperature — light layers work well.",
                 "A light cardigan for evenings."]
    elif temp >= 10:
        tips += ["Mild to cool — carry a medium jacket.",
                 "Layer up for mornings and evenings."]
    else:
        tips += ["Cold weather — pack warm layers and a heavy jacket.",
                 "Thermal innerwear is recommended."]

    # Condition-based
    if condition == "rain":
        tips += ["Rain expected — pack a compact waterproof raincoat.",
                 "Waterproof shoes or quick-dry sandals.",
                 "A small dry bag to protect electronics."]
    elif condition == "clear" and temp > 28:
        tips += ["Sun is strong — carry a hat/cap and UV sunglasses."]
    elif condition == "snow":
        tips += ["Snow conditions — waterproof boots essential.",
                 "Gloves, thermal hat, and scarf."]
    elif condition == "extreme":
        tips += ["Extreme weather — check advisories before going out."]

    # Humidity-based
    if humidity > 75:
        tips.append("High humidity — choose moisture-wicking fabrics.")

    return tips[:6]  # cap at 6 tips


# =============================================================
# SUB-PART 4E-iv  |  RAINY-DAY ALTERNATIVES PROMPT
# =============================================================

def get_rainy_day_prompt(day_data: dict, user_inputs: dict) -> str:
    """
    Build a prompt asking Gemini to suggest indoor / rainy-day
    alternatives for a given day's activities.

    Technique: Iterative Prompt Refinement — takes an existing day
    and asks for weather-contingent alternatives only.

    Args:
        day_data   : Single day dict from itinerary["days"].
        user_inputs: User preferences.

    Returns:
        Prompt string for call_gemini().
    """
    destination = user_inputs.get("destination", "")
    food_prefs  = user_inputs.get("food_preferences", [])
    food_str    = ", ".join(food_prefs) if food_prefs else "All cuisines"
    currency    = user_inputs.get("currency", "INR")
    budget      = user_inputs.get("budget", 10000)
    num_days    = user_inputs.get("num_days", 1)
    daily_budget = round(budget / num_days) if num_days > 0 else budget

    day_num  = day_data.get("day", 1)
    day_date = day_data.get("date", "")

    morning_acts   = ", ".join(day_data.get("morning",   {}).get("activities", []))
    afternoon_acts = ", ".join(day_data.get("afternoon", {}).get("activities", []))
    evening_acts   = ", ".join(day_data.get("evening",   {}).get("activities", []))

    return f"""
You are an expert travel planner helping a traveler deal with unexpected rain
on their trip to {destination}.

CURRENT DAY PLAN (Day {day_num} — {day_date}):
  Morning   : {morning_acts or 'Free time'}
  Afternoon : {afternoon_acts or 'Free time'}
  Evening   : {evening_acts or 'Free time'}

TASK:
It is raining today. Suggest INDOOR or RAIN-FRIENDLY alternatives for each
time slot (morning, afternoon, evening).

Requirements:
  • All suggestions must be INDOOR or undercover venues at {destination}
  • Food preference: {food_str} (strictly follow this)
  • Daily budget target: {currency} {daily_budget:,}
  • Keep the same time structure (morning / afternoon / evening)
  • Suggestions must be real, named places — not generic descriptions
  • Include 1-2 practical rain tips at the end (e.g. carry an umbrella)

Respond in clear plain text — NO JSON needed.
Format your response as:

MORNING ALTERNATIVE:
[your suggestion]

AFTERNOON ALTERNATIVE:
[your suggestion]

EVENING ALTERNATIVE:
[your suggestion]

RAIN TIPS:
[2 practical tips]
""".strip()


# =============================================================
# SUB-PART 4E-v  |  STREAMLIT WEATHER WIDGET
# =============================================================

def render_weather_widget(destination: str, user_inputs: dict | None = None):
    """
    Drop-in Streamlit component that shows:
      • Current temperature + description
      • 5-day forecast strip
      • Clothing tips
      • "Get Rainy Day Plan" AI button (only shown when raining)

    Safe to call from any page — silently renders nothing if
    the WEATHER_API_KEY is not configured.

    Args:
        destination : City name to fetch weather for.
        user_inputs : Optional user preferences (for rain-day prompt).
    """
    weather  = get_current_weather(destination)
    forecast = get_weather_forecast(destination, num_days=5)

    if weather is None and forecast is None:
        # No API key — show a minimal placeholder
        st.markdown("""
        <div style="
            background:#f8f9ff; border:1px dashed #c7d2fe;
            border-radius:8px; padding:0.7rem 1rem;
            font-size:0.82rem; color:#6366f1; text-align:center;
        ">
            🌤️ Add WEATHER_API_KEY to .env for live weather
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Current weather tile ──────────────────────────────────
    if weather:
        emoji = weather["emoji"]
        temp  = weather["temperature"]
        desc  = weather["description"]
        hum   = weather["humidity"]
        wind  = weather["wind_speed"]

        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea22, #764ba222);
            border: 1px solid #667eea44; border-radius: 10px;
            padding: 0.8rem 1rem; margin-bottom: 0.6rem;
        ">
            <div style="display:flex; align-items:center; gap:0.6rem;">
                <span style="font-size:2rem;">{emoji}</span>
                <div>
                    <div style="font-size:1.4rem; font-weight:700; color:#2d3748;">
                        {temp}°C
                        <span style="font-size:0.85rem; color:#718096; font-weight:400;">
                            · {desc}
                        </span>
                    </div>
                    <div style="font-size:0.78rem; color:#94a3b8;">
                        💧 {hum}% humidity &nbsp;·&nbsp; 💨 {wind} m/s wind
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── 5-day forecast strip ──────────────────────────────────
    if forecast:
        st.markdown(
            "<div style='font-size:0.8rem; font-weight:600; color:#4a5568; "
            "margin-bottom:0.3rem;'>5-Day Forecast</div>",
            unsafe_allow_html=True,
        )
        cols = st.columns(len(forecast))
        for col, day in zip(cols, forecast):
            with col:
                rain_badge = (
                    f"<div style='font-size:0.7rem;color:#e53e3e;'>🌧️ {day['rain_chance']}%</div>"
                    if day["rain_chance"] >= 40 else ""
                )
                st.markdown(f"""
                <div style="
                    background:#fff; border:1px solid #e2e8f0;
                    border-radius:8px; padding:0.4rem; text-align:center;
                    font-size:0.75rem;
                ">
                    <div style="color:#718096;">{day['date']}</div>
                    <div style="font-size:1.3rem;">{day['emoji']}</div>
                    <div style="font-weight:600; color:#2d3748;">
                        {day['temp_max']}° <span style="color:#94a3b8;">{day['temp_min']}°</span>
                    </div>
                    {rain_badge}
                </div>
                """, unsafe_allow_html=True)

    # ── Clothing tips ─────────────────────────────────────────
    tips = get_clothing_tips(weather, destination)
    if tips:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<div style='font-size:0.8rem; font-weight:600; color:#4a5568;'>"
            "👗 Packing Tips Based on Weather</div>",
            unsafe_allow_html=True,
        )
        for tip in tips[:4]:
            st.caption(f"• {tip}")

    # ── Rainy-day AI button ───────────────────────────────────
    if weather and weather.get("condition") == "rain":
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(
            "☔ Get AI Rainy-Day Plan",
            key="rainy_day_btn",
            use_container_width=True,
            help="AI will suggest indoor alternatives for today's activities.",
            type="primary",
        ):
            _fetch_rainy_day_plan(destination, user_inputs or {})


# =============================================================
# PRIVATE HELPERS
# =============================================================

def _normalize_condition(raw: str) -> str:
    """Map OWM condition string to a simplified category."""
    raw = raw.lower()
    if any(w in raw for w in ["rain", "drizzle", "shower", "thunderstorm"]):
        return "rain"
    if any(w in raw for w in ["snow", "sleet", "blizzard"]):
        return "snow"
    if any(w in raw for w in ["cloud", "overcast", "mist", "fog", "haze"]):
        return "clouds"
    if any(w in raw for w in ["tornado", "squall", "dust", "sand", "ash"]):
        return "extreme"
    return "clear"


def _condition_emoji(condition: str) -> str:
    """Return a weather emoji for a condition string."""
    mapping = {
        "clear":       "☀️",
        "clouds":      "⛅",
        "rain":        "🌧️",
        "drizzle":     "🌦️",
        "thunderstorm":"⛈️",
        "snow":        "❄️",
        "mist":        "🌫️",
        "fog":         "🌫️",
        "haze":        "🌁",
        "extreme":     "🌪️",
    }
    for key, emoji in mapping.items():
        if key in condition.lower():
            return emoji
    return "🌤️"


def _fetch_rainy_day_plan(destination: str, user_inputs: dict):
    """Fetch and display rainy-day alternatives using Gemini."""
    from services.llm_service import is_api_configured, call_gemini

    if not is_api_configured():
        st.warning("Add your Gemini API key to .env to get AI rainy-day suggestions.")
        return

    # Build a minimal day_data for the prompt
    day_data = {
        "day": 1, "date": "Today",
        "morning":   {"activities": [f"Explore {destination}"]},
        "afternoon": {"activities": ["Sightseeing"]},
        "evening":   {"activities": ["Dinner & relaxation"]},
    }

    prompt = get_rainy_day_prompt(day_data, {**user_inputs, "destination": destination})

    with st.spinner("☔ Getting rainy-day alternatives..."):
        try:
            reply = call_gemini(prompt, temperature=0.7, max_output_tokens=1024)
            st.markdown("#### ☔ Rainy Day Plan")
            st.markdown(reply)
        except Exception as e:
            st.error(f"Could not fetch rainy-day plan: {e}")
