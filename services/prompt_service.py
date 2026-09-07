"""
=============================================================
Prompt Service  —  Prompt Comparison & Education Layer
=============================================================
Day 2  |  Part 2F

This service powers the "Prompt Engineering" page of the app.
It exposes three levels of prompts for the same destination so
students and professors can see HOW prompt quality affects output.

Sub-parts implemented here
--------------------------
  2F-i   get_basic_prompt()        → minimal, poor-quality prompt
  2F-ii  get_standard_prompt()     → moderate, better prompt
  2F-iii get_advanced_prompt()     → full production prompt (from Part 2A)
  2F-iv  get_technique_examples()  → dict of all 7 PE techniques with
                                     definition, example, and where-used
  2F-v   get_prompt_stats()        → character/line/keyword counts for UI
=============================================================
"""

from prompts.itinerary_prompt import (
    build_itinerary_prompt,
    get_json_schema,
    get_few_shot_example,
    ITINERARY_JSON_SCHEMA,
)
import json


# =============================================================
# SUB-PART 2F-i  |  BASIC PROMPT (Zero-Shot, No Engineering)
# =============================================================

def get_basic_prompt(destination: str, num_days: int) -> str:
    """
    A minimal, poorly-engineered prompt that most beginners write.

    Problems with this prompt:
      - No role given to the model
      - No context about traveler preferences
      - No budget or dietary constraints
      - No output format specified
      - Response will be vague, generic, and unusable

    Used on the Prompt Engineering page to show
    WHY good prompt engineering matters.

    Args:
        destination: Trip destination.
        num_days   : Number of trip days.

    Returns:
        A short, low-quality prompt string.
    """
    return f"""Plan a {num_days} day trip to {destination}."""


# =============================================================
# SUB-PART 2F-ii  |  STANDARD PROMPT (Some Engineering)
# =============================================================

def get_standard_prompt(
    destination: str,
    num_days: int,
    budget: float,
    interests: list[str],
    currency: str = "INR",
) -> str:
    """
    A moderately-engineered prompt — better than basic but still incomplete.

    Improvements over basic:
      - Mentions budget
      - Lists interests
      - Asks for day-by-day structure

    Still missing:
      - No role prompting
      - No few-shot example
      - No dietary constraints
      - No JSON schema
      - No geographic or pacing constraints

    Args:
        destination: Trip destination.
        num_days   : Number of trip days.
        budget     : Total budget.
        interests  : List of traveler interests.
        currency   : Currency code.

    Returns:
        A medium-quality prompt string.
    """
    interests_str = ", ".join(interests) if interests else "sightseeing"

    return f"""Create a {num_days}-day travel itinerary for {destination}.

Budget: {currency} {budget:,}
Interests: {interests_str}

Please provide a day-by-day plan with activities for each day.
Include some food suggestions and estimated costs.
Make sure the itinerary fits within the budget."""


# =============================================================
# SUB-PART 2F-iii  |  ADVANCED PROMPT (Full Production)
# =============================================================

def get_advanced_prompt(user_inputs: dict) -> str:
    """
    The full production-quality prompt used by this application.

    Built using ALL 7 prompt engineering techniques:
      1. Role Prompting
      2. Context Injection
      3. Few-Shot Prompting
      4. Constraint-Based Prompting
      5. Structured Output Prompting
      (2D & 2C also add:)
      6. Zero-Shot for simple queries
      7. Iterative Refinement for edits

    This is the ACTUAL prompt sent to Gemini when a user clicks
    "Generate My Itinerary". Shown on the education page so
    students can compare Basic → Standard → Advanced.

    Args:
        user_inputs: Full user preferences dict from the form.

    Returns:
        The complete advanced prompt string.
    """
    return build_itinerary_prompt(user_inputs)


# =============================================================
# SUB-PART 2F-iv  |  TECHNIQUE EXAMPLES FOR EDUCATION PAGE
# =============================================================

def get_technique_examples() -> dict:
    """
    Return a dict of all 7 prompt engineering techniques used in
    this project, each with:
        definition   : What the technique is
        example      : The actual prompt text used in this project
        where_used   : Which file/function uses it
        benefit      : What it improves in the output

    Used to populate the cards on the Prompt Engineering page.
    """

    role_prompt_example = (
        "You are an expert AI travel planner with 20+ years of professional experience.\n"
        "You specialize in creating realistic, detailed, and budget-conscious\n"
        "day-by-day travel itineraries tailored to each traveler's unique preferences."
    )

    context_injection_example = (
        "  Destination         : Goa\n"
        "  Trip Duration       : 3 days\n"
        "  Number of Travelers : 2 persons\n"
        "  Total Budget        : INR 15,000\n"
        "  Travel Style        : Standard\n"
        "  Key Interests       : Beaches, Food, Nightlife\n"
        "  Food Preference     : Vegetarian\n"
        "  Special Requirements: Avoid long travel distances"
    )

    few_shot_example = get_few_shot_example()[:800] + "\n... (truncated for display)"

    constraint_example = (
        "1. BUDGET: Total estimated cost MUST NOT exceed INR 15,000.\n"
        "2. FOOD: ALL food must be Vegetarian — absolutely no meat or fish.\n"
        "3. PROXIMITY: Do not place attractions more than 10 km apart in one slot.\n"
        "4. REALISM: Each time slot max = 3-4 hours. Do not overpack the schedule.\n"
        "5. DAYS: Generate EXACTLY 3 days. No more, no less."
    )

    schema_str = json.dumps(ITINERARY_JSON_SCHEMA, indent=2)
    structured_example = (
        "Return ONLY a single valid JSON object.\n"
        "NO explanations. NO markdown. NO code fences.\n"
        "The JSON MUST follow this schema:\n\n"
        + schema_str[:600] + "\n... (schema continues)"
    )

    zero_shot_example = (
        "What should I pack for a 3-day beach trip to Goa in March?\n\n"
        "# No examples given — the model uses its own knowledge directly."
    )

    iterative_example = (
        "# EXISTING ITINERARY (passed as context):\n"
        '{ "days": [ { "day": 1, ... } ], "budget_breakdown": { "total": 18000 } }\n\n'
        "# INSTRUCTION:\n"
        "The current estimated cost is INR 18,000 but the budget is INR 15,000.\n"
        "Reduce cost by INR 3,000 while keeping the traveler's top interests:\n"
        "Beaches and Food.\n"
        "Replace expensive activities with budget alternatives.\n"
        "Return ONLY the complete updated itinerary as valid JSON."
    )

    return {
        "Role Prompting": {
            "icon":        "🎭",
            "definition":  (
                "Tell the model who it is before asking it anything. "
                "Giving the model a specific expert persona dramatically improves "
                "the quality, depth, and relevance of its responses."
            ),
            "example":     role_prompt_example,
            "where_used":  "prompts/itinerary_prompt.py — Section 1\n"
                           "prompts/optimization_prompt.py — Section 1\n"
                           "All modifier prompts — Section 1",
            "benefit":     "Model produces expert-level, domain-specific responses "
                           "instead of generic, surface-level answers.",
        },
        "Context Injection": {
            "icon":        "💉",
            "definition":  (
                "Embed all relevant background information directly into the prompt "
                "before asking the question. The model has no memory between calls, "
                "so all context must be re-injected every time."
            ),
            "example":     context_injection_example,
            "where_used":  "prompts/itinerary_prompt.py — Section 2\n"
                           "services/itinerary_service.py — _build_assistant_context()\n"
                           "All modifier prompts — CURRENT TRIP CONTEXT block",
            "benefit":     "Model gives personalized answers instead of generic ones. "
                           "The AI assistant 'remembers' the trip across chat turns.",
        },
        "Few-Shot Prompting": {
            "icon":        "📚",
            "definition":  (
                "Provide one or more examples of the expected output format BEFORE "
                "asking the model to generate its own output. This anchors the "
                "model's understanding of what 'good' looks like."
            ),
            "example":     few_shot_example,
            "where_used":  "prompts/itinerary_prompt.py — Section 3 (FEW_SHOT_DAY_EXAMPLE)",
            "benefit":     "Generated days are consistently formatted, detailed, and "
                           "realistic — matching the quality of the example given.",
        },
        "Constraint-Based Prompting": {
            "icon":        "🔒",
            "definition":  (
                "Explicitly list rules and restrictions that the model must follow. "
                "Without constraints, the model may ignore budget, dietary needs, "
                "or generate physically impossible schedules."
            ),
            "example":     constraint_example,
            "where_used":  "prompts/itinerary_prompt.py — Section 4 (_build_constraints())\n"
                           "prompts/optimization_prompt.py — Section 3",
            "benefit":     "Prevents hallucinated costs, dietary violations, "
                           "over-packed schedules, and unrealistic activity sequencing.",
        },
        "Structured Output Prompting": {
            "icon":        "📋",
            "definition":  (
                "Instruct the model to return output in a specific machine-readable "
                "format (JSON) by providing the exact schema. This makes the AI "
                "output directly usable by the application without manual parsing."
            ),
            "example":     structured_example,
            "where_used":  "prompts/itinerary_prompt.py — Section 5 (ITINERARY_JSON_SCHEMA)\n"
                           "All modifier and optimization prompts — OUTPUT FORMAT section",
            "benefit":     "AI output can be directly parsed, validated, and displayed "
                           "in the UI. Eliminates the need to extract data from plain text.",
        },
        "Zero-Shot Prompting": {
            "icon":        "🎯",
            "definition":  (
                "Ask the model to perform a task without providing any examples. "
                "Works well for simple, well-understood tasks where the model already "
                "has enough knowledge from training."
            ),
            "example":     zero_shot_example,
            "where_used":  "services/itinerary_service.py — ask_assistant()\n"
                           "(Chat questions don't need examples — context is enough)",
            "benefit":     "Fast and efficient for simple questions. "
                           "No need to craft examples for every type of query.",
        },
        "Iterative Prompt Refinement": {
            "icon":        "🔄",
            "definition":  (
                "Use the output of one prompt as the input context for the next. "
                "Instead of regenerating from scratch, you pass the existing result "
                "and ask the model to improve or modify ONE specific thing."
            ),
            "example":     iterative_example,
            "where_used":  "services/itinerary_service.py — modify_itinerary()\n"
                           "prompts/modifier_prompts.py — all modifier functions\n"
                           "prompts/optimization_prompt.py — budget optimization",
            "benefit":     "Faster and more targeted than full regeneration. "
                           "Preserves the parts the user liked while improving the rest.",
        },
    }


# =============================================================
# SUB-PART 2F-v  |  PROMPT STATS HELPER
# =============================================================

def get_prompt_stats(prompt: str) -> dict:
    """
    Compute statistics about a prompt string for display on the
    Prompt Engineering page.

    Args:
        prompt: Any prompt string.

    Returns:
        dict with:
            characters   : int
            lines        : int
            words        : int
            has_role     : bool — contains "You are an expert" pattern
            has_schema   : bool — contains JSON schema markers
            has_example  : bool — contains "EXAMPLE" or few-shot markers
            has_constraint: bool — contains numbered rules
    """
    return {
        "characters":     len(prompt),
        "lines":          prompt.count("\n") + 1,
        "words":          len(prompt.split()),
        "has_role":       "you are" in prompt.lower(),
        "has_schema":     "trip_summary" in prompt.lower() or "json" in prompt.lower(),
        "has_example":    "example" in prompt.lower() or "calangute" in prompt.lower(),
        "has_constraints": any(
            marker in prompt.upper()
            for marker in ["CONSTRAINT", "MUST NOT", "STRICTLY", "DO NOT"]
        ),
    }


def compare_prompts(user_inputs: dict) -> dict:
    """
    Generate all three prompt levels for the same destination and
    return them together for the comparison view on the education page.

    Args:
        user_inputs: Full user preferences dict.

    Returns:
        dict with keys:
            basic    : {"prompt": str, "stats": dict}
            standard : {"prompt": str, "stats": dict}
            advanced : {"prompt": str, "stats": dict}
    """
    destination = user_inputs.get("destination", "Goa")
    num_days    = user_inputs.get("num_days", 3)
    budget      = user_inputs.get("budget", 15000)
    currency    = user_inputs.get("currency", "INR")
    interests   = user_inputs.get("interests", ["Beaches", "Food"])

    basic_p    = get_basic_prompt(destination, num_days)
    standard_p = get_standard_prompt(destination, num_days, budget, interests, currency)
    advanced_p = get_advanced_prompt(user_inputs)

    return {
        "basic": {
            "prompt": basic_p,
            "stats":  get_prompt_stats(basic_p),
            "label":  "Basic Prompt",
            "description": "No role, no context, no format — the bare minimum.",
        },
        "standard": {
            "prompt": standard_p,
            "stats":  get_prompt_stats(standard_p),
            "label":  "Standard Prompt",
            "description": "Adds budget and interests, but missing role, schema, and constraints.",
        },
        "advanced": {
            "prompt": advanced_p,
            "stats":  get_prompt_stats(advanced_p),
            "label":  "Advanced Prompt (Used in This App)",
            "description": (
                "Full production prompt with Role + Context + Few-Shot "
                "+ Constraints + Structured Output = best results."
            ),
        },
    }
