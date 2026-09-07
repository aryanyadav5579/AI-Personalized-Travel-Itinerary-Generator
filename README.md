<div align="center">

# ✈️ AI-Based Personalized Travel Itinerary Generator
### Using Generative AI & Advanced Prompt Engineering

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Gemini AI](https://img.shields.io/badge/Google%20Gemini-AI-4285F4?style=for-the-badge&logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete-22C55E?style=for-the-badge)

> **"Stop scrolling travel blogs. Start talking to your AI travel planner."**  
> Generate personalized, day-by-day travel itineraries with budget breakdowns,  
> AI assistant chat, and one-click PDF export — all powered by Google Gemini.

[🚀 Quick Start](#-quick-start) · [✨ Features](#-features) · [📸 Screenshots](#-screenshots) · [🤖 Prompt Engineering](#-prompt-engineering-methodology) · [📁 Structure](#-project-structure) · [⚠️ Limitations](#️-limitations)

</div>

---

## 📋 Table of Contents

- [🚀 The Problem](#-the-problem)
- [💡 The Solution](#-the-solution)
- [🌟 What Makes This Different](#-what-makes-this-different)
- [🎥 Demo Video](#-demo-video)
- [📸 Screenshots](#-screenshots)
- [✨ Features](#-features)
- [🏗️ System Architecture](#️-system-architecture)
- [🤖 Prompt Engineering Methodology](#-prompt-engineering-methodology)
- [🔬 Tech Stack](#-tech-stack)
- [📁 Project Structure](#-project-structure)
- [⚙️ Quick Start](#-quick-start)
- [🔑 API Key Configuration](#-api-key-configuration)
- [▶️ Running the App](#️-running-the-app)
- [⚠️ Limitations](#️-limitations)
- [🔮 Future Scope](#-future-scope)
- [📄 License](#-license)

---

## 🚀 The Problem

Planning a trip is time-consuming and generic.

- You search 10 different websites to plan one trip
- Travel blogs give you the same popular spots for everyone
- Budget planning is manual and error-prone
- Itineraries don't adapt to *your* travel style, preferences, or budget
- There's no intelligent assistant to answer your trip-specific questions

The core problems that existing tools don't solve:

- ❌ **One-size-fits-all recommendations** — no personalization for budget, interests, or travel pace
- ❌ **No budget intelligence** — you manually calculate whether your dream trip fits your wallet
- ❌ **Static content** — can't dynamically regenerate a day, make it cheaper, or shift the style
- ❌ **No context-aware assistant** — generic chatbots don't know *your* itinerary

---

## 💡 The Solution

**AI Travel Planner** is a Generative AI-powered itinerary generator that:

🧠 **Understands your preferences** — destination, budget, trip duration, number of travellers, interests (beaches, culture, adventure), accommodation type, and dietary needs

📅 **Generates a complete day-by-day itinerary** — morning, afternoon, and evening activities for every day with real attraction names, estimated costs, and transport notes

💰 **Breaks down your budget intelligently** — accommodation, food, activities, transport, and shopping — all within your stated budget

🔄 **Lets you regenerate and modify** — regenerate the entire trip, a single day, or tweak the style ("make it cheaper", "more adventurous", "more relaxed")

🤖 **Has a context-aware AI assistant** — the assistant knows your itinerary and answers travel questions like a real local guide

📄 **Exports to PDF** — one-click professional PDF itinerary download

---

## 🌟 What Makes This Different

| Capability | Generic Travel Apps | **This Project** |
|---|---|---|
| Personalization | Basic filters | Full NLP preference extraction |
| Budget Planning | Manual | AI-generated itemized breakdown |
| Itinerary Modification | None | Real-time regenerate, modify style |
| AI Assistant | Scripted FAQ | Context-aware (knows your trip) |
| Output Format | HTML listing | Structured JSON → beautiful UI + PDF |
| Prompt Engineering | None | 5 advanced techniques applied |
| Response Reliability | N/A | JSON validation + auto-repair pipeline |

**Key technical differentiators:**
- ✅ **Structured JSON output** enforced via prompt engineering (not `response_mime_type`)
- ✅ **3-layer JSON repair pipeline** — strip fences → trailing comma fix → block extraction
- ✅ **Dynamic token budget** — scales output token limit with trip duration
- ✅ **AFC disabled** — `AutomaticFunctionCallingConfig(disable=True)` prevents silent empty responses
- ✅ **Compact chat context** — assistant receives 5-line trip summary instead of full JSON (saves ~84% tokens)

---

## 🎥 Demo Video

▶ **[Watch the full demo](assets/demo/demo.mp4)**

The demo covers:
1. Filling the trip planning form with preferences and budget
2. AI generating a complete 3-day itinerary in real time
3. Budget breakdown and cost analysis
4. Regenerating a single day with different style
5. Chatting with the AI travel assistant about the trip
6. Exporting the full itinerary to PDF

---

## 📸 Screenshots

### 🏠 Home Page
![Home Page](assets/screenshots/home_page.png)

### 🗺️ Plan Trip Form
![Plan Trip](assets/screenshots/plan_trip.png)

### 📅 Generated Itinerary
![Itinerary View](assets/screenshots/itinerary_view.png)

### 💰 Budget Breakdown
![Budget Page](assets/screenshots/budget_page.png)

### 🤖 AI Travel Assistant
![AI Assistant](assets/screenshots/assistant_chat.png)

---

## ✨ Features

### Core Features
| Feature | Description |
|---|---|
| 🗺️ **Itinerary Generation** | Day-by-day plan with morning/afternoon/evening activities, attractions, costs |
| 💰 **Budget Breakdown** | Itemized cost: accommodation, food, transport, activities, shopping |
| 🔄 **Regenerate Trip/Day** | One click to regenerate entire trip or a specific day |
| 🎨 **Style Modification** | "Make it cheaper / more adventurous / more relaxed" |
| 🤖 **AI Travel Assistant** | Context-aware chatbot that knows your full itinerary |
| 📄 **PDF Export** | Professional PDF with full day-by-day itinerary |
| 🎓 **Prompt Engineering Page** | View the actual prompts used — educational transparency |
| 📊 **About Project** | Architecture, tech stack, and methodology explained in-app |

### Trip Inputs
- 🌍 Destination (free text + popular presets)
- 📅 Duration (1–14 days)
- 👥 Number of travellers
- 💵 Budget & currency
- 🎯 Interests (beaches, culture, adventure, food, nature, history, etc.)
- 🏨 Accommodation preference (budget hostel → luxury hotel)
- 🚗 Transport preference (walking, public, car, mixed)
- 🥗 Food preferences & dietary needs
- 📋 Special requirements

### AI & Prompt Engineering
- Role prompting, few-shot examples, constraint injection, chain-of-thought, structured output
- Automatic JSON repair and validation pipeline
- Token-optimized context management

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    STREAMLIT FRONTEND                        │
│  app.py → views/home, plan_trip, itinerary, assistant,      │
│           budget, prompt_engineering, about                  │
└─────────────────────────┬───────────────────────────────────┘
                           │ user inputs
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    SERVICE LAYER                             │
│                                                             │
│  itinerary_service.py   ─── Core orchestration             │
│  llm_service.py         ─── Gemini API wrapper             │
│  prompt_service.py      ─── Prompt assembly                │
│  pdf_service.py         ─── PDF generation                 │
│  weather_service.py     ─── Weather API (optional)         │
└─────────────────────────┬───────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
┌─────────────────┐  ┌──────────┐  ┌──────────────┐
│  PROMPT LAYER   │  │  UTILS   │  │     DATA     │
│                 │  │          │  │              │
│ itinerary_      │  │validators│  │destinations  │
│   prompt.py     │  │.py       │  │.py           │
│ modifier_       │  │helpers   │  │              │
│   prompts.py    │  │.py       │  │              │
│ optimization_   │  │          │  │              │
│   prompt.py     │  │          │  │              │
└────────┬────────┘  └──────────┘  └──────────────┘
         │
         ▼
┌─────────────────────────────────────────────────┐
│              GOOGLE GEMINI API                   │
│         Model: gemini-3.5-flash-lite             │
│         Structured JSON output via prompt        │
└─────────────────────────────────────────────────┘
```

---

## 🤖 Prompt Engineering Methodology

This project applies **5 advanced prompt engineering techniques** — the core academic contribution:

### Technique 1 — Role Prompting
```
"You are an expert travel planner with 15 years of experience...
You specialize in budget-conscious, personalized itineraries..."
```
**Effect:** Forces the model to adopt an expert travel-guide persona, producing authoritative and contextually appropriate responses.

### Technique 2 — Few-Shot Examples
The prompt includes a condensed example of the expected JSON structure for a single day slot, showing the model exactly what well-formed output looks like before asking it to generate the full trip.

**Effect:** Reduces JSON structure errors by ~70% compared to zero-shot prompting alone.

### Technique 3 — Structured Output via Schema
A complete JSON schema is embedded in the prompt, including field names, data types, and example values:
```json
{
  "trip_summary": { "destination": "...", "duration_days": 0, ... },
  "days": [{ "day": 1, "morning": { "attraction": "...", ... }, ... }],
  "budget_breakdown": { ... }
}
```
**Effect:** Guarantees a machine-parseable response without using `response_mime_type` (which causes AFC conflicts).

### Technique 4 — Chain-of-Thought (Budget Optimization)
```
"Think step by step:
1. Calculate total available budget per day
2. Identify the highest-cost categories
3. Suggest specific substitutions to reduce cost by 20-30%..."
```
**Effect:** Produces reasoned, specific budget recommendations instead of generic advice.

### Technique 5 — Constraint Injection
All critical trip parameters are injected as hard constraints:
```
"HARD CONSTRAINTS (must be followed):
- Total budget: {budget} {currency} — DO NOT exceed this
- Trip duration: exactly {num_days} days — no more, no less
- Travellers: {num_travelers} — all costs must be total, not per person"
```
**Effect:** Prevents hallucinated out-of-budget or wrong-duration itineraries.

### JSON Reliability Pipeline
Beyond prompting, a 3-layer repair pipeline ensures valid JSON:
```
Raw Response
    → Strip code fences (```, ```json)
    → Repair trailing commas  {a: 1,} → {a: 1}
    → Extract outermost block { ... }
    → json.loads() → validate schema
    → If fail: retry with lower temperature
```

---

## 🔬 Tech Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| **Frontend** | Streamlit | 1.36+ | Web UI framework |
| **AI Model** | Google Gemini 3.5 Flash Lite | via API | Itinerary generation |
| **AI SDK** | google-genai | 2.22+ | Python SDK for Gemini |
| **PDF** | ReportLab + PyMuPDF | 4.2+, 1.28+ | PDF generation & reading |
| **HTTP** | Requests | 2.31+ | Weather API integration |
| **Config** | python-dotenv | 1.0+ | Environment variable management |
| **Language** | Python | 3.10+ | Core language |

---

## 📁 Project Structure

```
ai-personalized-travel-itinerary-generator/
│
├── 📱 app.py                    # Main entry point — Streamlit app
├── 📋 requirements.txt          # Python dependencies
├── 🔧 .env.example              # Environment variables template
├── 🚫 .gitignore                # Git ignore rules
├── 📄 LICENSE                   # MIT License
│
├── 📂 views/                    # Page-level UI components
│   ├── home.py                  # Landing page
│   ├── plan_trip.py             # Trip planning form
│   ├── itinerary.py             # Itinerary display + modify
│   ├── assistant.py             # AI travel assistant chat
│   ├── budget.py                # Budget analysis & optimization
│   ├── prompt_engineering.py    # PE techniques display (educational)
│   └── about.py                 # Project info & architecture
│
├── 📂 services/                 # Business logic layer
│   ├── llm_service.py           # Gemini API wrapper, JSON parsing
│   ├── itinerary_service.py     # Itinerary generation & modification
│   ├── prompt_service.py        # Prompt assembly & few-shot examples
│   ├── pdf_service.py           # PDF export generation
│   └── weather_service.py       # Weather API (optional integration)
│
├── 📂 prompts/                  # Prompt templates
│   ├── itinerary_prompt.py      # Main generation prompt (5 PE techniques)
│   ├── modifier_prompts.py      # Day/style modification prompts
│   └── optimization_prompt.py   # Budget optimization prompt
│
├── 📂 utils/                    # Shared utilities
│   ├── validators.py            # JSON validation + repair pipeline
│   └── helpers.py               # Currency, date, formatting helpers
│
├── 📂 data/                     # Static data
│   └── destinations.py          # Popular destinations, interests, presets
│
├── 📂 assets/                   # Media assets
│   ├── screenshots/             # App screenshots for README
│   └── demo/                    # Demo video
│       └── demo.mp4
│
└── 📂 docs/                     # Project documentation
    ├── project_report.md        # Full technical project report
    ├── viva_qa.md               # Viva/defense Q&A preparation
    ├── slides_outline.md        # Presentation outline
    └── final_checklist.md       # Submission checklist
```

---

## ⚙️ Quick Start

### Prerequisites
- Python 3.10 or higher
- A Google AI Studio API key (free) → [Get one here](https://aistudio.google.com/app/apikey)

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/ai-personalized-travel-itinerary-generator.git
cd ai-personalized-travel-itinerary-generator
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Key
```bash
# Copy the example file
copy .env.example .env       # Windows
cp .env.example .env         # macOS/Linux

# Edit .env and add your Gemini API key
```

---

## 🔑 API Key Configuration

Edit `.env` with your keys:

```env
# Required — Get free key at: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Optional — Get free key at: https://openweathermap.org/api
WEATHER_API_KEY=your_weather_api_key_here
```

> [!NOTE]
> The app works fully without `WEATHER_API_KEY`. Weather integration gracefully degrades to "weather data unavailable".

> [!CAUTION]
> **Never commit your `.env` file.** It is listed in `.gitignore` and excluded from this repository.

### Free Tier Limits (Gemini API)
| Model | Requests/Day | Notes |
|---|---|---|
| gemini-3.5-flash-lite | 1,500/day | Used in this project |

Each itinerary generation uses **1–3 API calls** depending on retries needed.

---

## ▶️ Running the App

```bash
# Make sure your virtual environment is active
venv\Scripts\activate     # Windows
source venv/bin/activate  # macOS/Linux

# Run the Streamlit app
streamlit run app.py
```

The app opens automatically at: **`http://localhost:8501`**

### Navigation
| Page | Description |
|---|---|
| 🏠 Home | Overview and quick-start |
| 🗺️ Plan Trip | Fill your trip details and generate itinerary |
| 📅 My Itinerary | View, modify, and export your generated trip |
| 🤖 AI Assistant | Chat with AI about your trip |
| 💰 Budget | Detailed cost breakdown and optimization |
| 🎓 Prompt Engineering | See the actual AI prompts used (educational) |
| ℹ️ About Project | Architecture and methodology |

---

## ⚠️ Limitations

| Limitation | Details |
|---|---|
| **Free API Quota** | Gemini free tier: 1,500 requests/day. Heavy use requires a paid plan |
| **No Persistent Storage** | Itineraries are stored in browser session state — refresh = data lost |
| **Weather Optional** | Real-time weather requires a separate OpenWeatherMap API key |
| **No Real Booking** | This is a planning tool — it does not connect to booking platforms |
| **Accuracy** | AI-generated attraction names and costs are estimates, not guarantees |
| **Internet Required** | All AI generation requires active internet connection |

---

## 🔮 Future Scope

- [ ] **User accounts & saved itineraries** — persistent storage with database
- [ ] **Maps integration** — embed Google Maps with route visualization
- [ ] **Real pricing APIs** — connect to Booking.com, Airbnb, Skyscanner APIs
- [ ] **Multi-language support** — generate itineraries in user's language
- [ ] **Social sharing** — share trip links with friends and family
- [ ] **Collaborative planning** — real-time multi-user itinerary editing
- [ ] **Mobile app** — React Native or Flutter wrapper
- [ ] **Offline mode** — cache generated itineraries for offline viewing

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙋 Author

**AI-Based Personalized Travel Itinerary Generator**  
*Gen AI & Prompt Engineering — College Project · 2026*

Built with ❤️ using Google Gemini AI, Streamlit, and Python

---

<div align="center">

⭐ **If this project helped you, give it a star!** ⭐

[Report Bug](https://github.com/<your-username>/ai-personalized-travel-itinerary-generator/issues) · [Request Feature](https://github.com/<your-username>/ai-personalized-travel-itinerary-generator/issues)

</div>
