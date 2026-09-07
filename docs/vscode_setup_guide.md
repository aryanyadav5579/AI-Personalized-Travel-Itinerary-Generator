# 🚀 Complete VS Code Setup Guide
## AI Travel Planner — Step-by-Step from Zero to Running

---

## STEP 1 — Install Required Software

### 1A. Install Python 3.10 or higher
1. Go to 👉 https://www.python.org/downloads/
2. Click **"Download Python 3.12.x"** (latest stable)
3. Run the installer
4. ⚠️ **IMPORTANT:** On the first screen, tick **"Add Python to PATH"** before clicking Install
5. Click **"Install Now"**

**Verify Python installed:**
Open Command Prompt or PowerShell and type:
```bash
python --version
```
You should see: `Python 3.12.x`

---

### 1B. Install VS Code
1. Go to 👉 https://code.visualstudio.com/
2. Download and install for Windows
3. Launch VS Code

---

### 1C. Install VS Code Extensions
Inside VS Code, click the **Extensions icon** on the left sidebar (or press `Ctrl+Shift+X`) and install:

| Extension | Purpose |
|-----------|---------|
| **Python** (by Microsoft) | Python language support, IntelliSense |
| **Pylance** (by Microsoft) | Better type checking and autocomplete |

> Search for "Python" → click the one by Microsoft → Install

---

## STEP 2 — Open the Project in VS Code

1. Open VS Code
2. Go to **File → Open Folder**
3. Navigate to `D:\gen ai\travel-ai-planner`
4. Click **"Select Folder"**

You will now see all project files in the left panel.

---

## STEP 3 — Open the Terminal in VS Code

Press **`` Ctrl + ` ``** (backtick key, below Escape) to open the integrated terminal.

> Make sure the terminal shows the path ending in `travel-ai-planner>`  
> Example: `PS D:\gen ai\travel-ai-planner>`

---

## STEP 4 — Create a Virtual Environment

A virtual environment keeps project dependencies separate from your system Python. **Always do this.**

In the VS Code terminal, type:

```bash
python -m venv venv
```

This creates a `venv/` folder inside your project. It takes 10–30 seconds.

---

## STEP 5 — Activate the Virtual Environment

```bash
venv\Scripts\activate
```

After activation, your terminal prompt changes to show `(venv)` at the start:
```
(venv) PS D:\gen ai\travel-ai-planner>
```

> ⚠️ If you see an error like "running scripts is disabled", run this once:
> ```bash
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
> Then try activating again.

---

## STEP 6 — Select the Virtual Environment in VS Code

1. Press **`Ctrl+Shift+P`** to open the Command Palette
2. Type: **`Python: Select Interpreter`**
3. Click it
4. Choose the one that says **`venv`** — it looks like:
   ```
   Python 3.12.x ('venv': venv)  D:\gen ai\travel-ai-planner\venv\Scripts\python.exe
   ```

> This makes sure VS Code uses your project's Python, not the system one.

---

## STEP 7 — Install All Dependencies

With the virtual environment **activated** (you see `(venv)` in terminal), run:

```bash
pip install -r requirements.txt
```

This installs all 8 packages:
- `streamlit` — the web UI framework
- `google-genai` — Google Gemini AI SDK
- `python-dotenv` — loads the `.env` file
- `reportlab` — PDF generation
- `plotly` — interactive charts
- `pandas` — data tables
- `Pillow` — image support
- `requests` — HTTP requests (weather API)

**This takes 2–5 minutes.** You will see packages downloading.

**Verify everything installed correctly:**
```bash
pip list
```

You should see all 8 packages (plus their dependencies) listed.

---

## STEP 8 — Set Up Your API Key

### 8A. Get a Free Gemini API Key
1. Go to 👉 https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key (starts with `AIza...`)

### 8B. Create the `.env` File
In VS Code, look at the files panel on the left. You will see `.env.example`.

**Option A — From terminal:**
```bash
copy .env.example .env
```

**Option B — Manually:**
1. Right-click in the file panel → **New File**
2. Name it exactly: `.env`
3. Type inside:
```
GEMINI_API_KEY=AIzaSy...paste_your_key_here
WEATHER_API_KEY=your_weather_api_key_here
```

> The `.env` file is already in `.gitignore` — it will never be uploaded to GitHub by accident.

### 8C. Verify the Key Works
In the terminal:
```bash
python -c "from services.llm_service import is_api_configured; print('API Ready:', is_api_configured())"
```
You should see: `API Ready: True`

---

## STEP 9 — Run the App

```bash
streamlit run app.py
```

VS Code terminal will show:
```
  You can now view your Streamlit app in your browser.
  Local URL:  http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Your browser should open **automatically**. If not, open it manually and go to:
```
http://localhost:8501
```

**The app is running! 🎉**

---

## STEP 10 — Stop the App

In the VS Code terminal, press:
```
Ctrl + C
```

---

## 🔁 Daily Workflow (Every Time You Open VS Code)

Every time you open the project again:

```bash
# Step 1 — Activate virtual environment
venv\Scripts\activate

# Step 2 — Run the app
streamlit run app.py
```

That's it — just 2 commands every session.

---

## 📁 Understanding the Project Structure

```
D:\gen ai\travel-ai-planner\
│
├── app.py                  ← START HERE — the main file (run this)
├── .env                    ← YOUR API KEYS (never share this)
├── .env.example            ← Template (safe to share)
├── requirements.txt        ← List of packages to install
│
├── pages\                  ← All 7 app pages
│   ├── home.py
│   ├── plan_trip.py
│   ├── itinerary.py
│   ├── assistant.py
│   ├── budget.py
│   ├── prompt_engineering.py
│   └── about.py
│
├── services\               ← AI + PDF + Weather logic
│   ├── llm_service.py
│   ├── itinerary_service.py
│   ├── prompt_service.py
│   ├── pdf_service.py
│   └── weather_service.py
│
├── prompts\                ← Prompt Engineering files
│   ├── itinerary_prompt.py
│   ├── optimization_prompt.py
│   └── modifier_prompts.py
│
├── utils\                  ← Helper functions
│   ├── validators.py
│   └── helpers.py
│
├── data\
│   └── destinations.py     ← Dropdown data
│
├── docs\                   ← Project report + slides + viva guide
│   ├── project_report.md
│   ├── slides_outline.md
│   ├── viva_qa.md
│   └── final_checklist.md
│
└── venv\                   ← Virtual environment (do NOT edit)
```

---

## ❗ Common Problems & Fixes

### Problem 1 — "streamlit is not recognized"
**Cause:** Virtual environment not activated  
**Fix:**
```bash
venv\Scripts\activate
streamlit run app.py
```

---

### Problem 2 — "ModuleNotFoundError: No module named 'google'"
**Cause:** Dependencies not installed in the virtual environment  
**Fix:**
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

---

### Problem 3 — "API key not found" warning in app
**Cause:** `.env` file missing or key not set  
**Fix:** Check your `.env` file has:
```
GEMINI_API_KEY=AIzaSy...your_real_key
```
Then restart the app (`Ctrl+C` then `streamlit run app.py`).

---

### Problem 4 — "running scripts is disabled" error on activation
**Cause:** Windows PowerShell security setting  
**Fix:** Run this ONCE in PowerShell as Administrator:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then activate again:
```bash
venv\Scripts\activate
```

---

### Problem 5 — Port 8501 already in use
**Cause:** Previous Streamlit session still running  
**Fix:**
```bash
streamlit run app.py --server.port 8502
```
Then open http://localhost:8502

---

### Problem 6 — Changes not reflecting in browser
**Cause:** Streamlit caches some elements  
**Fix:** Press **`R`** in the browser (hard refresh), or in the top-right corner of the app click **⋮ → Rerun**.

---

### Problem 7 — VS Code shows red underlines on imports
**Cause:** VS Code not using the venv Python  
**Fix:**
1. `Ctrl+Shift+P` → `Python: Select Interpreter`
2. Choose the `venv` entry

---

## ✅ Quick Verification Checklist

Run this to verify everything is set up correctly:

```bash
python -c "
import streamlit, plotly, pandas, reportlab
from google import genai
from dotenv import load_dotenv
from services.llm_service import is_api_configured
load_dotenv()
print('Streamlit:', streamlit.__version__)
print('Plotly:', plotly.__version__)
print('Pandas:', pandas.__version__)
print('google-genai: OK')
print('API configured:', is_api_configured())
print('ALL OK - ready to run!')
"
```

Expected output:
```
Streamlit: 1.39.0
Plotly: 6.x.x
Pandas: 2.2.x
google-genai: OK
API configured: True
ALL OK - ready to run!
```

---

## 🎯 Summary — 3 Commands to Remember

```bash
# 1. Activate virtual environment (every session)
venv\Scripts\activate

# 2. Install packages (first time only)
pip install -r requirements.txt

# 3. Run the app (every session)
streamlit run app.py
```

---

*Setup Guide · AI Travel Planner · Gen AI & Prompt Engineering · 2025*
