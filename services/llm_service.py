"""
=============================================================
LLM Service  —  Google Gemini API Wrapper
=============================================================
Day 1  |  Part 1B

This is the ONLY file that talks directly to the Gemini API.
Every other module imports from here — never call genai elsewhere.

Uses the new google-genai SDK (google.genai).

Sub-parts implemented here
--------------------------
  1B-i   API key management          (get_api_key, is_api_configured, _get_client)
  1B-ii  Core call functions         (call_gemini, call_gemini_json, call_gemini_chat)
  1B-iii Internal helpers            (_strip_code_fences, _extract_json_block)
=============================================================
"""

import os
import re
import json
import time
import warnings

# Suppress FutureWarnings from google SDK on older Python versions
warnings.filterwarnings("ignore", category=FutureWarning)

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# ── Model to use ──────────────────────────────────────────────────────────────
_MODEL_NAME = "gemini-3.5-flash-lite"


# =============================================================
# SUB-PART 1B-i  |  API KEY MANAGEMENT
# =============================================================

def get_api_key() -> str | None:
    """Return the Gemini API key from the .env file."""
    return os.getenv("GEMINI_API_KEY")


def is_api_configured() -> bool:
    """
    Return True only if a real (non-placeholder) Gemini API key exists.
    Used by the UI to show/hide the warning banner.
    """
    key = get_api_key()
    return bool(
        key
        and key.strip()
        and key != "your_gemini_api_key_here"
        and len(key) > 15
    )


def _validate_key() -> str:
    """
    Validate key presence and return it.
    Raises ValueError with step-by-step fix instructions if missing.
    """
    key = get_api_key()
    if not key or key == "your_gemini_api_key_here" or len(key) < 15:
        raise ValueError(
            "Gemini API key not found or invalid.\n\n"
            "How to fix:\n"
            "  1. Copy .env.example -> .env\n"
            "  2. Visit https://aistudio.google.com/app/apikey\n"
            "  3. Create a free key and paste it as GEMINI_API_KEY=AIzaSy...\n"
            "  4. Save .env and restart the app."
        )
    return key


def _get_client() -> genai.Client:
    """Return a configured Gemini client (new SDK)."""
    key = _validate_key()
    return genai.Client(api_key=key)


# =============================================================
# SUB-PART 1B-ii  |  CORE CALL FUNCTIONS
# =============================================================

def call_gemini(
    prompt: str,
    temperature: float = 0.7,
    max_output_tokens: int = 2048,
    retries: int = 3,
) -> str:
    """
    Send a plain-text prompt to Gemini and return the response text.

    This is the backbone of ALL prompt engineering in this project.
    Every technique (role prompting, few-shot, constraints, etc.) works
    by constructing the `prompt` string cleverly before calling this.

    Args:
        prompt           : The complete prompt string.
        temperature      : 0.0 = deterministic  |  1.0 = very creative.
        max_output_tokens: Maximum response length in tokens.
        retries          : Retry attempts with exponential back-off (2s->4s->8s).

    Returns:
        The model's response as a plain string.

    Raises:
        RuntimeError: If all retry attempts fail.
    """
    client = _get_client()

    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        # Disable AFC — the SDK enables it by default in generate_content(),
        # causing "model output must contain text or tool calls" crash when
        # no tools are defined but AFC fires internally.
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )

    last_error = None
    for attempt in range(1, retries + 1):
        try:
            response = client.models.generate_content(
                model=_MODEL_NAME,
                contents=prompt,
                config=config,
            )
            text = response.text
            if not text:
                raise ValueError("Gemini returned an empty response.")
            return text

        except Exception as exc:
            last_error = exc
            if attempt < retries:
                wait = 2 ** attempt      # 2 -> 4 -> 8 seconds
                time.sleep(wait)

    raise RuntimeError(
        f"Gemini API call failed after {retries} attempts.\n"
        f"Last error: {last_error}\n"
        "Check your API key and internet connection."
    )


def tokens_for_days(num_days: int) -> int:
    """
    Return a safe max_output_tokens value scaled to trip duration.

    Live sweep test result:
      3-day itinerary = 6,600 chars ≈ 1,650 tokens of OUTPUT needed.
      max_output_tokens must be HIGHER than that or the model truncates silently.
      Minimum safe value = 4096 (confirmed working by live API test).

    Formula: 4096 base + 512 per extra day beyond 3, capped at 8192.
      1–3 day  → 4096   |  5-day → 5120  |  7-day → 6144
    """
    extra = max(0, num_days - 3)
    return min(4096 + (extra * 512), 8192)


def call_gemini_json(
    prompt: str,
    temperature: float = 0.2,
    max_output_tokens: int = 4096,
    retries: int = 3,
) -> dict:
    """
    Call Gemini and parse the response as JSON.

    NOTE: response_mime_type='application/json' is intentionally NOT used here.
    It triggers AFC (Automatic Function Calling) in generate_content(),
    which is unsupported and causes empty/503 responses.
    JSON correctness is enforced via prompt instruction + post-processing repair.

    Repair pipeline per attempt:
      1. Strip markdown code fences
      2. Remove trailing commas  (most common LLM JSON mistake)
      3. json.loads() on cleaned text
      4. Extract first {...} block and retry json.loads()

    Returns:
        Parsed Python dict from the model's JSON response.

    Raises:
        ValueError: If JSON cannot be parsed after all retries.
    """
    last_parse_error = None

    for attempt in range(1, retries + 1):
        try:
            # Route through call_gemini() — already has exponential backoff retry
            raw = call_gemini(
                prompt,
                temperature=temperature,
                max_output_tokens=max_output_tokens,
            )
        except RuntimeError as exc:
            last_parse_error = exc
            if attempt < retries:
                time.sleep(2 ** attempt)
            continue

        # ── Repair pipeline ──────────────────────────────────
        cleaned = _strip_code_fences(raw)
        # Remove trailing commas before } or ] — second most common LLM JSON mistake
        cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)

        # Attempt 1: direct json.loads
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as exc:
            last_parse_error = exc

        # Attempt 2: extract first {...} block, re-apply comma fix, retry
        extracted = _extract_json_block(cleaned)
        if extracted:
            extracted = re.sub(r",\s*([}\]])", r"\1", extracted)
            try:
                return json.loads(extracted)
            except json.JSONDecodeError:
                pass

        if attempt < retries:
            time.sleep(2)

    raise ValueError(
        f"Could not parse Gemini response as JSON after {retries} attempts.\n"
        f"Last JSON error: {last_parse_error}\n"
        "Tip: Make sure your prompt ends with the structured output instruction."
    )


def call_gemini_chat(
    messages: list[dict],
    system_context: str = "",
    temperature: float = 0.7,
    max_output_tokens: int = 4096,
) -> str:
    """
    Multi-turn chat with Gemini using conversation history.

    Prompt Engineering — Context Injection:
        `system_context` is prepended to the first user message.
        This injects the full itinerary + user preferences, giving
        the model "memory" of the trip across the entire conversation.

    Args:
        messages       : List of {"role": "user"/"model", "content": str}.
        system_context : Context injected at the start of the conversation.
        temperature    : Creativity level.
        max_output_tokens: Token limit per response.

    Returns:
        The assistant's reply as a plain string.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = _get_client()

    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )

    # Build the contents list for the new SDK
    # Format: [{"role": "user"/"model", "parts": [{"text": "..."}]}]
    contents = []
    for i, msg in enumerate(messages):
        role    = msg.get("role", "user")
        content = msg.get("content", "")

        # Inject system context into the very first user message
        if i == 0 and role == "user" and system_context:
            content = f"{system_context}\n\n---\n\nUser: {content}"

        contents.append(
            types.Content(
                role=role,
                parts=[types.Part(text=content)],
            )
        )

    try:
        response = client.models.generate_content(
            model=_MODEL_NAME,
            contents=contents,
            config=config,
        )
        return response.text.strip()
    except Exception as exc:
        raise RuntimeError(
            f"Chat request failed: {exc}\n"
            "Please check your API key and try again."
        )


# =============================================================
# SUB-PART 1B-iii  |  INTERNAL HELPERS
# =============================================================

def _strip_code_fences(text: str) -> str:
    """
    Remove markdown code fences and surrounding text from model output.
    Handles all common variants Gemini uses:
      ```json ... ```
      ```        ... ```
      `{ ... }`
    Also strips leading/trailing whitespace and any text before the first {.
    """
    text = text.strip()
    # Remove ```json ... ``` or ``` ... ``` wrappers
    text = re.sub(r"^```(?:json|JSON)?\s*\n?", "", text)
    text = re.sub(r"\n?\s*```\s*$", "", text)
    # Remove single-backtick inline code wrapping
    text = re.sub(r"^`|`$", "", text)
    return text.strip()


def _extract_json_block(text: str) -> str | None:
    """
    Extract the first complete JSON object { ... } from surrounding text.
    Uses greedy DOTALL match to capture nested structures.
    Handles cases where the model adds sentences before/after the JSON.
    """
    # Find the first { and the last } to get the outermost object
    start = text.find("{")
    end   = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start:end + 1]
    return None
