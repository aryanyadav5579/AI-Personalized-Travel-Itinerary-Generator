# 🎓 Presentation Slides Outline
## AI-Based Personalized Travel Itinerary Generator
### Using Generative AI and Prompt Engineering

> **15 Slides** · Recommended time: 12–15 minutes  
> Course: Gen AI & Prompt Engineering · 2025

---

## 📋 Slide-by-Slide Breakdown

---

### SLIDE 1 — Title Slide

**Title:** AI-Based Personalized Travel Itinerary Generator  
**Subtitle:** Using Generative AI and Prompt Engineering  
**Course:** Gen AI & Prompt Engineering  
**Year:** 2025  

**Visual:** App hero banner screenshot OR the ✈️ logo on a gradient purple background

**Speaker Notes:**  
> "Good morning/afternoon. Today we'll present our project — an AI-powered travel planning application that uses Google Gemini and Prompt Engineering to generate personalized, day-by-day travel itineraries. What makes this different from a normal travel app is that Prompt Engineering is the core engine — not just a chatbot on top."

---

### SLIDE 2 — The Problem

**Title:** Why Do We Need This?

**Left Column — Pain Points:**
- Travel planning takes hours of research
- Existing apps give generic, one-size-fits-all suggestions
- No app considers ALL your constraints at once (budget + diet + style + pace)
- Generic ChatGPT prompts produce inconsistent, non-machine-readable text

**Right Column — What Users Need:**
- Personalized plan based on MY budget, diet, interests
- Day-by-day structure, not vague suggestions
- Editable — if I don't like Day 2, change just Day 2
- Exportable as PDF for offline use

**Visual:** Side-by-side comparison — generic travel site result vs. our structured itinerary card

**Speaker Notes:**  
> "When you search for 'Goa 3-day itinerary' online, you get the same generic blog post everyone else gets. Our app generates a plan specific to YOUR budget, YOUR dietary needs, YOUR travel pace — and produces it in a structured format the UI can directly use."

---

### SLIDE 3 — Project Objective

**Title:** What We Built

**One-liner:**  
> An AI-powered web app that generates personalized day-by-day travel itineraries using 7 Prompt Engineering techniques with Google Gemini 2.0 Flash.

**Key Numbers:**
- 🗂️ **12** user inputs (destination, budget, diet, interests…)
- 🧠 **7** Prompt Engineering techniques
- 📄 **~9,000** characters in the main AI prompt
- ⚡ **~20 seconds** to generate a complete itinerary
- 📁 **25** Python files across 4 architecture layers

**Visual:** The 4-layer architecture diagram (boxes and arrows)

---

### SLIDE 4 — Live Demo — Home Page

**Title:** The Application — Home Page

**Show on screen:**
- Hero banner with CTA buttons
- 6 feature cards
- Popular destinations strip

**Points to say:**
- "Click 'View Sample Itinerary' — no API key needed for this demo"
- "6 features: Generation, Budget, Chat, Edit, PDF, PE education"

**Visual:** Screenshot of the Home page

---

### SLIDE 5 — Live Demo — Plan Trip Form

**Title:** Step 1 — Tell the AI About Your Trip

**Show on screen:**
- The 12-input form
- Live per-person budget calculator updating as you type
- Interests chip display
- Quick destination buttons

**Points to say:**
- "12 inputs captured — all of these get injected into the AI prompt"
- "The per-person calculator shows budget awareness from the first step"
- "Interests appear as chips — these drive activity selection"

**Visual:** Screenshot of the Plan Trip form

---

### SLIDE 6 — The Core — Prompt Engineering (Part 1)

**Title:** 🧠 How Prompt Engineering Powers This App

**The Key Insight (large text):**
> A 25-character prompt gives generic text.  
> A 9,000-character engineered prompt gives a structured, personalized, validated itinerary.

**The 5 Core Techniques (in the main itinerary prompt):**

| # | Technique | What It Does |
|---|-----------|-------------|
| 1 | Role Prompting | Model becomes "expert travel planner with 20+ years experience" |
| 2 | Context Injection | All 12 user inputs embedded in structured format |
| 3 | Few-Shot Prompting | Complete example Day 1 shown before asking for the real output |
| 4 | Constraint-Based | Explicit rules: budget cap, diet, max travel time, daily structure |
| 5 | Structured Output | Full JSON schema — forces machine-readable response |

**Visual:** Side-by-side code blocks: Basic prompt (1 line) vs. Advanced prompt (first 20 lines)

---

### SLIDE 7 — The Core — Prompt Engineering (Part 2)

**Title:** 🔄 Iterative Refinement + Zero-Shot

**Technique 6 — Zero-Shot Prompting:**
- Used in the **AI Assistant chat**
- No examples needed — model uses its own travel knowledge
- Context Injection still used to give it the full itinerary

**Technique 7 — Iterative Prompt Refinement:**
- Used when user clicks "Make Adventurous", "Regenerate Day 2", etc.
- Existing itinerary passed as context
- Only the target part is changed — other days preserved
- Far more efficient than full regeneration

**Visual:** Diagram showing: User clicks "Make Day 2 Adventurous" → modifier prompt builds → Gemini → updated Day 2 → merged back

---

### SLIDE 8 — Live Demo — My Itinerary Page

**Title:** Step 2 — Your AI-Generated Itinerary

**Show on screen:**
- Trip overview card (destination, budget status chip)
- Quick action buttons bar
- Day 1 expanded — Morning/Afternoon/Evening 3-column cards
- Per-day cost metrics

**Points to say:**
- "Each day has 3 time slots — structured JSON rendered as cards"
- "Click 'Make Adventurous' — AI changes activities using Iterative Refinement"
- "Budget status chip — green = under budget, red = over"

**Visual:** Screenshot of itinerary page with Day 1 expanded

---

### SLIDE 9 — Live Demo — AI Assistant Chat

**Title:** Step 3 — Ask the AI Anything About Your Trip

**Show on screen:**
- Chat interface with 10 quick question chips
- Send a question: "Which day has the highest cost?"
- Show the AI response

**Points to say:**
- "Zero-Shot Prompting — no examples needed"
- "Context Injection — AI knows your full itinerary"
- "Multi-turn — conversation history maintained across messages"

**Visual:** Screenshot of assistant page with a conversation shown

---

### SLIDE 10 — Live Demo — Budget Analysis

**Title:** Step 4 — Visual Budget Breakdown

**Show on screen:**
- Budget status banner (green/yellow/red)
- 4 metric tiles
- Donut chart — 5 expense categories
- Stacked bar chart — daily spending with budget target line

**Points to say:**
- "Donut chart: Accommodation, Food, Transport, Activities, Shopping"
- "Bar chart: Morning/Afternoon/Evening stacked per day"
- "Red dashed line = daily budget target"
- "If over budget → 'Optimize Budget with AI' button triggers optimization prompt"

**Visual:** Screenshot of budget page with both charts visible

---

### SLIDE 11 — Live Demo — Prompt Engineering Page

**Title:** 🎓 Teaching Prompt Engineering Inside the App

**Show on screen:**
- 7 technique accordion cards (expand Role Prompting)
- 3-tab prompt comparison — switch between Basic / Standard / Advanced
- Quality metrics bar chart
- Live prompt inspector showing the actual Gemini prompt

**Points to say:**
- "The Basic prompt is 25 characters — gives vague, non-usable text"
- "The Advanced prompt is 9,000+ characters — gives structured, validated JSON"
- "This chart shows all 4 quality dimensions — Advanced scores 100% on all"

**Visual:** Screenshot of PE page showing the 3-tab comparison

---

### SLIDE 12 — Architecture Deep Dive

**Title:** 🏗️ System Architecture

**The 4 Layers:**

```
Presentation Layer → Service Layer → Prompt Engineering Layer → Data/Utils Layer
```

**Key Design Decisions:**
1. **Single API Gateway:** All Gemini calls go through `llm_service.py` — easy to maintain, update, or swap models
2. **JSON Schema:** Output always validated against schema — broken JSON is auto-repaired
3. **Session State:** `st.session_state` persists itinerary across all 7 pages
4. **Graceful degradation:** Weather works without API key; sample itinerary works without Gemini key

**Visual:** The full architecture diagram with arrows

---

### SLIDE 13 — Technology Stack

**Title:** ⚙️ Technology Stack & Why

| Technology | Version | Why Chosen |
|-----------|---------|-----------|
| Streamlit | 1.39 | Python-only UI, built-in session state, instant deployment |
| Google Gemini 2.0 Flash | API | Best JSON output, free tier, large context window |
| google-genai SDK | ≥0.8 | Latest official SDK (not deprecated google-generativeai) |
| ReportLab | 4.2 | Programmatic PDF with full styling control |
| Plotly | 6.x | Interactive charts with hover and custom styling |
| Pandas | 2.2 | Budget data tables |
| python-dotenv | 1.0 | Secure API key management |

**Visual:** Logos or technology badge row

---

### SLIDE 14 — Challenges & What We Learned

**Title:** 🧗 Challenges Faced & Lessons Learned

**Challenge 1 — Inconsistent JSON Output**  
→ Solution: `_strip_code_fences()` + `_extract_json_block()` + 3-attempt retry  
→ Lesson: Always build a repair system for LLM-generated structured output

**Challenge 2 — SDK Deprecation**  
→ `google-generativeai` deprecated mid-project — migrated to `google-genai`  
→ Lesson: Pin SDK versions and monitor deprecation notices

**Challenge 3 — Budget Constraint Reliability**  
→ Soft constraints in prompts (~90% compliance) vs. hard constraints in code (100%)  
→ Lesson: Use prompts for guidance + code for enforcement

**Challenge 4 — Multi-page State in Streamlit**  
→ Streamlit is stateless by default — all state lost on page change  
→ Solution: 5 `st.session_state` keys initialized at app startup

**Visual:** 4 challenge boxes with arrows pointing to solution boxes

---

### SLIDE 15 — Conclusion & Future Work

**Title:** ✅ Conclusion & What's Next

**What We Achieved:**
- ✅ Fully functional AI travel planning web app
- ✅ 7 Prompt Engineering techniques implemented and demonstrated
- ✅ Structured, validated JSON itinerary generation
- ✅ Interactive editing with Iterative Refinement
- ✅ AI assistant, budget charts, PDF export, weather widget

**The Core Insight:**
> Prompt Engineering is not just "how you talk to an AI."  
> It is an engineering discipline that determines whether an LLM produces  
> generic text or a structured, validated, production-ready output.

**Future Enhancements:**
- 🗺️ Live map integration (Google Maps route per day)
- 💳 Real hotel/flight pricing API
- 👥 Multi-user collaborative planning
- 🌐 Multi-destination itineraries

**Visual:** App screenshot + a QR code to the running app (if deployed)

**Closing Line:**  
> "Thank you. The app is running at localhost:8501 — happy to demonstrate any feature live."

---

## 🕐 Time Guide

| Slides | Section | Time |
|--------|---------|------|
| 1–3 | Introduction + Problem + Objective | 2 min |
| 4–5 | Live Demo Part 1 (Home + Form) | 2 min |
| 6–7 | Prompt Engineering Deep Dive | 3 min |
| 8–11 | Live Demo Part 2 (Itinerary + Chat + Budget + PE page) | 4 min |
| 12–13 | Architecture + Tech Stack | 2 min |
| 14–15 | Challenges + Conclusion | 2 min |
| **Total** | | **~15 min** |

---

## 📝 Pre-Demo Checklist

Before starting the presentation:
- [ ] App is running: `streamlit run app.py`
- [ ] Browser open at `http://localhost:8501`
- [ ] `.env` file has valid `GEMINI_API_KEY`
- [ ] Sample itinerary pre-loaded (Home → "View Sample Itinerary")
- [ ] Slides open in second window / second monitor
- [ ] Internet connection stable (for live API call demo)
- [ ] Backup: Sample itinerary loaded in case API is slow

---

*Slides Outline · AI Travel Planner · Gen AI & Prompt Engineering · 2025*
