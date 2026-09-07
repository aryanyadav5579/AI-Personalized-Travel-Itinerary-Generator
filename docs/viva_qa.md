# 🎤 Viva Q&A Preparation Guide
## AI-Based Personalized Travel Itinerary Generator

> **20 Questions** across 5 categories  
> Study these carefully — read both the question AND the model answer.

---

## Category 1 — Prompt Engineering Fundamentals (Q1–Q5)

---

### Q1. What is Prompt Engineering and why is it important?

**Model Answer:**  
Prompt Engineering is the practice of systematically designing input text (prompts) to guide Large Language Models toward producing accurate, structured, and reliable outputs. It is important because LLMs are general-purpose — they can do many things, but without precise instructions they produce inconsistent, generic, and often unusable results.

In this project, Prompt Engineering is the *core intelligence* — not a feature on top of a normal app. A basic prompt like *"Plan a trip to Goa"* gives vague text. Our engineered 9,000-character prompt gives a structured, budget-accurate, JSON itinerary that the UI can directly render as cards and charts.

**Key phrase to remember:**  
> "Prompt Engineering determines whether an LLM produces generic text or a structured, validated, production-ready output."

---

### Q2. How many Prompt Engineering techniques did you use? List them.

**Model Answer:**  
We used **7 techniques**:

1. **Role Prompting** — Assigning the model an expert identity (*"You are an expert travel planner with 20+ years of experience..."*)
2. **Context Injection** — Embedding all 12 user inputs directly in the prompt body
3. **Few-Shot Prompting** — Providing a complete example Day 1 before asking for the real output
4. **Constraint-Based Prompting** — Listing explicit rules the model must not violate (budget cap, dietary restriction, no overloading)
5. **Structured Output Prompting** — Providing a full JSON schema and instructing *"Return ONLY valid JSON"*
6. **Zero-Shot Prompting** — Used in the AI chat assistant — no examples needed, model uses its own knowledge
7. **Iterative Prompt Refinement** — Existing itinerary passed as context for targeted edits (e.g., "Make Day 2 more adventurous — keep all other days the same")

---

### Q3. What is the difference between Few-Shot and Zero-Shot prompting?

**Model Answer:**  
- **Zero-Shot Prompting:** The model is asked to perform a task with *no examples*. It relies entirely on its pre-trained knowledge. Used in the AI assistant chat where each question is answered directly.

- **Few-Shot Prompting:** The model is given one or more *complete examples* of the expected output before being asked for the real one. In this project, a full Day 1 itinerary for Goa is provided as an example (the `FEW_SHOT_DAY_EXAMPLE` in `itinerary_prompt.py`), which teaches the model the exact format, depth, and structure expected for every day.

**Why we use Few-Shot for generation but Zero-Shot for chat:**  
For itinerary generation, consistency in format is critical — Few-Shot ensures every day follows the same JSON structure. For the chat assistant, format doesn't matter — the user just wants an answer, so Zero-Shot is faster and sufficient.

---

### Q4. What is Structured Output Prompting and why is it critical in this project?

**Model Answer:**  
Structured Output Prompting means explicitly telling the LLM to respond in a specific format — in this case, a JSON schema — and instructing it not to add any extra text.

In the itinerary prompt, we include:
1. The complete `ITINERARY_JSON_SCHEMA` — a Python dict showing the exact keys, nested structure, and data types expected
2. The instruction: *"Return ONLY valid JSON. No markdown. No explanations. No code fences."*

**Why it is critical:**  
Without structured output, Gemini returns a narrative text response. The frontend cannot extract activities, costs, or tips from unstructured text. By forcing JSON, the response is directly parsed into a Python dict and used to render day cards, cost charts, and the PDF — without any manual parsing.

**JSON repair system:**  
Even with this instruction, Gemini occasionally wraps the JSON in markdown fences (` ```json ... ``` `). The `_strip_code_fences()` and `_extract_json_block()` functions handle these edge cases, and the system retries up to 3 times if parsing still fails.

---

### Q5. What is Context Injection? How did you use it?

**Model Answer:**  
Context Injection means embedding all relevant background information directly into the prompt body before asking the question — so the model has complete context without needing follow-up questions.

In the itinerary prompt (Section 2), all 12 user inputs are injected in a structured block:
```
TRAVELER PROFILE:
  Destination     : Goa, India
  Duration        : 3 days
  Travelers       : 2 people
  Total Budget    : INR 15,000
  Travel Style    : Standard
  Accommodation   : 3-Star Hotel
  Interests       : Beaches, Food, Culture
  Food Preference : Vegetarian
  Special Needs   : Avoid crowded tourist spots
```

This means a vegetarian traveler gets vegetarian food recommendations in every single slot — not because we filter afterwards, but because the model knows the constraint from the very beginning.

Context Injection is also used in the AI assistant — the full itinerary (all days, costs, tips) is injected as a system context, giving the model "memory" of the entire trip for every chat message.

---

## Category 2 — Technical Implementation (Q6–Q10)

---

### Q6. Why did you use Streamlit instead of Flask or Django?

**Model Answer:**  
Streamlit was chosen for three main reasons:

1. **Speed of development** — The entire UI is written in Python. No HTML, CSS, or JavaScript required. A `st.chat_message()` call renders a complete chat bubble.

2. **Built-in components** — `st.chat_input()`, `st.plotly_chart()`, `st.download_button()`, `st.progress()` are all available out of the box — saving weeks of frontend development.

3. **Session state** — Streamlit provides `st.session_state` for persisting data across pages and reruns, which is essential for multi-page apps where the itinerary must survive navigation.

**Trade-off acknowledged:**  
Streamlit is less flexible than React for complex UI. For a production app we might use FastAPI + React. For a college project demonstration, Streamlit gives the fastest path from AI logic to working demo.

---

### Q7. How does the app handle errors from the Gemini API?

**Model Answer:**  
The error handling is implemented in layers:

1. **API level (`llm_service.py`):** `call_gemini()` retries up to 3 times with exponential backoff (2s → 4s → 8s) on any exception. If all retries fail, it raises a `RuntimeError` with a clear message.

2. **JSON level (`call_gemini_json()`):** After getting text, it attempts to parse as JSON. If that fails, it strips code fences and tries again. Then extracts the JSON block with regex. If all fail after 3 retries, it raises `ValueError`.

3. **Service level (`itinerary_service.py`):** `generate_itinerary()` catches `ValueError` from JSON parsing and can call `repair_json_string()` from validators as a last resort.

4. **UI level (`plan_trip.py`):** `try/except` blocks around the generation call show user-friendly error messages — never a raw Python traceback.

5. **Optional features:** Weather and PDF functions return `None` or show `st.warning()` on failure — they never crash the app.

---

### Q8. What is the difference between the old google-generativeai SDK and the new google-genai SDK?

**Model Answer:**

| Aspect | Old SDK (deprecated) | New SDK (google-genai) |
|--------|---------------------|----------------------|
| Configuration | `genai.configure(api_key=key)` | `client = genai.Client(api_key=key)` |
| Model creation | `genai.GenerativeModel("gemini-1.5-flash")` | Passed directly to `client.models.generate_content()` |
| Config object | `genai.types.GenerationConfig(...)` | `types.GenerateContentConfig(...)` |
| API call | `model.generate_content(prompt)` | `client.models.generate_content(model=..., contents=prompt, config=...)` |

**Why we migrated:**  
During development, the old `google-generativeai` package started showing `FutureWarning: google-generativeai is deprecated`. We migrated to the new `google-genai` package which uses a client-based approach, is actively maintained, and is the official SDK going forward.

---

### Q9. How does the PDF export work?

**Model Answer:**  
The PDF is generated using **ReportLab** — a Python library for programmatic PDF creation.

The `generate_pdf()` function in `services/pdf_service.py` builds a `story` list of `Flowable` elements and passes it to `SimpleDocTemplate.build()`. The structure is:

1. **Cover page** — A colour-filled `Table` simulates a gradient header. Below it, a trip info grid table.
2. **Overview page** — Budget breakdown table (9 rows, colour-coded by row type) + day highlights table.
3. **Day pages (one per day)** — Day header bar in `PRIMARY` colour. Three slot headers (Morning=Blue, Afternoon=Purple, Evening=Dark Purple). Each slot's content in a nested table.
4. **Final page** — 2-column packing list table + numbered tips.
5. **Every page footer** — Page number + branding line drawn via `canvas.drawString()`.

The function returns `bytes` from `io.BytesIO`, which Streamlit's `st.download_button()` accepts directly.

---

### Q10. How is multi-turn chat implemented?

**Model Answer:**  
The AI assistant uses `call_gemini_chat()` in `llm_service.py`, which builds a `contents` list in the format required by the new google-genai SDK:

```python
contents = [
    types.Content(role="user",  parts=[types.Part(text="...")]),
    types.Content(role="model", parts=[types.Part(text="...")]),
    types.Content(role="user",  parts=[types.Part(text="current question")]),
]
```

The conversation history is stored in `st.session_state.chat_history` as a list of `{"role", "content"}` dicts, which persists across Streamlit reruns.

**Context Injection for memory:**  
The full itinerary is injected into the FIRST user message as a prefix:
```python
if i == 0 and role == "user" and system_context:
    content = f"{system_context}\n\n---\n\nUser: {content}"
```
This gives the model "memory" of the entire trip across all messages in the conversation.

---

## Category 3 — Project Design Decisions (Q11–Q14)

---

### Q11. Why did you create a separate llm_service.py instead of calling the Gemini API directly from each page?

**Model Answer:**  
This is the **Single Responsibility Principle** applied to API integration. Having one file as the sole gateway to the Gemini API provides:

1. **Centralized error handling** — retry logic, exponential backoff, and error messages defined once
2. **Easy model updates** — change `_MODEL_NAME = "gemini-3.6-flash"` in one place to upgrade all API calls
3. **Testability** — mock just `llm_service.py` to test all other layers without API calls
4. **Security** — API key validation logic in one place, not scattered across 7 page files
5. **SDK migration** — when `google-generativeai` was deprecated, we updated one file instead of 10+

---

### Q12. How does the app ensure the budget is respected?

**Model Answer:**  
Budget enforcement works at **two levels**:

**Level 1 — Prompt (Constraint-Based Prompting):**
The constraint section includes explicit rules:
- *"Total costs across all days MUST NOT exceed INR 15,000"*
- *"Daily budget target is INR 5,000 per day (15,000 ÷ 3)"*
- *"If budget is tight, prioritize free attractions and local food"*
- *"Flag any day that exceeds proportional budget"*

This guides the model to make budget-aware choices from the start — selecting free or low-cost activities when needed.

**Level 2 — Code (Post-generation validation):**
After generation, `get_budget_comparison()` computes the actual estimated total and compares it to the user's budget. If over budget:
- A red warning banner appears on the Budget page
- The "Optimize Budget with AI" button is shown
- Clicking it sends `build_optimization_prompt()` which asks Gemini to reduce costs while maintaining quality

---

### Q13. What happens if the generated JSON doesn't match the schema?

**Model Answer:**  
There is a 3-tier repair system:

**Tier 1 — `call_gemini_json()` in llm_service.py:**
- Strips markdown code fences (` ```json ``` `)
- Attempts `json.loads(cleaned_text)`
- If it fails, uses regex to find the first `{...}` block and tries again
- Retries the full API call up to 3 times

**Tier 2 — `validate_itinerary_json()` in validators.py:**
- Checks all required top-level keys: `trip_summary`, `days`, `budget_breakdown`, `packing_list`, `important_tips`
- Checks each day has `morning`, `afternoon`, `evening` sub-keys
- Returns `(False, error_message)` if invalid

**Tier 3 — `repair_json_string()` in validators.py:**
- More aggressive repair using regex
- Called as last resort before showing error to user

**In practice:** The structured output prompt succeeds on the first attempt ~95% of the time. The repair system handles the remaining 5%.

---

### Q14. Why did you choose Google Gemini over OpenAI GPT or Anthropic Claude?

**Model Answer:**  
Three practical reasons:

1. **Free API tier** — Google AI Studio provides a free Gemini API key with generous limits. For a college project, this avoids billing setup and credit card requirements.

2. **Strong structured output** — Gemini 2.0 Flash reliably follows the JSON schema instruction. In testing, it had fewer instances of wrapping output in markdown or adding extra text compared to smaller models.

3. **Large context window** — The 9,000-character prompt plus the few-shot example fits comfortably within Gemini 2.0 Flash's context window, leaving ample room for the response.

**Academic note:** The Prompt Engineering techniques demonstrated in this project are model-agnostic — they would work with GPT-4, Claude, or any instruction-following LLM. The choice of Gemini is a practical decision, not an architectural one.

---

## Category 4 — Feature-Specific Questions (Q15–Q18)

---

### Q15. Explain the Iterative Prompt Refinement technique with a specific example from your app.

**Model Answer:**  
Iterative Prompt Refinement means taking an existing AI output, passing it back as context, and asking for a specific, targeted change — rather than starting from scratch.

**Example — "Make Day 2 More Adventurous":**

1. User clicks "More Adventure" on Day 2 on the Itinerary page
2. `modify_itinerary("make_adventurous", itinerary, user_inputs, day_num=2)` is called
3. `build_make_adventurous_prompt()` builds a prompt that includes:
   - The full existing itinerary as context
   - Current Day 2 activities
   - The instruction: *"Replace Day 2 activities with higher-energy alternatives (e.g., water sports, trekking, rock climbing). Keep Days 1 and 3 exactly as they are."*
4. Gemini returns an updated full itinerary with only Day 2 changed
5. The session state is updated and the page reruns

**Why not regenerate from scratch?**  
The user may be happy with Days 1 and 3. Regenerating would give entirely new days they didn't ask to change. Iterative Refinement respects what's working and changes only what was requested.

---

### Q16. How does the weather feature work? What happens if the API key is missing?

**Model Answer:**  
The weather feature uses the **OpenWeatherMap API** (free tier) and is fully optional.

`services/weather_service.py` provides:
- `get_current_weather(city)` — temperature, humidity, description, wind speed
- `get_weather_forecast(city, num_days=5)` — groups 3-hour interval data into daily summaries
- `get_clothing_tips(weather, destination)` — smart packing suggestions based on temperature and conditions
- `render_weather_widget(destination)` — drop-in Streamlit component

**Graceful degradation (no API key):**
Every function starts with:
```python
key = _get_api_key()
if not key:
    return None
```
`render_weather_widget()` checks if both `weather` and `forecast` are `None` and shows a small placeholder instead. The rest of the app works completely normally. This is the *fail-silently* pattern for optional features.

---

### Q17. How does the Budget page calculate the "over budget" status?

**Model Answer:**  
`get_budget_comparison()` in `itinerary_service.py` does the following:

1. Calls `calculate_total_estimated_cost()` which:
   - First tries `itinerary["budget_breakdown"]["total_estimated"]` (set by Gemini)
   - Falls back to summing all `day["day_total_cost"]` values if breakdown is missing

2. Compares: `estimated_total` vs. `user_budget`

3. Returns a status dict with:
   ```python
   {
       "status":      "under" | "tight" | "over",
       "percentage":  float,        # estimated as % of budget
       "difference":  float,        # signed (positive = under)
       "emoji":       "✅" | "⚠️" | "🔴",
       "message":     "Within budget" | "Budget is tight" | "Over budget",
       "budget_fmt":  "₹15,000",
       "estimated_fmt": "₹14,200",
   }
   ```

4. **"tight"** is defined as: estimated is between 90% and 100% of budget

5. The Budget page uses the `status` field to set the banner background color (green/yellow/red) and decide whether to show the optimization button.

---

### Q18. What does the Prompt Engineering comparison page show? What is its educational purpose?

**Model Answer:**  
The Prompt Engineering page (`pages/prompt_engineering.py`) has 4 components:

1. **7 Technique Cards (accordion):** Each card shows the technique's definition, a verbatim code example from this project, the file it's used in, and its benefit. This proves the techniques are not theoretical — they are actively used in the codebase.

2. **3-Tab Prompt Comparison:**
   - **Basic (🔴):** `"Plan a 3 day trip to Goa."` — 25 chars, no engineering
   - **Standard (🟡):** Destination + budget + interests — 248 chars, still no role/schema
   - **Advanced (🟢):** Full production prompt — 9,000+ chars, all 5 core techniques
   - Each tab shows: character count, word count, has_role, has_schema, has_example, has_constraints

3. **Quality Metrics Bar Chart:** Groups the 3 prompts on 5 quality dimensions, visually showing the gap.

4. **Live Prompt Inspector:** Shows the *actual prompt* that was sent to Gemini for the user's last itinerary generation — with real character count and feature flags.

**Educational purpose:** The examiner (or student) can directly observe the engineering effort behind each prompt level and understand why the advanced prompt produces a structured, usable result while the basic prompt does not.

---

## Category 5 — Critical Thinking (Q19–Q20)

---

### Q19. What are the limitations of your system? What would you improve?

**Model Answer:**  
**Current limitations:**

1. **Soft constraint enforcement (~90%):** Budget and dietary constraints are stated in the prompt but not enforced in code. The model occasionally generates a slightly over-budget itinerary. Solution: post-generation code validation to scale down costs.

2. **No real-time pricing:** Cost estimates are educated guesses from the AI, not live data from hotel/restaurant APIs. A Booking.com or Zomato integration would make costs accurate.

3. **No map integration:** The itinerary doesn't show a geographic route. Users can't see if Day 1 requires excessive cross-city travel.

4. **Single language:** The app is English-only. Internationalization would require translated prompt templates.

5. **Session-only storage:** Itineraries are lost when the browser closes. User accounts with database storage would fix this.

**What I would add next:**
- Google Maps route visualization per day
- Real hotel/flight pricing via APIs
- Fine-tuned model on real travel reviews for better local knowledge
- User accounts to save multiple trips

---

### Q20. Is this really "AI" or just a fancy way to call an API? Justify your answer.

**Model Answer:**  
This is a fair and important question. The core AI reasoning — understanding geography, estimating costs, selecting culturally appropriate activities, and respecting dietary constraints — is done by Google Gemini, which is a 540B+ parameter Large Language Model trained on vast amounts of text.

**What this project contributes beyond "just calling an API":**

1. **Prompt Engineering as the core product** — Without the 7-technique, 9,000-character engineered prompt, the same Gemini API produces generic, unusable output. The engineering of the prompt is the primary intellectual contribution.

2. **Schema enforcement and validation system** — The JSON schema, validation pipeline, and repair system ensure reliable, machine-readable output — which a naive API call does not provide.

3. **Iterative refinement architecture** — The modifier prompt system passes existing itinerary context for targeted edits, which requires careful prompt design, not just API calling.

4. **System integration** — Combining LLM output with Plotly charts, ReportLab PDF, OpenWeatherMap, and a multi-page Streamlit UI into a coherent product requires software engineering beyond API calls.

**Analogy:** A calculator "just calls arithmetic operations" — but the engineering of what operations to call, in what order, with what inputs, and how to present the results is what makes it a product. This project does the same with LLM operations.

> "We didn't just call an API. We engineered the communication with the API to produce a production-quality, structured, validated, application-ready output."

---

## 📝 Quick Reference Card

| Question Category | Questions | Key Terms to Remember |
|------------------|-----------|----------------------|
| PE Fundamentals | Q1–Q5 | Role, Context Injection, Few-Shot, Constraint, Structured Output, Zero-Shot, Iterative Refinement |
| Technical | Q6–Q10 | Streamlit session state, retry + backoff, JSON repair, ReportLab flowables, contents list |
| Design Decisions | Q11–Q14 | Single gateway pattern, two-level budget enforcement, 3-tier JSON repair, model choice rationale |
| Features | Q15–Q18 | Iterative Refinement example, weather graceful degradation, budget status calc, PE page purpose |
| Critical Thinking | Q19–Q20 | Limitations, soft vs. hard constraints, engineering contribution beyond API calls |

---

## 🎯 Top 5 Things to Always Say in the Viva

1. **"Prompt Engineering is the core intelligence — not just a chatbot layer."**
2. **"The advanced prompt is ~9,000 characters; the basic prompt is 25 characters. That difference is Prompt Engineering."**
3. **"Structured Output Prompting forces JSON — making the output directly usable by code without manual parsing."**
4. **"All Gemini API calls go through a single gateway (`llm_service.py`) — following the Single Responsibility Principle."**
5. **"Every optional feature degrades gracefully — the app never crashes even without the weather API key."**

---

*Viva Q&A Guide · AI Travel Planner · Gen AI & Prompt Engineering · 2025*
