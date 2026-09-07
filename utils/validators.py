"""
=============================================================
Validators  —  Input & JSON Validation
=============================================================
Day 1  |  Part 1C

Two jobs:
  1C-i   Validate user form inputs before building a prompt.
  1C-ii  Validate the JSON structure the AI returns.
  1C-iii Repair broken JSON strings from the AI.

Why this matters
----------------
Without validation, a bad AI response would crash the whole app.
This module makes the app robust and user-friendly by catching
problems early and showing clear error messages instead of tracebacks.
=============================================================
"""

import json
import re
from typing import Any


# =============================================================
# SUB-PART 1C-i  |  USER INPUT VALIDATION
# =============================================================

def validate_user_inputs(inputs: dict) -> tuple[bool, list[str]]:
    """
    Check all user-supplied form values before building an AI prompt.

    Called immediately when the user clicks "Generate My Itinerary".
    If any check fails, a list of errors is shown above the form
    so the user knows exactly what to fix.

    Args:
        inputs: dict containing the trip planning form values.

    Returns:
        (True,  [])              — all values are valid.
        (False, ["msg", ...])   — one or more validation errors.
    """
    errors: list[str] = []

    # ── Destination ──────────────────────────────────────────
    dest = inputs.get("destination", "").strip()
    if not dest:
        errors.append("⚠️  Destination is required.")
    elif len(dest) < 2:
        errors.append("⚠️  Destination name is too short (minimum 2 characters).")

    # ── Trip duration ─────────────────────────────────────────
    days = inputs.get("num_days", 0)
    if not isinstance(days, int) or not (1 <= days <= 30):
        errors.append("⚠️  Trip duration must be between 1 and 30 days.")

    # ── Number of travelers ───────────────────────────────────
    travelers = inputs.get("num_travelers", 0)
    if not isinstance(travelers, int) or not (1 <= travelers <= 50):
        errors.append("⚠️  Number of travelers must be between 1 and 50.")

    # ── Budget ────────────────────────────────────────────────
    budget = inputs.get("budget", 0)
    try:
        budget_f = float(budget)
        if budget_f <= 0:
            errors.append("⚠️  Budget must be greater than zero.")
        elif budget_f > 100_000_000:
            errors.append("⚠️  Budget seems unrealistically large. Please check.")
    except (TypeError, ValueError):
        errors.append("⚠️  Budget must be a valid number.")

    # ── Interests ─────────────────────────────────────────────
    interests = inputs.get("interests", [])
    if not interests:
        errors.append("⚠️  Please select at least one interest.")

    return (len(errors) == 0), errors


# =============================================================
# SUB-PART 1C-ii  |  ITINERARY JSON STRUCTURE VALIDATION
# =============================================================

# Keys that MUST exist in the top-level itinerary object
_REQUIRED_TOP_KEYS = {
    "trip_summary",
    "days",
    "budget_breakdown",
    "packing_list",
    "important_tips",
}

# Keys that MUST exist in every day object
_REQUIRED_DAY_KEYS = {
    "day",
    "date",
    "morning",
    "afternoon",
    "evening",
    "day_total_cost",
}


def _check_slots(day: dict, day_num: int) -> tuple[bool, str]:
    """
    Confirm morning / afternoon / evening are dicts, not strings.
    This catches the 'same structure as morning' model mistake.
    """
    for slot in ("morning", "afternoon", "evening"):
        val = day.get(slot)
        if val is not None and not isinstance(val, dict):
            return (
                False,
                f"Day {day_num}: '{slot}' must be a JSON object, "
                f"got {type(val).__name__} = {str(val)[:40]!r}",
            )
    return True, ""


def validate_itinerary_json(data: Any) -> tuple[bool, str]:
    """
    Check that an AI-generated itinerary dict has the required structure.

    Called right after the AI responds and the JSON is parsed.
    If validation fails, the app triggers a repair or retry rather
    than showing the user broken content.

    Args:
        data: The parsed JSON object (should be a dict).

    Returns:
        (True,  "")             — structure is valid.
        (False, reason_string)  — structure is invalid, with explanation.
    """
    if not isinstance(data, dict):
        return False, "AI response is not a JSON object."

    # Check top-level keys
    missing_top = _REQUIRED_TOP_KEYS - set(data.keys())
    if missing_top:
        return False, f"Missing required top-level keys: {missing_top}"

    # Check 'days' is a non-empty list
    days = data.get("days")
    if not isinstance(days, list) or len(days) == 0:
        return False, "'days' must be a non-empty list."

    # Check each day object
    for i, day in enumerate(days):
        if not isinstance(day, dict):
            return False, f"Day {i + 1} is not a JSON object."
        missing_day = _REQUIRED_DAY_KEYS - set(day.keys())
        if missing_day:
            return False, f"Day {i + 1} is missing keys: {missing_day}"
        # 3A extended: ensure slots are objects, not strings
        ok, reason = _check_slots(day, i + 1)
        if not ok:
            return False, reason

    # Check packing_list and important_tips are lists
    if not isinstance(data.get("packing_list"), list):
        return False, "'packing_list' must be a list."

    if not isinstance(data.get("important_tips"), list):
        return False, "'important_tips' must be a list."

    return True, ""   # ✅ all good


# =============================================================
# SUB-PART 1C-iii  |  JSON REPAIR UTILITY
# =============================================================

def repair_json_string(raw: str) -> dict | None:
    """
    Attempt to fix and parse a malformed JSON string from the AI.

    Repair pipeline (4 steps, each more aggressive):
      1. Strip code fences + remove trailing commas → json.loads()
      2. Remove single-quote JSON (common LLM mistake) → json.loads()
      3. Extract outermost { ... } block using find/rfind (more reliable
         than regex for deeply nested JSON) → json.loads()
      4. Return None — caller shows graceful error to the user.

    This means the app NEVER crashes due to a bad AI response.

    Args:
        raw: The raw text string returned by the AI.

    Returns:
        Parsed dict on success, None on total failure.
    """
    if not raw or not raw.strip():
        return None

    # ── Step 1 — strip fences + remove trailing commas ───────
    text = raw.strip()
    text = re.sub(r"^```(?:json|JSON)?\s*\n?", "", text)
    text = re.sub(r"\n?\s*```\s*$", "", text)
    text = re.sub(r"`", "", text)                      # backtick wrappers
    text = re.sub(r",\s*([}\]])", r"\1", text)         # trailing commas
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # ── Step 2 — replace single-quote keys/values ─────────────
    # Only attempt if text looks like it uses single quotes
    if "'" in text:
        try:
            fixed = re.sub(r"'([^']*)'", r'"\1"', text)
            fixed = re.sub(r",\s*([}\]])", r"\1", fixed)
            return json.loads(fixed)
        except json.JSONDecodeError:
            pass

    # ── Step 3 — extract outermost { ... } block ─────────────
    start = text.find("{")
    end   = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        block = text[start:end + 1]
        block = re.sub(r",\s*([}\]])", r"\1", block)   # re-apply trailing comma fix
        try:
            return json.loads(block)
        except json.JSONDecodeError:
            pass

    # ── Step 4 — give up, caller handles gracefully ───────────
    return None
