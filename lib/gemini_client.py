import io  # used for _bytes_to_pil
import os
import warnings

import streamlit as st
from dotenv import load_dotenv
from PIL import Image
from google import genai
from google.genai import types

load_dotenv()

_MODEL = "gemini-2.5-flash-image"
_MAX_INPUT_PX = 1024
_MAX_REFERENCES = 2  # logo + up to 2 refs = 3 total inputs
_client: genai.Client | None = None


def _get_api_key() -> str:
    try:
        return st.secrets["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError):
        return os.environ["GEMINI_API_KEY"]


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=_get_api_key())
    return _client


def _bytes_to_pil(image_bytes: bytes) -> Image.Image:
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    w, h = img.size
    if max(w, h) > _MAX_INPUT_PX:
        scale = _MAX_INPUT_PX / max(w, h)
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    return img


def generate_brand_image(
    prompt: str,
    logo_bytes: bytes,
    reference_image_bytes: list[bytes],
) -> bytes:
    """Generate one brand-conditioned image. Returns image bytes."""
    client = _get_client()

    if len(reference_image_bytes) > _MAX_REFERENCES:
        warnings.warn(
            f"generate_brand_image received {len(reference_image_bytes)} reference images; "
            f"capping at {_MAX_REFERENCES} (model supports ≤3 total inputs including logo).",
            stacklevel=2,
        )
        reference_image_bytes = reference_image_bytes[:_MAX_REFERENCES]

    logo_img = _bytes_to_pil(logo_bytes)
    ref_imgs = [_bytes_to_pil(b) for b in reference_image_bytes]

    contents: list = [prompt, logo_img] + ref_imgs

    try:
        response = client.models.generate_content(
            model=_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio="1:1",
                    # image_size omitted: gemini-2.5-flash-image has fixed 1024px resolution
                ),
            ),
        )
    except Exception as e:
        raise RuntimeError(f"Gemini API error: {e}") from e

    response_texts: list[str] = []
    for part in response.parts:
        if part.text is not None:
            response_texts.append(part.text)
        else:
            genai_img = part.as_image()
            if genai_img is not None and genai_img.image_bytes:
                return genai_img.image_bytes

    # No image in response — safety refusal or unexpected shape.
    # Collect any text Gemini returned so the UI can surface it.
    detail = " | ".join(response_texts) if response_texts else "(no text in response)"
    raise RuntimeError(f"No image returned by Gemini. Model said: {detail}")
