# BrandCanvas

BrandCanvas is a Streamlit web app that helps small businesses generate brand-consistent campaign images using Gemini Flash Image (nano banana 2). Built as a PM take-home for Ideogram.

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

<!-- TODO: add Streamlit Community Cloud URL after deploy -->

Deployed on Streamlit Community Cloud. Set `GEMINI_API_KEY` in the app's Secrets manager (no `.env` needed).
