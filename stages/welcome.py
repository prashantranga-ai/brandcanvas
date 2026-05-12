import streamlit as st

_CARDS = [
    {
        "n": "1",
        "title": "Set up your brand",
        "desc": "Add your name, logo, and reference images of your visual style.",
    },
    {
        "n": "2",
        "title": "Describe what you need",
        "desc": "Tell us the image you want. Be specific about subject, mood, and setting.",
    },
    {
        "n": "3",
        "title": "Get on-brand visuals",
        "desc": "We'll generate two candidates that match your brand.",
    },
]

_CSS = """
<style>
.bc-welcome .block-container {
    padding-top: 4rem !important;
    padding-bottom: 4rem !important;
}
.bc-card {
    background-color: #18181B;
    padding: 20px 22px;
    border-radius: 10px;
    height: 100%;
    box-sizing: border-box;
}
.bc-card-num {
    width: 26px;
    height: 26px;
    border: 1px solid #3A3830;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.65rem;
    color: #6B6760;
    font-weight: 500;
    margin: 0 auto 14px auto;
}
.bc-card-title {
    font-size: 0.925rem;
    font-weight: 600;
    color: #E8E6E0;
    margin-bottom: 7px;
}
.bc-card-desc {
    font-size: 0.85rem;
    color: #8A8680;
    line-height: 1.6;
    margin: 0;
}
</style>
"""


def _card_html(n: str, title: str, desc: str) -> str:
    return (
        f'<div class="bc-card">'
        f'<div class="bc-card-num">{n}</div>'
        f'<div class="bc-card-title">{title}</div>'
        f'<p class="bc-card-desc">{desc}</p>'
        f'</div>'
    )


def render():
    st.markdown(_CSS, unsafe_allow_html=True)

    # Header
    _, hdr, _ = st.columns([1, 2, 1])
    with hdr:
        st.markdown(
            "<div style='text-align:center; font-size:1.5rem; margin-bottom:0.1rem;'>🎨</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h1 style='text-align:center; margin-top:0.2rem; margin-bottom:0.3rem;'>BrandCanvas</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='text-align:center; color:#8A8680; font-size:1rem; margin-top:0;'>"
            "Create on-brand visuals, no design skills required.</p>",
            unsafe_allow_html=True,
        )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Orientation cards — constrained width with outer gutters
    _, cards_col, _ = st.columns([1, 4, 1])
    with cards_col:
        c1, c2, c3 = st.columns(3, gap="medium")
        for col, card in zip((c1, c2, c3), _CARDS):
            with col:
                st.markdown(_card_html(card["n"], card["title"], card["desc"]), unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # CTA
    _, btn_col, _ = st.columns([2, 1, 2])
    with btn_col:
        if st.button("Get started", type="primary", use_container_width=True):
            st.session_state.stage = "setup"
            st.rerun()
