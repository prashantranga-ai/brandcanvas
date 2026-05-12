import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from lib.state import init_state
from stages import welcome, setup, generate

st.set_page_config(
    page_title="BrandCanvas",
    page_icon="🎨",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&display=swap');
    h1, h2, h3 { font-family: 'Playfair Display', serif !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

init_state()

stage = st.session_state.stage

if stage == "welcome":
    welcome.render()
elif stage == "setup":
    setup.render()
elif stage == "generate":
    generate.render()
