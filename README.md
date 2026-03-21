# AI Talent Matcher 

An intelligent, AI-powered resume screening dashboard built with Streamlit and the Groq LLM API.

## Project Structure

```
ai_resume/
├── app.py               # Entry point — run this with streamlit
├── config.py            # Loads .env and exposes API constants
├── requirements.txt
├── .env                 # ← your secrets go here (never committed)
├── .gitignore
│
├── core/
│   ├── pdf_parser.py    # PDF text extraction
│   └── analyzer.py      # LLM call + result parsing
│
├── ui/
│   ├── styles.py        # All global CSS injection
│   ├── landing.py       # Landing page (forms + upload)
│   └── dashboard.py     # Results dashboard (filters, table, charts)
│
└── utils/
    └── helpers.py       # Shared utilities (scoring, session reset)
```

## Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure your API key**

   Create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   GROQ_API_BASE=https://api.groq.com/openai/v1
   MODEL_NAME=llama-3.1-8b-instant
   ```

3. **Run the app**
   ```bash
   streamlit run app.py
   ```

## Features

-  Upload multiple PDF resumes at once
-  AI scoring (0–100) against any job description
-  Sidebar filters (minimum score, decision type)
-  Animated metric cards and score distribution chart
-  Ranked leaderboard with hover tooltips for strengths/gaps
-  One-click Excel export of all results
-  Deep dive tab with full AI reasoning and raw PDF text