"""
Smoke test for the Gemini client wrapper.

Prerequisites:
  - .env file with GEMINI_API_KEY set
  - test_logo.png in the project root

Run:
  python test_gemini.py
"""

import sys
from pathlib import Path

LOGO_PATH = Path(__file__).parent / "test_logo.png"
OUTPUT_PATH = Path(__file__).parent / "test_output.png"
PROMPT = (
    "A product photograph of a coffee cup on a wooden table, soft natural lighting"
)


def main():
    if not LOGO_PATH.exists():
        print(f"ERROR: {LOGO_PATH} not found. Add a test_logo.png to the project root.")
        sys.exit(1)

    logo_bytes = LOGO_PATH.read_bytes()

    print(f"Logo: {LOGO_PATH} ({len(logo_bytes):,} bytes)")
    print(f"Prompt: {PROMPT!r}")
    print("Calling Gemini API...")

    try:
        from lib.gemini_client import generate_brand_image
        result = generate_brand_image(
            prompt=PROMPT,
            logo_bytes=logo_bytes,
            reference_image_bytes=[],
        )
    except RuntimeError as e:
        print(f"\nFAIL: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUNEXPECTED ERROR ({type(e).__name__}): {e}")
        sys.exit(1)

    OUTPUT_PATH.write_bytes(result)
    print(f"\nSUCCESS: {len(result):,} bytes written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
