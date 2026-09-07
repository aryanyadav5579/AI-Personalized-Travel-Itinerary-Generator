"""
=============================================================
Budget Optimization Prompt  —  Constraint-Based Prompting
=============================================================
Day 2  |  Part 2B  |  OPTIMISED VERSION

Token reduction: ~60% smaller than original.
PE Technique: Iterative Refinement + Constraint-Based Prompting
=============================================================
"""

import json


def build_optimization_prompt(itinerary: dict, user_inputs: dict) -> str:
    """
    Build a compact budget optimization prompt.

    Asks Gemini to reduce costs to fit within the user's budget while
    maintaining quality. Uses Iterative Refinement — existing itinerary
    passed as context, targeted cost-reduction changes requested.

    Args:
        itinerary  : Current full itinerary dict.
        user_inputs: User's original preferences.

    Returns:
        Prompt string (~400 chars vs original ~1,200).
    """
    budget   = user_inputs.get("budget", 10000)
    currency = user_inputs.get("currency", "INR")
    food     = ", ".join(user_inputs.get("food_preferences", [])) or "All"
    style    = user_inputs.get("travel_style", "Standard")

    estimated = _get_total_cost(itinerary)
    over_by   = max(0, estimated - budget)

    full_itin = json.dumps(itinerary)

    return (
        f"Trip: {user_inputs.get('destination', '')} | Style: {style} | Food: {food}\n"
        f"User budget: {currency} {budget:,.0f} | Current estimate: {currency} {estimated:,.0f} "
        f"| Over by: {currency} {over_by:,.0f}\n\n"
        f"TASK: Reduce total cost to stay within {currency} {budget:,.0f} by:\n"
        f"  - Replacing expensive activities with free/low-cost alternatives\n"
        f"  - Suggesting cheaper food options (keep {food} diet)\n"
        f"  - Recommending budget transport where possible\n"
        f"  - Adjusting accommodation if needed\n"
        f"Keep quality and all {style} style preferences intact.\n\n"
        f"EXISTING ITINERARY:\n{full_itin}\n\n"
        f"Return ONLY the updated full itinerary as valid JSON (same schema)."
    )


def _get_total_cost(itinerary: dict) -> float:
    """Extract or compute the total estimated cost from the itinerary."""
    bd = itinerary.get("budget_breakdown", {})
    if bd.get("total_estimated"):
        try:
            return float(bd["total_estimated"])
        except (ValueError, TypeError):
            pass

    # Fallback: sum day totals
    total = 0.0
    for day in itinerary.get("days", []):
        try:
            total += float(day.get("day_total_cost", 0))
        except (ValueError, TypeError):
            pass
    return total
