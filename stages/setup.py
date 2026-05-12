import streamlit as st

_CSS = """
<style>
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #18181B !important;
    border: 1px solid #27272A !important;
    border-radius: 10px !important;
}
.bc-tip {
    font-size: 0.8rem;
    color: #6B6760;
    margin: 4px 0 0 0;
}
</style>
"""


def render():
    st.markdown(_CSS, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 4, 1])
    with col:
        if st.button("← Back", key="setup_back"):
            st.session_state.stage = "welcome"
            st.rerun()

        st.markdown(
            "<h1 style='margin-top:0.5rem; margin-bottom:0.2rem;'>Set up your brand</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='color:#8A8680; font-size:1rem; margin-top:0;'>"
            "We'll use this every time you generate.</p>",
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        with st.container(border=True):
            # Brand name
            st.text_input(
                "Brand name",
                placeholder="e.g., Apparel Co.",
                key="brand_name",
            )

            st.markdown("<br>", unsafe_allow_html=True)

            # Logo
            logo_file = st.file_uploader(
                "Logo",
                type=["png", "jpg", "jpeg"],
                accept_multiple_files=False,
                key="logo_uploader",
            )
            if logo_file is not None:
                st.session_state.brand_logo = logo_file.getvalue()
            if st.session_state.brand_logo:
                st.image(st.session_state.brand_logo, width=100)

            st.markdown("<br>", unsafe_allow_html=True)

            # Reference images
            ref_files = st.file_uploader(
                "Reference images",
                type=["png", "jpg", "jpeg"],
                accept_multiple_files=True,
                key="ref_uploader",
            )
            if ref_files:
                ref_bytes = [f.getvalue() for f in ref_files]
                if len(ref_bytes) > 5:
                    ref_bytes = ref_bytes[:5]
                    st.info("Only the first 5 references will be used.")
                st.session_state.brand_references = ref_bytes
            if st.session_state.brand_references:
                thumb_cols = st.columns(5)
                for i, img_bytes in enumerate(st.session_state.brand_references):
                    with thumb_cols[i]:
                        st.image(img_bytes, width=100)

            st.markdown(
                "<p class='bc-tip'>Tip: include 3–5 images showing your brand's style — "
                "product shots, lifestyle photos, packaging.</p>",
                unsafe_allow_html=True,
            )

            st.markdown("<br>", unsafe_allow_html=True)

            # CTA — right-aligned
            ready = (
                bool(st.session_state.brand_name.strip())
                and st.session_state.brand_logo is not None
            )
            _, btn_col = st.columns([3, 1])
            with btn_col:
                if st.button(
                    "Looks good",
                    type="primary",
                    disabled=not ready,
                    use_container_width=True,
                    key="setup_cta",
                ):
                    st.session_state.stage = "generate"
                    st.rerun()
