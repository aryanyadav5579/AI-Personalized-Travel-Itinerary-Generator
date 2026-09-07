"""
=============================================================
Itinerary Prompt Builder  —  Prompt Engineering Engine
=============================================================
Day 2  |  Part 2A  |  OPTIMISED VERSION v2

Changes from v1:
  2A — Full schema for all 3 slots (morning/afternoon/evening).
       Removed "same structure as morning" string shortcut that
       caused the model to output a string instead of an object.
       Numeric fields use 0 (int) not "number" (string).
  2B — Stronger mandatory JSON-only output instruction at the end.

PE Techniques preserved:
  1. Role Prompting      — 1 line role statement
  2. Context Injection   — all 12 user inputs
  3. Constraint-Based    — 6 critical rules
  4. Structured Output   — full schema, all 3 slots expanded
=============================================================
"""

import json
from datetime import date, timedelta

# ── Slot template (reused 3 times in schema) ──────────────────
_SLOT = {
    "time": "string e.g. 7:00 AM - 11:00 AM",
    "activities": ["string", "string"],
    "attraction": "string",
    "food": "string",
    "transport": "string",
    "estimated_cost": 0,
    "notes": "string",
}

# ── 2A: Full schema — all 3 slots fully expanded ──────────────
ITINERARY_JSON_SCHEMA = {
    "trip_summary": {
        "destination": "string",
        "duration_days": 0,
        "start_date": "string",
        "end_date": "string",
        "num_travelers": 0,
        "total_budget": 0,
        "currency": "string",
        "travel_style": "string",
        "accommodation_type": "string",
        "transportation_mode": "string",
        "top_interests": ["string"],
        "overview": "string",
    },
    "days": [
        {
            "day": 1,
            "date": "string",
            "morning": {
                "time": "string e.g. 7:00 AM - 11:00 AM",
                "activities": ["string", "string"],
                "attraction": "string",
                "food": "string",
                "transport": "string",
                "estimated_cost": 0,
                "notes": "string",
            },
            "afternoon": {
                "time": "string e.g. 12:00 PM - 4:00 PM",
                "activities": ["string", "string"],
                "attraction": "string",
                "food": "string",
                "transport": "string",
                "estimated_cost": 0,
                "notes": "string",
            },
            "evening": {
                "time": "string e.g. 5:00 PM - 9:00 PM",
                "activities": ["string", "string"],
                "attraction": "string",
                "food": "string",
                "transport": "string",
                "estimated_cost": 0,
                "notes": "string",
            },
            "day_total_cost": 0,
            "daily_transport": "string",
            "tips": ["string", "string"],
        }
    ],
    "budget_breakdown": {
        "accommodation": 0,
        "food": 0,
        "transportation": 0,
        "activities_entry_fees": 0,
        "shopping_misc": 0,
        "total_estimated": 0,
    },
    "packing_list": ["string"],
    "important_tips": ["string"],
}


def build_itinerary_prompt(user_inputs: dict) -> str:
    """
    Build the main itinerary generation prompt.

    Args:
        user_inputs: Validated dict of 12 user form inputs.

    Returns:
        Compact prompt string (~2,200 chars, ~550 tokens).
    """
    destination    = user_inputs.get("destination", "")
    num_days       = int(user_inputs.get("num_days", 3))
    num_travelers  = int(user_inputs.get("num_travelers", 2))
    budget         = float(user_inputs.get("budget", 10000))
    currency       = user_inputs.get("currency", "INR")
    interests      = user_inputs.get("interests", [])
    travel_style   = user_inputs.get("travel_style", "Standard")
    accommodation  = user_inputs.get("accommodation", "3-Star Hotel")
    transportation = user_inputs.get("transportation", "Mixed")
    food_prefs     = user_inputs.get("food_preferences", [])
    special_req    = user_inputs.get("special_requirements", "None")
    start_date_raw = user_inputs.get("start_date", str(date.today()))

    # Date range
    try:
        start = start_date_raw if isinstance(start_date_raw, date) \
                else date.fromisoformat(str(start_date_raw))
    except Exception:
        start = date.today()
    end = start + timedelta(days=num_days - 1)

    daily_budget  = round(budget / num_days) if num_days > 0 else budget
    per_person    = round(budget / num_travelers) if num_travelers > 0 else budget
    interests_str = ", ".join(interests) if interests else "General sightseeing"
    food_str      = ", ".join(food_prefs) if food_prefs else "All cuisines"

    # ── SECTION 1 — ROLE PROMPTING ────────────────────────────
    role = (
        "You are an expert travel planner. "
        "Create a detailed, budget-accurate, personalized travel itinerary."
    )

    # ── SECTION 2 — CONTEXT INJECTION ────────────────────────
    context = (
        f"TRIP DETAILS:\n"
        f"  Destination  : {destination}\n"
        f"  Dates        : {start.strftime('%d %b %Y')} to "
        f"{end.strftime('%d %b %Y')} ({num_days} days)\n"
        f"  Travelers    : {num_travelers}\n"
        f"  Budget       : {currency} {budget:,.0f} total | "
        f"{currency} {daily_budget:,.0f}/day | "
        f"{currency} {per_person:,.0f}/person\n"
        f"  Style        : {travel_style}\n"
        f"  Stay         : {accommodation}\n"
        f"  Transport    : {transportation}\n"
        f"  Interests    : {interests_str}\n"
        f"  Food         : {food_str}\n"
        f"  Special      : {special_req}"
    )

    # ── SECTION 3 — CONSTRAINT-BASED PROMPTING ───────────────
    constraints = (
        f"RULES (follow strictly):\n"
        f"1. Total cost MUST NOT exceed {currency} {budget:,.0f}\n"
        f"2. Food MUST match: {food_str}\n"
        f"3. Each day MUST have morning, afternoon, evening as JSON objects\n"
        f"4. Activities must suit {travel_style} style\n"
        f"5. Use real named attractions\n"
        f"6. All cost fields must be numbers (not strings)"
    )

    # ── SECTION 4 — STRUCTURED OUTPUT PROMPTING ──────────────
    schema_str = json.dumps(ITINERARY_JSON_SCHEMA, indent=2)

    # 2B: Stronger mandatory JSON output instruction
    output_instruction = (
        "OUTPUT RULES (mandatory):\n"
        "- Your ENTIRE response must be ONE valid JSON object\n"
        "- Start with { and end with }\n"
        "- Do NOT write ```json or any markdown\n"
        "- Do NOT add any text before or after the JSON\n"
        "- morning, afternoon, evening MUST each be a JSON object (not a string)\n"
        "- All numeric fields must be numbers not strings\n\n"
        f"JSON SCHEMA TO FOLLOW:\n{schema_str}"
    )

    return f"{role}\n\n{context}\n\n{constraints}\n\n{output_instruction}"


def get_json_schema() -> dict:
    """Return the JSON schema dict (for documentation / PE page)."""
    return ITINERARY_JSON_SCHEMA


def get_few_shot_example() -> str:
    """Placeholder — few-shot replaced by full schema in optimised version."""
    return (
        "Few-shot example removed in optimised version. "
        "Full 3-slot schema enforces structure at prompt level."
    )
