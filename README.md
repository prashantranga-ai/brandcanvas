# BrandCanvas

BrandCanvas is a Streamlit web app that helps small businesses generate brand-consistent campaign images using Gemini Flash Image (nano banana).

## How it works

- **Brand setup** — enter your brand name, upload a logo, and add up to 5 reference images that define your visual style
- **Describe your image** — type a prompt describing the campaign image you need
- **Generate** — two on-brand candidates are generated in parallel; download whichever works

## Run locally

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
cp .env.example .env   # then add your GEMINI_API_KEY
streamlit run app.py
```

`GEMINI_API_KEY` is required. Get one at [aistudio.google.com](https://aistudio.google.com). See `.env.example` for the format.

## Deploy

Live at [brandcanvas-prashantr.streamlit.app](https://brandcanvas-prashantr.streamlit.app).

Deployed on Streamlit Community Cloud. Set `GEMINI_API_KEY` in the app's Secrets manager (no `.env` needed).

## Documentation

- [Product spec](./BrandCanvas-PRD.md) — scope, design decisions, system prompt design, what's next
- [Eval set](./BrandCanvas-Evals.md) — reusable test harness with prompts, observations, and findings
