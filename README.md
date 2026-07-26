# Geopolitical Automation Pipeline

A production-focused automation pipeline that monitors fast-moving geopolitical and defense signals, rewrites them into structured briefing content, and generates social-ready assets for publishing and archival.

The goal is practical: reduce manual monitoring time while keeping the output factual, traceable, and reproducible.

## What this repository does

- Ingests RSS + web sources for geopolitical and aerospace/security events
- Filters low-signal content with keyword and relevance gates
- Uses AI fallbacks for concise summaries and captions
- Generates branded cards and captions
- Optionally uploads outputs to Google Drive
- Tracks posted links to reduce duplicates across runs

## Tech stack

- **Python 3.11+**
- **Data & scraping:** `feedparser`, `requests`, `trafilatura`, `beautifulsoup4`, `cloudscraper`, `yt-dlp`
- **AI providers:** Groq, Gemini, OpenRouter, Hugging Face (optional by environment)
- **Image rendering:** Pillow (`pillow-avif-plugin`)
- **Storage/integration:** Google Drive API
- **Automation:** GitHub Actions (`.github/workflows/*.yml`)

## Project layout

```text
.
├── main.py                      # Primary geopolitical automation pipeline
├── antigravity/
│   ├── main.py                  # Aerospace/advanced-physics automation variant
│   └── generate_logos.py        # Local logo asset generator
├── assets/                      # Maps, flags, actor icons, backgrounds
├── fonts/                       # Card typography assets
├── generate_assets.py           # Map/actor visual asset generator
├── download_flags.py            # Country flag downloader
├── generate_missing_flags.py    # Fallback flag generator
├── oauth_setup.py               # OAuth token bootstrap helper
├── exchange.py                  # OAuth code-to-token exchange helper
├── posted_links.json            # Duplicate suppression tracker
├── ai_usage.json                # AI usage tracker
├── requirements.txt
└── .github/workflows/           # Scheduled + manual automation workflows
```

## Local setup

1. **Create and activate a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**

   ```bash
   cp .env.example .env
   # then edit .env with real values
   ```

   Load variables into your shell (example):

   ```bash
   set -a
   source .env
   set +a
   ```

## Running automation manually

- **Primary pipeline:**

  ```bash
  python main.py
  ```

- **Aerospace variant:**

  ```bash
  python antigravity/main.py
  ```

Outputs are generated in `output/` (and optionally uploaded to Drive when auth is configured).

## Scheduled automation

Workflows are in `.github/workflows`:

- `geopolitics.yml` — runs every 30 minutes + manual dispatch
- `antigravity.yml` — runs every 2 hours + manual dispatch

To trigger manually:
1. Open the repository on GitHub
2. Go to **Actions**
3. Select the workflow
4. Click **Run workflow**

## Security notes

- Keep all API keys and auth JSON in environment variables/secrets only.
- Never commit `.env`, raw OAuth codes, token JSON, or service-account keys.
- Use repository/organization secrets for GitHub Actions execution.
