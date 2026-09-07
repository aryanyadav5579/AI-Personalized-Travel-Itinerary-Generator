"""
=============================================================
About Project Page
=============================================================
Day 4  |  Part 4F

Full project documentation page — designed for college viva
and presentation. Covers project objective, architecture,
technology stack, prompt engineering techniques, and team info.

Sub-parts:
  4F-i    Project header + course info
  4F-ii   Objectives and problem statement
  4F-iii  Technology stack table
  4F-iv   System architecture diagram (text-based)
  4F-v    Prompt engineering techniques summary table
  4F-vi   File structure explorer
  4F-vii  How to run (setup instructions)
  4F-viii Team / submission info
=============================================================
"""

import streamlit as st


def render():
    """Render the About Project page."""

    # ==========================================================
    # SUB-PART 4F-i  |  PROJECT HEADER
    # ==========================================================
    st.markdown("""
    <div class="hero-banner" style="padding:2rem 2.5rem;">
        <div style="font-size:2.2rem; margin-bottom:0.4rem;">📖</div>
        <h1 style="font-size:1.9rem;">About This Project</h1>
        <p style="font-size:0.95rem;">
            AI-Based Personalized Travel Itinerary Generator<br>
            Using Generative AI and Prompt Engineering
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Course badge row
    badge_cols = st.columns(4)
    badges = [
        ("📚", "Course",   "Gen AI & Prompt Engineering"),
        ("🏫", "Level",    "College / University Project"),
        ("🤖", "Core AI",  "Google Gemini 2.0 Flash"),
        ("📅", "Year",     "2026"),
    ]
    for col, (icon, label, value) in zip(badge_cols, badges):
        with col:
            st.markdown(f"""
            <div style="
                background:#f8f9ff; border:1px solid #e2e8f0;
                border-radius:10px; padding:0.8rem; text-align:center;
            ">
                <div style="font-size:1.5rem;">{icon}</div>
                <div style="font-size:0.72rem; color:#94a3b8; margin-top:0.2rem;">{label}</div>
                <div style="font-size:0.85rem; font-weight:600; color:#2d3748;">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================================
    # SUB-PART 4F-ii  |  OBJECTIVES & PROBLEM STATEMENT
    # ==========================================================
    tab_obj, tab_arch, tab_tech, tab_pe, tab_files, tab_run, tab_team = st.tabs([
        "🎯 Objectives",
        "🏗️ Architecture",
        "⚙️ Tech Stack",
        "🧠 Prompt Engineering",
        "📁 File Structure",
        "🚀 How to Run",
        "👥 Team",
    ])

    # ── OBJECTIVES TAB ────────────────────────────────────────
    with tab_obj:
        st.markdown("### 🎯 Project Objective")
        st.markdown("""
        <div class="info-banner">
            This project demonstrates that Generative AI can be used as a
            <strong>core intelligence engine</strong> — not just a chatbot — to produce
            structured, personalized, and contextually accurate outputs through
            systematic prompt engineering.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### Problem Statement")
        st.markdown("""
        Planning a travel itinerary is time-consuming and requires knowledge of:
        - Local attractions, their opening times and entry costs
        - Geographic proximity of places to avoid excessive travel
        - Budget allocation across accommodation, food, transport, and activities
        - Dietary, pace, and style preferences of each traveler

        **Existing solutions** provide generic itineraries that ignore individual
        preferences. This project solves that by using **Prompt Engineering** to
        instruct Gemini AI to produce a fully personalized, structured, and
        budget-accurate itinerary.
        """)

        st.markdown("#### ✅ Objectives Achieved")
        objectives = [
            "Generate a complete day-by-day travel itinerary using Generative AI",
            "Apply 7 distinct Prompt Engineering techniques in one application",
            "Produce structured JSON output that is directly usable by the frontend",
            "Respect user's budget, dietary needs, and travel style constraints",
            "Allow iterative refinement — edit, optimize, or regenerate any part",
            "Provide an AI travel assistant for follow-up questions",
            "Export the itinerary as a professional PDF",
            "Educate users on how Prompt Engineering works (PE page)",
        ]
        for i, obj in enumerate(objectives, 1):
            st.markdown(f"**{i}.** {obj}")

    # ── ARCHITECTURE TAB ─────────────────────────────────────
    with tab_arch:
        st.markdown("### 🏗️ System Architecture")

        st.markdown("""
        The application follows a **3-layer architecture**:
        """)

        st.markdown("""
        ```
        ┌─────────────────────────────────────────────────────────────┐
        │                     PRESENTATION LAYER                      │
        │                     (pages/ + app.py)                       │
        │                                                             │
        │  home.py  plan_trip.py  itinerary.py  assistant.py          │
        │  budget.py  prompt_engineering.py  about.py                 │
        └───────────────────────┬─────────────────────────────────────┘
                                │ calls
        ┌───────────────────────▼─────────────────────────────────────┐
        │                     SERVICE LAYER                           │
        │                     (services/)                             │
        │                                                             │
        │  itinerary_service.py   prompt_service.py                   │
        │  pdf_service.py         weather_service.py                  │
        │  llm_service.py  ◄──── ALL Gemini API calls go here         │
        └───────────────────────┬─────────────────────────────────────┘
                                │ calls
        ┌───────────────────────▼─────────────────────────────────────┐
        │                  PROMPT ENGINEERING LAYER                   │
        │                     (prompts/)                              │
        │                                                             │
        │  itinerary_prompt.py    optimization_prompt.py              │
        │  modifier_prompts.py    (7 prompt engineering techniques)   │
        └───────────────────────┬─────────────────────────────────────┘
                                │ uses
        ┌───────────────────────▼─────────────────────────────────────┐
        │                     DATA / UTILS LAYER                      │
        │                                                             │
        │  utils/validators.py    utils/helpers.py                   │
        │  data/destinations.py   .env (API keys)                    │
        └─────────────────────────────────────────────────────────────┘
        ```
        """)

        st.markdown("#### Data Flow")
        st.markdown("""
        1. **User fills the form** → `pages/plan_trip.py` collects 12 inputs
        2. **Form validated** → `utils/validators.validate_user_inputs()`
        3. **Prompt built** → `prompts/itinerary_prompt.build_itinerary_prompt()`
           applies all 5 core PE techniques to create a ~9,000 character prompt
        4. **Sent to Gemini** → `services/llm_service.call_gemini_json()`
        5. **Response validated** → `utils/validators.validate_itinerary_json()`
           repairs if needed → `repair_json_string()`
        6. **Stored in session state** → displayed on `pages/itinerary.py`
        7. **Edit actions** → `services/itinerary_service.modify_itinerary()`
           uses Iterative Refinement prompts from `prompts/modifier_prompts.py`
        """)

    # ── TECH STACK TAB ────────────────────────────────────────
    with tab_tech:
        st.markdown("### ⚙️ Technology Stack")

        import pandas as pd
        tech_data = {
            "Component": [
                "Frontend Framework",
                "AI / LLM",
                "AI SDK",
                "PDF Generation",
                "Charts & Visualization",
                "Data Manipulation",
                "Image Processing",
                "HTTP Requests",
                "Environment Config",
                "Language",
            ],
            "Technology": [
                "Streamlit 1.39",
                "Google Gemini 2.0 Flash",
                "google-genai (New SDK)",
                "ReportLab 4.2",
                "Plotly 6.x",
                "Pandas 2.2",
                "Pillow 10.x",
                "requests 2.32",
                "python-dotenv 1.0",
                "Python 3.10+",
            ],
            "Why Chosen": [
                "Rapid prototyping, no HTML/CSS/JS needed, runs in browser",
                "Best-in-class LLM for structured JSON output and instruction following",
                "Latest official SDK — replaces deprecated google-generativeai",
                "Programmatic PDF creation with professional styling",
                "Interactive charts (donut, stacked bar) with hover",
                "Budget tables and data manipulation",
                "Future image support for destination photos",
                "Weather API and external HTTP calls",
                "Secure API key management without hardcoding",
                "Modern type hints, f-strings, match statements",
            ],
        }
        st.dataframe(pd.DataFrame(tech_data), use_container_width=True, hide_index=True)

    # ── PROMPT ENGINEERING TAB ────────────────────────────────
    with tab_pe:
        st.markdown("### 🧠 Prompt Engineering Techniques")
        st.markdown("Summary of all 7 techniques used — with file references:")

        import pandas as pd
        pe_data = {
            "Technique": [
                "1. Role Prompting",
                "2. Context Injection",
                "3. Few-Shot Prompting",
                "4. Constraint-Based",
                "5. Structured Output",
                "6. Zero-Shot",
                "7. Iterative Refinement",
            ],
            "Definition": [
                "Give the model an expert identity before asking anything",
                "Embed all relevant background data directly in the prompt",
                "Show one complete example output before requesting the real one",
                "Explicitly list rules the model must not violate",
                "Specify exact output format (JSON schema) the model must follow",
                "Ask a question with no examples — model uses its own knowledge",
                "Pass existing output as context and ask for targeted changes",
            ],
            "Used In": [
                "All 3 prompt files — Section 1",
                "itinerary_prompt.py Section 2, modifier_prompts.py",
                "itinerary_prompt.py Section 3 (FEW_SHOT_DAY_EXAMPLE)",
                "itinerary_prompt.py Section 4, optimization_prompt.py",
                "itinerary_prompt.py Section 5 (ITINERARY_JSON_SCHEMA)",
                "itinerary_service.py — ask_assistant() chat",
                "modifier_prompts.py, optimization_prompt.py",
            ],
            "Impact": [
                "Produces expert-level, domain-specific responses",
                "Gives personalized, accurate itinerary for each traveler",
                "Consistent day formatting & level of detail across all days",
                "Prevents budget violations, diet issues, overloaded schedules",
                "JSON returned directly — no manual parsing needed",
                "Fast Q&A in chat without needing examples every time",
                "Targeted edits without regenerating the full itinerary",
            ],
        }
        st.dataframe(pd.DataFrame(pe_data), use_container_width=True, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="
            background:#f0fdf4; border-left:4px solid #38a169;
            border-radius:0 8px 8px 0; padding:0.8rem 1rem;
        ">
            <strong>Key Insight for Viva:</strong><br>
            The difference between a <em>basic prompt</em> ("Plan a trip to Goa")
            and our <em>advanced prompt</em> (~9,000 characters with 5 techniques)
            is not just length — it is the <strong>precision, structure, and constraints</strong>
            that eliminate ambiguity and guide the model to a specific, usable output.
        </div>
        """, unsafe_allow_html=True)

    # ── FILE STRUCTURE TAB ────────────────────────────────────
    with tab_files:
        st.markdown("### 📁 Project File Structure")
        st.markdown("""
        ```
        travel-ai-planner/
        │
        ├── app.py                          # Main entry point + CSS + routing
        │
        ├── pages/                          # One file per app page
        │   ├── home.py                     # Landing page + destination cards
        │   ├── plan_trip.py                # Trip planning form
        │   ├── itinerary.py                # Day-by-day itinerary dashboard
        │   ├── assistant.py                # AI travel chat assistant
        │   ├── budget.py                   # Budget analysis + charts
        │   ├── prompt_engineering.py       # PE education page
        │   └── about.py                    # This page
        │
        ├── services/                       # Business logic layer
        │   ├── llm_service.py              # ALL Gemini API calls (single point)
        │   ├── itinerary_service.py        # Generate, modify, chat, budget logic
        │   ├── prompt_service.py           # Prompt comparison + PE education data
        │   ├── pdf_service.py              # ReportLab PDF export
        │   └── weather_service.py          # OpenWeatherMap integration
        │
        ├── prompts/                        # Prompt Engineering files
        │   ├── itinerary_prompt.py         # Main itinerary prompt (5 PE techniques)
        │   ├── optimization_prompt.py      # Budget optimization prompt
        │   └── modifier_prompts.py         # 7 edit action prompts
        │
        ├── utils/                          # Pure utility functions
        │   ├── validators.py               # Input + JSON validation
        │   └── helpers.py                  # Dates, currency, budget, UI helpers
        │
        ├── data/
        │   └── destinations.py             # Static dropdown data
        │
        ├── exports/                        # Generated PDFs saved here
        │
        ├── .env.example                    # API key template (safe to commit)
        ├── .env                            # Your actual keys (never commit!)
        ├── .gitignore                      # Excludes .env, exports, caches
        └── requirements.txt                # All dependencies
        ```
        """)

    # ── HOW TO RUN TAB ────────────────────────────────────────
    with tab_run:
        st.markdown("### 🚀 Setup & Run Instructions")

        st.markdown("#### Step 1 — Clone / Download the Project")
        st.code("cd travel-ai-planner", language="bash")

        st.markdown("#### Step 2 — Install Dependencies")
        st.code("pip install -r requirements.txt", language="bash")

        st.markdown("#### Step 3 — Configure Your API Key")
        st.markdown("""
        1. Copy `.env.example` to `.env`
        2. Get a **free** Gemini API key from [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
        3. Paste it in `.env`:
        """)
        st.code("GEMINI_API_KEY=AIzaSy...", language="bash")

        st.markdown("#### Step 4 — Run the App")
        st.code("streamlit run app.py", language="bash")

        st.markdown("#### Step 5 — Open in Browser")
        st.markdown("""
        Streamlit will automatically open:
        ```
        Local URL:    http://localhost:8501
        ```
        """)

        st.markdown("#### Optional — Weather Feature")
        st.markdown("""
        Get a free OpenWeatherMap API key at [openweathermap.org/api](https://openweathermap.org/api)
        and add it to `.env`:
        ```
        WEATHER_API_KEY=your_key_here
        ```
        The app works fully without this key — weather is optional.
        """)

        st.info(
            "**For Viva Demo**: Use the **'View Sample Itinerary'** button on the Home page "
            "to load a pre-built Goa itinerary without needing an API call.",
            icon="💡",
        )

    # ── TEAM TAB ─────────────────────────────────────────────
    with tab_team:
        st.markdown("### 👥 Team & Submission Details")

        st.markdown("""
        <div class="ai-card" style="padding:1.2rem;">
            <table width="100%" style="font-size:0.9rem; border-collapse:collapse;">
                <tr>
                    <td style="padding:8px; color:#718096; width:160px;"><strong>Project Title</strong></td>
                    <td style="padding:8px; color:#2d3748;">
                        AI-Based Personalized Travel Itinerary Generator<br>
                        Using Generative AI and Prompt Engineering
                    </td>
                </tr>
                <tr style="background:#f8f9ff;">
                    <td style="padding:8px; color:#718096;"><strong>Course</strong></td>
                    <td style="padding:8px; color:#2d3748;">Gen AI &amp; Prompt Engineering</td>
                </tr>
                <tr>
                    <td style="padding:8px; color:#718096;"><strong>Core Technology</strong></td>
                    <td style="padding:8px; color:#2d3748;">
                        Google Gemini 2.0 Flash API (google-genai SDK)
                    </td>
                </tr>
                <tr style="background:#f8f9ff;">
                    <td style="padding:8px; color:#718096;"><strong>Frontend</strong></td>
                    <td style="padding:8px; color:#2d3748;">Streamlit (Python)</td>
                </tr>
                <tr>
                    <td style="padding:8px; color:#718096;"><strong>PE Techniques</strong></td>
                    <td style="padding:8px; color:#2d3748;">
                        7 — Role, Context Injection, Few-Shot, Constraint-Based,
                        Structured Output, Zero-Shot, Iterative Refinement
                    </td>
                </tr>
                <tr style="background:#f8f9ff;">
                    <td style="padding:8px; color:#718096;"><strong>Total Files</strong></td>
                    <td style="padding:8px; color:#2d3748;">
                        20+ Python files across 5 layers
                    </td>
                </tr>
                <tr>
                    <td style="padding:8px; color:#718096;"><strong>Year</strong></td>
                    <td style="padding:8px; color:#2d3748;">2026</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Key innovation highlight
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea11, #764ba211);
            border: 1px solid #667eea33;
            border-radius: 12px;
            padding: 1.2rem 1.5rem;
        ">
            <div style="font-size:1rem; font-weight:700; color:#2d3748; margin-bottom:0.6rem;">
                🏆 Key Innovation
            </div>
            <div style="font-size:0.88rem; color:#4a5568; line-height:1.8;">
                Most AI travel apps use AI as a conversational chatbot layer on top of a
                regular website. This project is different — <strong>Prompt Engineering IS the
                product</strong>.<br><br>
                The entire intelligence of this app lives in 3 prompt files
                (<code>itinerary_prompt.py</code>, <code>optimization_prompt.py</code>,
                <code>modifier_prompts.py</code>) that use 7 techniques to turn 12 user
                form inputs into a structured, validated, budget-accurate, personalized
                travel plan — in a single API call.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Footer ─────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; padding: 1.5rem 0 0.5rem 0;
                color:#94a3b8; font-size:0.8rem; border-top:1px solid #e2e8f0;">
        AI Travel Planner &nbsp;·&nbsp; Built with Streamlit + Google Gemini AI &nbsp;·&nbsp;
        Gen AI &amp; Prompt Engineering Project &nbsp;·&nbsp; 2026
    </div>
    """, unsafe_allow_html=True)
