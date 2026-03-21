"""AI Resume Screener — entry point. Run with: streamlit run app.py"""

import streamlit as st

from ui.styles import inject_styles
from ui.landing import render_landing_page
from ui.dashboard import render_dashboard


def setup_page_config() -> None:
    st.set_page_config(
        page_title="AI Resume Screener",
        layout="wide",
        menu_items={
            "About": (
                "### AI Resume Screening System\n"
                "An intelligent matching tool built to accelerate hiring by automatically "
                "evaluating PDF resumes against job descriptions."
            )
        }
    )


def main() -> None:
    setup_page_config()
    inject_styles()

    if "screening_results" not in st.session_state:
        render_landing_page()
    else:
        render_dashboard()


if __name__ == "__main__":
    main()