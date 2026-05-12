import streamlit as st


def init_state():
    defaults = {
        "stage": "welcome",
        "brand_name": "",
        "brand_logo": None,
        "brand_references": [],
        "selected_references": [],
        "generated_images": [],
        "last_prompt_constructed": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
