"""Shared utility functions used across UI modules."""

import streamlit as st


def get_final_decision(score: int) -> str:
    """Maps a numeric score to a hiring decision label."""
    if score >= 80:
        return "Strong Fit"
    elif score >= 60:
        return "Moderate Fit"
    return "Not Fit"


def reset_session() -> None:
    """Clears all Streamlit session state keys."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
