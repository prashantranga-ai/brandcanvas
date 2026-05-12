import concurrent.futures
import re

import streamlit as st

from lib.gemini_client import generate_brand_image
from lib.prompts import construct_prompt

_CSS = """
<style>
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #18181B !important;
    border: 1px solid #27272A !important;
    border-radius: 10px !important;
}
.bc-context {
    font-size: 0.8rem;
    color: #6B6760;
    margin: 0 0 0.25rem 0;
}
</style>
"""

_FRIENDLY_ERROR = (
    "Couldn't generate that one. The model may be busy, or the request "
    "might conflict with your brand context. Try regenerating, or adjust your prompt."
)


def _brand_slug() -> str:
    name = st.session_state.brand_name or "brand"
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _ref_bytes_for_regen() -> list[bytes]:
    return [
        st.session_state.brand_references[i]
        for i in st.session_state.selected_references
        if i < len(st.session_state.brand_references)
    ][:2]


def _run_generation(
    user_description: str,
    logo_bytes: bytes,
    ref_bytes: list[bytes],
) -> None:
    """Construct prompt, call API twice in parallel, store results in session state."""
    prompt = construct_prompt(user_description, st.session_state.brand_name)
    st.session_state.last_prompt_constructed = prompt

    # Always 2-element; None means that candidate failed.
    results: list[bytes | None] = [None, None]
    error_msgs: list[str | None] = [None, None]

    with st.status(
        "Generating two on-brand candidates... this usually takes 15–25 seconds.",
        expanded=True,
    ) as status:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future_map: dict[concurrent.futures.Future, int] = {
                executor.submit(generate_brand_image, prompt, logo_bytes, ref_bytes): i
                for i in range(2)
            }
            completed = 0
            for future in concurrent.futures.as_completed(future_map):
                idx = future_map[future]
                completed += 1
                try:
                    results[idx] = future.result()
                    if completed == 1:
                        status.update(
                            label="First candidate ready. Finishing the second..."
                        )
                except Exception as exc:
                    error_msgs[idx] = str(exc)

        all_failed = all(r is None for r in results)
        status.update(
            label="Generation failed." if all_failed else "Done!",
            state="error" if all_failed else "complete",
        )

    st.session_state.generated_images = results
    st.session_state.generation_errors = error_msgs


def _render_reference_tray() -> None:
    refs = st.session_state.brand_references

    if not refs:
        st.caption("No references uploaded. Go back to setup to add some.")
        if st.button("← Back to setup", key="tray_back"):
            st.session_state.stage = "setup"
            st.rerun()
        return

    st.caption(
        "Select reference images to guide the generation. "
        "Up to 3 will be sent to the model. The logo is always included."
    )

    # Compute selection count from previous render cycle before rendering checkboxes.
    n_selected = sum(
        1 for i in range(len(refs))
        if st.session_state.get(f"ref_check_{i}", False)
    )

    cols = st.columns(5)
    for i, img_bytes in enumerate(refs):
        is_checked = st.session_state.get(f"ref_check_{i}", False)
        with cols[i]:
            st.image(img_bytes, width=100)
            st.checkbox(
                "Select",
                key=f"ref_check_{i}",
                disabled=not (is_checked or n_selected < 3),
                label_visibility="collapsed",
            )

    # Keep selected_references in sync after checkboxes render.
    st.session_state.selected_references = [
        i for i in range(len(refs))
        if st.session_state.get(f"ref_check_{i}", False)
    ]


def _render_results(prompt_text: str) -> None:
    st.markdown("<br>", unsafe_allow_html=True)

    images: list[bytes | None] = st.session_state.generated_images
    errors: list[str | None] = st.session_state.get("generation_errors", [None, None])
    slug = _brand_slug()
    regen_triggered = False

    c1, c2 = st.columns(2, gap="medium")
    for col, i in zip((c1, c2), range(2)):
        with col:
            img = images[i] if i < len(images) else None
            if img is not None:
                st.image(img, use_container_width=True)
                st.download_button(
                    label="Download",
                    data=img,
                    file_name=f"brandcanvas-{slug}-{i + 1}.png",
                    mime="image/png",
                    key=f"dl_{i}",
                )
                st.caption(f"Candidate {i + 1}")
            else:
                st.error(_FRIENDLY_ERROR)
                if st.button("Try again", key=f"try_again_{i}"):
                    regen_triggered = True

    if regen_triggered:
        _run_generation(prompt_text, st.session_state.brand_logo, _ref_bytes_for_regen())
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    _, regen_col, _ = st.columns([2, 1, 2])
    with regen_col:
        if st.button(
            "Regenerate",
            type="primary",
            use_container_width=True,
            key="regen_btn",
        ):
            _run_generation(prompt_text, st.session_state.brand_logo, _ref_bytes_for_regen())
            st.rerun()

    if st.session_state.last_prompt_constructed:
        with st.expander("View constructed prompt", expanded=False):
            st.caption(
                "This is the full prompt sent to the model. "
                "The reference images and logo are sent alongside."
            )
            st.code(st.session_state.last_prompt_constructed, language=None)


def render() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 4, 1])
    with col:
        if st.button("← Back", key="gen_back"):
            st.session_state.stage = "setup"
            st.rerun()

        st.markdown(
            "<h1 style='margin-top:0.5rem; margin-bottom:0.2rem;'>Generate a creative</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='color:#8A8680; font-size:1rem; margin-top:0;'>"
            "Describe the image. We'll generate two on-brand candidates.</p>",
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        n_refs = len(st.session_state.brand_references)
        ref_label = f"{n_refs} reference image{'s' if n_refs != 1 else ''}"
        st.markdown(
            f"<p class='bc-context'>Brand: <strong>{st.session_state.brand_name}</strong>"
            f" &middot; {ref_label}</p>",
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            prompt_text: str = st.text_area(
                "Image description",
                placeholder="A product photograph of [your product] on a wooden table, soft natural lighting",
                height=110,
                key="generate_prompt",
            )

            with st.expander("Add references", expanded=False):
                _render_reference_tray()

            st.markdown("<br>", unsafe_allow_html=True)

            _, btn_col = st.columns([3, 1])
            with btn_col:
                generate_clicked = st.button(
                    "Generate",
                    type="primary",
                    disabled=not bool(prompt_text.strip()),
                    use_container_width=True,
                    key="gen_btn",
                )

        if generate_clicked:
            ref_bytes = [
                st.session_state.brand_references[i]
                for i in st.session_state.selected_references
                if i < len(st.session_state.brand_references)
            ][:2]
            _run_generation(prompt_text, st.session_state.brand_logo, ref_bytes)
            st.rerun()

        if st.session_state.generated_images:
            _render_results(prompt_text)
