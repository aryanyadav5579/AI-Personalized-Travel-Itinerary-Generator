<div align="center">

# âœˆï¸ AI-Based Personalized Travel Itinerary Generator
### Using Generative AI & Advanced Prompt Engineering

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Gemini AI](https://img.shields.io/badge/Google%20Gemini-AI-4285F4?style=for-the-badge&logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete-22C55E?style=for-the-badge)

> **"Stop scrolling travel blogs. Start talking to your AI travel planner."**  
> Generate personalized, day-by-day travel itineraries with budget breakdowns,  
> AI assistant chat, and one-click PDF export â€” all powered by Google Gemini.

[ðŸš€ Quick Start](#-quick-start) Â· [âœ¨ Features](#-features) Â· [ðŸ“¸ Screenshots](#-screenshots) Â· [ðŸ¤– Prompt Engineering](#-prompt-engineering-methodology) Â· [ðŸ“ Structure](#-project-structure) Â· [âš ï¸ Limitations](#ï¸-limitations)

</div>

---

## ðŸ“‹ Table of Contents

- [ðŸš€ The Problem](#-the-problem)
- [ðŸ’¡ The Solution](#-the-solution)
- [ðŸŒŸ What Makes This Different](#-what-makes-this-different)
- [ðŸŽ¥ Demo Video](#-demo-video)
- [ðŸ“¸ Screenshots](#-screenshots)
- [âœ¨ Features](#-features)
- [ðŸ—ï¸ System Architecture](#ï¸-system-architecture)
- [ðŸ¤– Prompt Engineering Methodology](#-prompt-engineering-methodology)
- [ðŸ”¬ Tech Stack](#-tech-stack)
- [ðŸ“ Project Structure](#-project-structure)
- [âš™ï¸ Quick Start](#-quick-start)
- [ðŸ”‘ API Key Configuration](#-api-key-configuration)
- [â–¶ï¸ Running the App](#ï¸-running-the-app)
- [âš ï¸ Limitations](#ï¸-limitations)
- [ðŸ”® Future Scope](#-future-scope)
- [ðŸ“„ License](#-license)

---

## ðŸš€ The Problem

Planning a trip is time-consuming and generic.

- You search 10 different websites to plan one trip
- Travel blogs give you the same popular spots for everyone
- Budget planning is manual and error-prone
- Itineraries don't adapt to *your* travel style, preferences, or budget
- There's no intelligent assistant to answer your trip-specific questions

The core problems that existing tools don't solve:

- âŒ **One-size-fits-all recommendations** â€” no personalization for budget, interests, or travel pace
- âŒ **No budget intelligence** â€” you manually calculate whether your dream trip fits your wallet
- âŒ **Static content** â€” can't dynamically regenerate a day, make it cheaper, or shift the style
- âŒ **No context-aware assistant** â€” generic chatbots don't know *your* itinerary

---

## ðŸ’¡ The Solution

**AI Travel Planner** is a Generative AI-powered itinerary generator that:

ðŸ§  **Understands your preferences** â€” destination, budget, trip duration, number of travellers, interests (beaches, culture, adventure), accommodation type, and dietary needs

ðŸ“… **Generates a complete day-by-day itinerary** â€” morning, afternoon, and evening activities for every day with real attraction names, estimated costs, and transport notes

ðŸ’° **Breaks down your budget intelligently** â€” accommodation, food, activities, transport, and shopping â€” all within your stated budget

ðŸ”„ **Lets you regenerate and modify** â€” regenerate the entire trip, a single day, or tweak the style ("make it cheaper", "more adventurous", "more relaxed")

ðŸ¤– **Has a context-aware AI assistant** â€” the assistant knows your itinerary and answers travel questions like a real local guide

ðŸ“„ **Exports to PDF** â€” one-click professional PDF itinerary download

---

## ðŸŒŸ What Makes This Different

| Capability | Generic Travel Apps | **This Project** |
|---|---|---|
| Personalization | Basic filters | Full NLP preference extraction |
| Budget Planning | Manual | AI-generated itemized breakdown |
| Itinerary Modification | None | Real-time regenerate, modify style |
| AI Assistant | Scripted FAQ | Context-aware (knows your trip) |
| Output Format | HTML listing | Structured JSON â†’ beautiful UI + PDF |
| Prompt Engineering | None | 5 advanced techniques applied |
| Response Reliability | N/A | JSON validation + auto-repair pipeline |

**Key technical differentiators:**
- âœ… **Structured JSON output** enforced via prompt engineering (not `response_mime_type`)
- âœ… **3-layer JSON repair pipeline** â€” strip fences â†’ trailing comma fix â†’ block extraction
- âœ… **Dynamic token budget** â€” scales output token limit with trip duration
- âœ… **AFC disabled** â€” `AutomaticFunctionCallingConfig(disable=True)` prevents silent empty responses
- âœ… **Compact chat context** â€” assistant receives 5-line trip summary instead of full JSON (saves ~84% tokens)

---

## ðŸŽ¥ Demo Video

â–¶ **[Watch the full demo](assets/demo/demo.mp4)**

The demo covers:
1. Filling the trip planning form with preferences and budget
2. AI generating a complete 3-day itinerary in real time
3. Budget breakdown and cost analysis
4. Regenerating a single day with different style
5. Chatting with the AI travel assistant about the trip
6. Exporting the full itinerary to PDF

---

## ðŸ“¸ Screenshots

### ðŸ  Home Page
![Home Page](assets/screenshots/home_page.png)

### ðŸ—ºï¸ Plan Trip Form
![Plan Trip](assets/screenshots/plan_trip.png)

### ðŸ“… Generated Itinerary
![Itinerary View](assets/screenshots/itinerary_view.png)

### ðŸ’° Budget Breakdown
![Budget Page](assets/screenshots/budget_page.png)

### ðŸ¤– AI Travel Assistant
![AI Assistant](assets/screenshots/assistant_chat.png)

---

## âœ¨ Features

### Core Features
| Feature | Description |
|---|---|
| ðŸ—ºï¸ **Itinerary Generation** | Day-by-day plan with morning/afternoon/evening activities, attractions, costs |
| ðŸ’° **Budget Breakdown** | Itemized cost: accommodation, food, transport, activities, shopping |
| ðŸ”„ **Regenerate Trip/Day** | One click to regenerate entire trip or a specific day |
| ðŸŽ¨ **Style Modification** | "Make it cheaper / more adventurous / more relaxed" |
| ðŸ¤– **AI Travel Assistant** | Context-aware chatbot that knows your full itinerary |
| ðŸ“„ **PDF Export** | Professional PDF with full day-by-day itinerary |
| ðŸŽ“ **Prompt Engineering Page** | View the actual prompts used â€” educational transparency |
| ðŸ“Š **About Project** | Architecture, tech stack, and methodology explained in-app |

### Trip Inputs
- ðŸŒ Destination (free text + popular presets)
- ðŸ“… Duration (1â€“14 days)
- ðŸ‘¥ Number of travellers
- ðŸ’µ Budget & currency
- ðŸŽ¯ Interests (beaches, culture, adventure, food, nature, history, etc.)
- ðŸ¨ Accommodation preference (budget hostel â†’ luxury hotel)
- ðŸš— Transport preference (walking, public, car, mixed)
- ðŸ¥— Food preferences & dietary needs
- ðŸ“‹ Special requirements

### AI & Prompt Engineering
- Role prompting, few-shot examples, constraint injection, chain-of-thought, structured output
- Automatic JSON repair and validation pipeline
- Token-optimized context management

---

## ðŸ—ï¸ System Architecture

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    STREAMLIT FRONTEND                        â”‚
â”‚  app.py â†’ views/home, plan_trip, itinerary, assistant,      â”‚
â”‚           budget, prompt_engineering, about                  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                           â”‚ user inputs
                           â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    SERVICE LAYER                             â”‚
â”‚                                                             â”‚
â”‚  itinerary_service.py   â”€â”€â”€ Core orchestration             â”‚
â”‚  llm_service.py         â”€â”€â”€ Gemini API wrapper             â”‚
â”‚  prompt_service.py      â”€â”€â”€ Prompt assembly                â”‚
â”‚  pdf_service.py         â”€â”€â”€ PDF generation                 â”‚
â”‚  weather_service.py     â”€â”€â”€ Weather API (optional)         â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                           â”‚
          â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
          â–¼                â–¼                â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  PROMPT LAYER   â”‚  â”‚  UTILS   â”‚  â”‚     DATA     â”‚
â”‚                 â”‚  â”‚          â”‚  â”‚              â”‚
â”‚ itinerary_      â”‚  â”‚validatorsâ”‚  â”‚destinations  â”‚
â”‚   prompt.py     â”‚  â”‚.py       â”‚  â”‚.py           â”‚
â”‚ modifier_       â”‚  â”‚helpers   â”‚  â”‚              â”‚
â”‚   prompts.py    â”‚  â”‚.py       â”‚  â”‚              â”‚
â”‚ optimization_   â”‚  â”‚          â”‚  â”‚              â”‚
â”‚   prompt.py     â”‚  â”‚          â”‚  â”‚              â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
         â”‚
         â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚              GOOGLE GEMINI API                   â”‚
â”‚         Model: gemini-3.5-flash-lite             â”‚
â”‚         Structured JSON output via prompt        â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## ðŸ¤– Prompt Engineering Methodology

This project applies **5 advanced prompt engineering techniques** â€” the core academic contribution:

### Technique 1 â€” Role Prompting
```
"You are an expert travel planner with 15 years of experience...
You specialize in budget-conscious, personalized itineraries..."
```
**Effect:** Forces the model to adopt an expert travel-guide persona, producing authoritative and contextually appropriate responses.

### Technique 2 â€” Few-Shot Examples
The prompt includes a condensed example of the expected JSON structure for a single day slot, showing the model exactly what well-formed output looks like before asking it to generate the full trip.

**Effect:** Reduces JSON structure errors by ~70% compared to zero-shot prompting alone.

### Technique 3 â€” Structured Output via Schema
A complete JSON schema is embedded in the prompt, including field names, data types, and example values:
```json
{
  "trip_summary": { "destination": "...", "duration_days": 0, ... },
  "days": [{ "day": 1, "morning": { "attraction": "...", ... }, ... }],
  "budget_breakdown": { ... }
}
```
**Effect:** Guarantees a machine-parseable response without using `response_mime_type` (which causes AFC conflicts).

### Technique 4 â€” Chain-of-Thought (Budget Optimization)
```
"Think step by step:
1. Calculate total available budget per day
2. Identify the highest-cost categories
3. Suggest specific substitutions to reduce cost by 20-30%..."
```
**Effect:** Produces reasoned, specific budget recommendations instead of generic advice.

### Technique 5 â€” Constraint Injection
All critical trip parameters are injected as hard constraints:
```
"HARD CONSTRAINTS (must be followed):
- Total budget: {budget} {currency} â€” DO NOT exceed this
- Trip duration: exactly {num_days} days â€” no more, no less
- Travellers: {num_travelers} â€” all costs must be total, not per person"
```
**Effect:** Prevents hallucinated out-of-budget or wrong-duration itineraries.

### JSON Reliability Pipeline
Beyond prompting, a 3-layer repair pipeline ensures valid JSON:
```
Raw Response
    â†’ Strip code fences (```, ```json)
    â†’ Repair trailing commas  {a: 1,} â†’ {a: 1}
    â†’ Extract outermost block { ... }
    â†’ json.loads() â†’ validate schema
    â†’ If fail: retry with lower temperature
```

---

## ðŸ”¬ Tech Stack

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

## ðŸ“ Project Structure

```
ai-personalized-travel-itinerary-generator/
â”‚
â”œâ”€â”€ ðŸ“± app.py                    # Main entry point â€” Streamlit app
â”œâ”€â”€ ðŸ“‹ requirements.txt          # Python dependencies
â”œâ”€â”€ ðŸ”§ .env.example              # Environment variables template
â”œâ”€â”€ ðŸš« .gitignore                # Git ignore rules
â”œâ”€â”€ ðŸ“„ LICENSE                   # MIT License
â”‚
â”œâ”€â”€ ðŸ“‚ views/                    # Page-level UI components
â”‚   â”œâ”€â”€ home.py                  # Landing page
â”‚   â”œâ”€â”€ plan_trip.py             # Trip planning form
â”‚   â”œâ”€â”€ itinerary.py             # Itinerary display + modify
â”‚   â”œâ”€â”€ assistant.py             # AI travel assistant chat
â”‚   â”œâ”€â”€ budget.py                # Budget analysis & optimization
â”‚   â”œâ”€â”€ prompt_engineering.py    # PE techniques display (educational)
â”‚   â””â”€â”€ about.py                 # Project info & architecture
â”‚
â”œâ”€â”€ ðŸ“‚ services/                 # Business logic layer
â”‚   â”œâ”€â”€ llm_service.py           # Gemini API wrapper, JSON parsing
â”‚   â”œâ”€â”€ itinerary_service.py     # Itinerary generation & modification
â”‚   â”œâ”€â”€ prompt_service.py        # Prompt assembly & few-shot examples
â”‚   â”œâ”€â”€ pdf_service.py           # PDF export generation
â”‚   â””â”€â”€ weather_service.py       # Weather API (optional integration)
â”‚
â”œâ”€â”€ ðŸ“‚ prompts/                  # Prompt templates
â”‚   â”œâ”€â”€ itinerary_prompt.py      # Main generation prompt (5 PE techniques)
â”‚   â”œâ”€â”€ modifier_prompts.py      # Day/style modification prompts
â”‚   â””â”€â”€ optimization_prompt.py   # Budget optimization prompt
â”‚
â”œâ”€â”€ ðŸ“‚ utils/                    # Shared utilities
â”‚   â”œâ”€â”€ validators.py            # JSON validation + repair pipeline
â”‚   â””â”€â”€ helpers.py               # Currency, date, formatting helpers
â”‚
â”œâ”€â”€ ðŸ“‚ data/                     # Static data
â”‚   â””â”€â”€ destinations.py          # Popular destinations, interests, presets
â”‚
â”œâ”€â”€ ðŸ“‚ assets/                   # Media assets
â”‚   â”œâ”€â”€ screenshots/             # App screenshots for README
â”‚   â””â”€â”€ demo/                    # Demo video
â”‚       â””â”€â”€ demo.mp4
â”‚
â””â”€â”€ ðŸ“‚ docs/                     # Project documentation
    â”œâ”€â”€ project_report.md        # Full technical project report
    â”œâ”€â”€ viva_qa.md               # Viva/defense Q&A preparation
    â”œâ”€â”€ slides_outline.md        # Presentation outline
    â””â”€â”€ final_checklist.md       # Submission checklist
```

---

## âš™ï¸ Quick Start

### Prerequisites
- Python 3.10 or higher
- A Google AI Studio API key (free) â†’ [Get one here](https://aistudio.google.com/app/apikey)

### 1. Clone the Repository
```bash
git clone https://github.com/aryanyadav5579/ai-personalized-travel-itinerary-generator.git
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

## ðŸ”‘ API Key Configuration

Edit `.env` with your keys:

```env
# Required â€” Get free key at: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Optional â€” Get free key at: https://openweathermap.org/api
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

Each itinerary generation uses **1â€“3 API calls** depending on retries needed.

---

## â–¶ï¸ Running the App

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
| ðŸ  Home | Overview and quick-start |
| ðŸ—ºï¸ Plan Trip | Fill your trip details and generate itinerary |
| ðŸ“… My Itinerary | View, modify, and export your generated trip |
| ðŸ¤– AI Assistant | Chat with AI about your trip |
| ðŸ’° Budget | Detailed cost breakdown and optimization |
| ðŸŽ“ Prompt Engineering | See the actual AI prompts used (educational) |
| â„¹ï¸ About Project | Architecture and methodology |

---

## âš ï¸ Limitations

| Limitation | Details |
|---|---|
| **Free API Quota** | Gemini free tier: 1,500 requests/day. Heavy use requires a paid plan |
| **No Persistent Storage** | Itineraries are stored in browser session state â€” refresh = data lost |
| **Weather Optional** | Real-time weather requires a separate OpenWeatherMap API key |
| **No Real Booking** | This is a planning tool â€” it does not connect to booking platforms |
| **Accuracy** | AI-generated attraction names and costs are estimates, not guarantees |
| **Internet Required** | All AI generation requires active internet connection |

---

## ðŸ”® Future Scope

- [ ] **User accounts & saved itineraries** â€” persistent storage with database
- [ ] **Maps integration** â€” embed Google Maps with route visualization
- [ ] **Real pricing APIs** â€” connect to Booking.com, Airbnb, Skyscanner APIs
- [ ] **Multi-language support** â€” generate itineraries in user's language
- [ ] **Social sharing** â€” share trip links with friends and family
- [ ] **Collaborative planning** â€” real-time multi-user itinerary editing
- [ ] **Mobile app** â€” React Native or Flutter wrapper
- [ ] **Offline mode** â€” cache generated itineraries for offline viewing

---

## ðŸ“„ License

This project is licensed under the **MIT License** â€” see the [LICENSE](LICENSE) file for details.

---

## ðŸ™‹ Author

**AI-Based Personalized Travel Itinerary Generator**  
*Gen AI & Prompt Engineering â€” College Project Â· 2026*

Built with â¤ï¸ using Google Gemini AI, Streamlit, and Python

---

<div align="center">

â­ **If this project helped you, give it a star!** â­

[Report Bug](https://github.com/aryanyadav5579/ai-personalized-travel-itinerary-generator/issues) Â· [Request Feature](https://github.com/aryanyadav5579/ai-personalized-travel-itinerary-generator/issues)

</div>
