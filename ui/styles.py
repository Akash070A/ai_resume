"""Injects global CSS styles and Google Font imports into the Streamlit page."""

import streamlit as st


def inject_styles() -> None:
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap');

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            font-family: 'Inter', sans-serif;
        }

        span[data-baseweb="tag"] {
            background-color: #ff6b6b !important;
            border-radius: 8px !important;
            padding: 5px 12px !important;
        }
        span[data-baseweb="tag"] * {
            color: #ffffff !important;
            font-weight: 600 !important;
        }
        div.stSlider div[role="slider"] {
            background-color: #ff6b6b !important;
            border-color: #ff4757 !important;
            box-shadow: 0 4px 10px rgba(255, 107, 107, 0.4) !important;
        }

        h1, h2, h3, h4 {
            font-family: 'Inter', sans-serif;
            font-weight: 800;
            letter-spacing: -0.5px;
        }

        hr {
            margin: 2.5em 0;
            border-top: 1px solid #cbd5e1;
        }

        div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #ff6b6b 0%, #ff4757 100%) !important;
            color: white !important;
            font-weight: 800 !important;
            border-radius: 12px !important;
            padding: 0.75rem 2rem !important;
            border: none !important;
            box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3) !important;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        div.stButton > button[kind="primary"]:hover {
            transform: translateY(-4px) scale(1.02) !important;
            box-shadow: 0 15px 35px rgba(255, 107, 107, 0.5) !important;
            filter: brightness(1.1) !important;
        }

        div.stButton > button[kind="secondary"] {
            background-color: #ffffff;
            color: #475569;
            font-weight: 600;
            border-radius: 10px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            transition: all 0.2s ease;
        }
        div.stButton > button[kind="secondary"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(0,0,0,0.08);
            border-color: #cbd5e1;
            color: #0f172a;
        }

        .streamlit-expanderHeader {
            font-weight: 600 !important;
            color: #1e293b !important;
        }
    </style>
    """, unsafe_allow_html=True)
