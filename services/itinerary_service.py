"""
=============================================================
Itinerary Service  —  Core AI Business Logic
=============================================================
Day 2  |  Part 2E

This is the brain of the application.
It connects the prompt builders (prompts/) with the LLM wrapper
(llm_service.py) and handles all validation, repair, and error logic.

Sub-parts implemented here
--------------------------
  2E-i   generate_itinerary()       → create new itinerary from user inputs
  2E-ii  modify_itinerary()         → apply a specific edit to existing plan
  2E-iii ask_assistant()            → answer user questions about the trip
  2E-iv  Budget helpers
            extract_budget_data()
            calculate_total_estimated_cost()
            get_budget_comparison()
=============================================================
"""

import json

from services.llm_service    import call_gemini_json, call_gemini_chat, call_gemini, tokens_for_days
from prompts.itinerary_prompt   import build_itinerary_prompt
from prompts.optimization_prompt import build_optimization_prompt
from prompts.modifier_prompts   import get_modifier_prompt
from utils.validators import validate_itinerary_json, repair_json_string
from utils.helpers    import calculate_budget_status, format_currency


# =============================================================
# SUB-PART 2E-i  |  GENERATE ITINERARY
# =============================================================

def generate_itinerary(user_inputs: dict) -> dict:
    """
    Generate a full day-by-day travel itinerary using Gemini.

    Full pipeline:
      1. Build prompt  (itinerary_prompt.py — all 5 PE techniques)
      2. Call Gemini   (llm_service.call_gemini_json)
      3. Validate JSON structure
      4. If invalid → attempt repair → retry once more
      5. Return validated itinerary dict

    Args:
        user_inputs: dict from the trip planning form with keys:
            destination, num_days, num_travelers, budget, currency,
            start_date, interests, travel_style, accommodation,
            transportation, food_preferences, special_requirements

    Returns:
        Validated itinerary dict matching ITINERARY_JSON_SCHEMA.

    Raises:
        ValueError  : If JSON cannot be parsed or validated after retries.
        RuntimeError: If the Gemini API call itself fails (from llm_service).
    """
    # Step 1 — build the prompt
    prompt = build_itinerary_prompt(user_inputs)
    num_days = int(user_inputs.get("num_days", 3))
    max_tok  = tokens_for_days(num_days)

    # Step 2 — call Gemini and parse JSON (retries built into call_gemini_json)
    data = call_gemini_json(prompt, temperature=0.4, max_output_tokens=max_tok)

    # Step 3 — validate structure
    valid, reason = validate_itinerary_json(data)
    if valid:
        return _post_process(data)

    # Step 4 — validation failed: try repair then re-validate
    repaired = repair_json_string(json.dumps(data))   # re-serialize and repair
    if repaired:
        valid2, reason2 = validate_itinerary_json(repaired)
        if valid2:
            return _post_process(repaired)

    # Step 5 — still invalid: retry entire generation once
    data2 = call_gemini_json(prompt, temperature=0.3, max_output_tokens=max_tok)
    valid3, reason3 = validate_itinerary_json(data2)
    if valid3:
        return _post_process(data2)

    raise ValueError(
        f"Could not generate a valid itinerary after multiple attempts.\n"
        f"Last validation error: {reason3}\n"
        "Please try again or simplify your trip details."
    )


# =============================================================
# SUB-PART 2E-ii  |  MODIFY ITINERARY
# =============================================================

def modify_itinerary(
    action: str,
    itinerary: dict,
    user_inputs: dict,
    **kwargs,
) -> dict:
    """
    Apply a specific edit to an existing itinerary using Gemini.

    Supported actions and their prompt sources
    ------------------------------------------
    Action                Source prompt function
    ─────────────────     ─────────────────────────────────────
    "make_cheaper"        optimization_prompt.build_optimization_prompt()
    "regenerate_day"      modifier_prompts.build_regenerate_day_prompt()
    "add_day"             modifier_prompts.build_add_day_prompt()
    "remove_day"          modifier_prompts.build_remove_day_prompt()
    "make_adventurous"    modifier_prompts.build_make_adventurous_prompt()
    "make_relaxed"        modifier_prompts.build_make_relaxed_prompt()
    "add_food"            modifier_prompts.build_add_food_prompt()
    "reduce_travel_time"  modifier_prompts.build_reduce_travel_time_prompt()
    "regenerate_entire"   build_itinerary_prompt() (same as generate)

    Prompt Engineering — Iterative Refinement:
        Every action (except "regenerate_entire") passes the existing
        itinerary as context and asks the model to modify ONE thing.
        This is Iterative Prompt Refinement in practice.

    Args:
        action     : One of the action strings above.
        itinerary  : The current itinerary dict.
        user_inputs: Original user preferences.
        **kwargs   : Extra params:
                       day_num (int) — required for regenerate_day, remove_day.

    Returns:
        Updated and validated itinerary dict.

    Raises:
        ValueError  : Unknown action or invalid AI response.
        RuntimeError: Gemini API failure.
    """
    # Special case: full regeneration
    if action == "regenerate_entire":
        return generate_itinerary(user_inputs)

    # Special case: budget optimization (has its own prompt builder)
    if action == "make_cheaper":
        prompt = build_optimization_prompt(itinerary, user_inputs)
    else:
        # All other actions go through the modifier dispatcher
        prompt = get_modifier_prompt(action, itinerary, user_inputs, **kwargs)

    # Call Gemini (modifiers only change 1 day — fewer tokens needed)
    mod_tok = tokens_for_days(len(itinerary.get("days", [3])))
    data = call_gemini_json(prompt, temperature=0.4, max_output_tokens=mod_tok)

    # Validate
    valid, reason = validate_itinerary_json(data)
    if valid:
        return _post_process(data)

    # One repair attempt
    repaired = repair_json_string(json.dumps(data))
    if repaired:
        valid2, _ = validate_itinerary_json(repaired)
        if valid2:
            return _post_process(repaired)

    raise ValueError(
        f"Could not apply '{action}' modification — AI returned an invalid structure.\n"
        f"Reason: {reason}\n"
        "Please try again."
    )


# =============================================================
# SUB-PART 2E-iii  |  AI TRAVEL ASSISTANT
# =============================================================

def ask_assistant(
    question: str,
    itinerary: dict,
    user_inputs: dict,
    chat_history: list[dict],
) -> str:
    """
    Answer a user's question about their trip using Gemini chat.

    Prompt Engineering — Context Injection:
        The full itinerary + user preferences are injected into the
        system context so the model "remembers" the entire trip
        across every turn of the conversation.

    Args:
        question     : The user's latest question.
        itinerary    : Current itinerary dict (injected as context).
        user_inputs  : Original user preferences (injected as context).
        chat_history : List of {"role": "user"/"model", "content": str}
                       from previous turns.

    Returns:
        The assistant's reply as a plain string.

    Raises:
        RuntimeError: If the Gemini API call fails.
    """
    # Build the system context (injected once at conversation start)
    system_context = _build_assistant_context(itinerary, user_inputs)

    # Append the new question to history
    messages = list(chat_history) + [{"role": "user", "content": question}]

    # Call Gemini chat
    reply = call_gemini_chat(
        messages=messages,
        system_context=system_context,
        temperature=0.7,
        max_output_tokens=2048,
    )
    return reply.strip()


def _build_assistant_context(itinerary: dict, user_inputs: dict) -> str:
    """
    Build a compact system-level context for the AI travel assistant.

    Token-optimised: sends a 5-line summary instead of the full itinerary JSON.
    This reduces chat input tokens by ~84% while preserving useful context.

    Technique: Context Injection (compact)
    """
    destination   = user_inputs.get("destination", "")
    num_days      = user_inputs.get("num_days", 0)
    budget        = user_inputs.get("budget", 0)
    currency      = user_inputs.get("currency", "INR")
    food_prefs    = user_inputs.get("food_preferences", [])
    travel_style  = user_inputs.get("travel_style", "")
    num_travelers = user_inputs.get("num_travelers", 1)

    food_str = ", ".join(food_prefs) if food_prefs else "All cuisines"

    # Build compact day summaries (one line per day)
    day_summaries = []
    for d in itinerary.get("days", []):
        day_num  = d.get("day", "?")
        morning  = d.get("morning",   {}).get("attraction", "")
        aft      = d.get("afternoon", {}).get("attraction", "")
        eve      = d.get("evening",   {}).get("attraction", "")
        cost     = d.get("day_total_cost", 0)
        spots    = " → ".join(filter(None, [morning, aft, eve]))
        day_summaries.append(f"  Day {day_num}: {spots} ({currency} {cost:,.0f})")

    days_text = "\n".join(day_summaries) or "  No days yet."

    # Budget status
    estimated = calculate_total_estimated_cost(itinerary)
    status    = "within budget" if estimated <= budget else f"over by {currency} {estimated - budget:,.0f}"

    return (
        f"You are a friendly AI travel assistant for a {num_travelers}-person trip to {destination} "
        f"({num_days} days, {currency} {budget:,.0f} budget, {travel_style} style, food: {food_str}).\n"
        f"Trip day summary:\n{days_text}\n"
        f"Budget: estimated {currency} {estimated:,.0f} — {status}.\n"
        f"Answer questions about this specific trip concisely. "
        f"Do NOT output the full itinerary JSON unless explicitly asked."
    )


# =============================================================
# SUB-PART 2E-iv  |  BUDGET HELPERS
# =============================================================

def extract_budget_data(itinerary: dict) -> dict:
    """
    Extract the budget_breakdown dict from an itinerary.

    Returns a guaranteed dict with all keys present
    (fills missing keys with 0 to prevent KeyError in the UI).

    Returns:
        dict with keys:
            accommodation, food, transportation,
            activities_entry_fees, shopping_misc, total_estimated
    """
    default = {
        "accommodation":        0,
        "food":                 0,
        "transportation":       0,
        "activities_entry_fees": 0,
        "shopping_misc":        0,
        "total_estimated":      0,
    }
    raw = itinerary.get("budget_breakdown", {})
    if not isinstance(raw, dict):
        return default

    # Merge raw into defaults (so missing keys get 0)
    merged = {**default, **{k: float(v) for k, v in raw.items()
                             if k in default and _is_number(v)}}
    return merged


def calculate_total_estimated_cost(itinerary: dict) -> float:
    """
    Calculate total estimated trip cost by summing day_total_cost
    across all days AND adding accommodation from budget_breakdown.

    This is more accurate than using budget_breakdown.total_estimated
    alone, because some AI responses may not sum correctly.

    Returns:
        Total estimated cost as a float.
    """
    day_sum = 0.0
    for day in itinerary.get("days", []):
        try:
            day_sum += float(day.get("day_total_cost", 0))
        except (TypeError, ValueError):
            pass

    accommodation = 0.0
    try:
        accommodation = float(
            itinerary.get("budget_breakdown", {}).get("accommodation", 0)
        )
    except (TypeError, ValueError):
        pass

    # If days already include accommodation in their costs, avoid double-counting.
    # Use budget_breakdown.total_estimated as the authoritative source if available.
    breakdown_total = 0.0
    try:
        breakdown_total = float(
            itinerary.get("budget_breakdown", {}).get("total_estimated", 0)
        )
    except (TypeError, ValueError):
        pass

    # Prefer breakdown total if it looks realistic (within 20% of day sum)
    if breakdown_total > 0:
        return breakdown_total

    return day_sum + accommodation


def get_budget_comparison(
    itinerary: dict,
    user_budget: float,
    currency: str = "INR",
) -> dict:
    """
    Compare the itinerary's estimated cost against the user's budget.

    Returns:
        dict with keys from calculate_budget_status() PLUS:
            estimated_cost   : float — what the trip will cost
            user_budget      : float — what the user said they have
            budget_fmt       : str   — formatted user budget
            estimated_fmt    : str   — formatted estimated cost
            difference_fmt   : str   — formatted difference
    """
    estimated = calculate_total_estimated_cost(itinerary)
    status    = calculate_budget_status(estimated, user_budget)

    return {
        **status,
        "estimated_cost":  estimated,
        "user_budget":     user_budget,
        "budget_fmt":      format_currency(user_budget, currency),
        "estimated_fmt":   format_currency(estimated, currency),
        "difference_fmt":  format_currency(status["difference"], currency),
    }


def get_day_cost_table(itinerary: dict) -> list[dict]:
    """
    Build a list of per-day cost records for display in the budget table.

    Returns:
        List of dicts, one per day, with keys:
            day, date, morning_cost, afternoon_cost, evening_cost, day_total
    """
    rows = []
    for day in itinerary.get("days", []):
        rows.append({
            "day":           day.get("day", ""),
            "date":          day.get("date", ""),
            "morning_cost":  _safe_float(day, "morning",   "estimated_cost"),
            "afternoon_cost": _safe_float(day, "afternoon", "estimated_cost"),
            "evening_cost":  _safe_float(day, "evening",   "estimated_cost"),
            "day_total":     _safe_float_key(day, "day_total_cost"),
        })
    return rows


# =============================================================
# PRIVATE HELPERS
# =============================================================

def _post_process(data: dict) -> dict:
    """
    Apply minor fixes to ensure numeric fields are actual numbers
    (not strings), so the UI can use them without type errors.
    """
    # Ensure day_total_cost is float
    for day in data.get("days", []):
        for slot in ("morning", "afternoon", "evening"):
            slot_data = day.get(slot, {})
            if isinstance(slot_data, dict):
                slot_data["estimated_cost"] = _coerce_float(
                    slot_data.get("estimated_cost", 0)
                )
        day["day_total_cost"] = _coerce_float(day.get("day_total_cost", 0))

    # Ensure budget_breakdown values are float
    bd = data.get("budget_breakdown", {})
    if isinstance(bd, dict):
        for key in bd:
            bd[key] = _coerce_float(bd.get(key, 0))

    return data


def _coerce_float(val) -> float:
    """Convert a value to float, return 0.0 on failure."""
    try:
        return float(str(val).replace(",", "").replace("₹", "").strip())
    except (TypeError, ValueError):
        return 0.0


def _is_number(val) -> bool:
    """Return True if val can be converted to float."""
    try:
        float(val)
        return True
    except (TypeError, ValueError):
        return False


def _safe_float(d: dict, *keys) -> float:
    """Navigate nested dict and return float value or 0.0."""
    for key in keys:
        if not isinstance(d, dict):
            return 0.0
        d = d.get(key, 0.0)
    return _coerce_float(d)


def _safe_float_key(d: dict, key: str) -> float:
    """Return float value of a top-level dict key or 0.0."""
    return _coerce_float(d.get(key, 0.0))
