"""Renders the results dashboard: sidebar filters, metrics, leaderboard, analysis tabs, and export."""

from typing import Any

import io
import pandas as pd
import streamlit as st

from utils.helpers import get_final_decision, reset_session


def _make_hover(text: Any) -> str:
    raw_str = str(text)
    full_text = raw_str.replace('"', "&quot;").replace("\n", "<br>")
    short_text = raw_str.replace("\n", " ")
    if len(short_text) > 40:
        short_text = short_text[:40].strip() + "..."
    return (
        f'<span class="tbl-popup-trigger" style="cursor: pointer; color: #3b82f6; '
        f'border-bottom: 1px dashed #94a3b8; font-weight: 500; position: relative;">'
        f'{short_text}'
        f'<span class="tbl-popup">{full_text}</span>'
        f'</span>'
    )


def _style_decision(decision: str) -> str:
    if "Strong" in decision:
        return (
            f'<span style="background-color: #dcfce7; color: #15803d; padding: 5px 12px; '
            f'border-radius: 20px; font-weight: 700; font-size: 0.85em; '
            f'box-shadow: 0 2px 5px rgba(22,101,52,0.1);">Strong Fit</span>'
        )
    elif "Moderate" in decision:
        return (
            f'<span style="background-color: #fef9c3; color: #854d0e; padding: 5px 12px; '
            f'border-radius: 20px; font-weight: 700; font-size: 0.85em; '
            f'box-shadow: 0 2px 5px rgba(133,77,14,0.1);">Moderate Fit</span>'
        )
    return (
        f'<span style="background-color: #fee2e2; color: #b91c1c; padding: 5px 12px; '
        f'border-radius: 20px; font-weight: 700; font-size: 0.85em; '
        f'box-shadow: 0 2px 5px rgba(185,28,28,0.1);">Not Fit</span>'
    )


def _render_metrics(filtered_df: pd.DataFrame, strong_fits: int) -> None:
    total_names = filtered_df["Candidate"].str.replace(".pdf", "", case=False).tolist()
    highest_score = filtered_df["Score"].max()
    top_candidates = (
        filtered_df[filtered_df["Score"] == highest_score]["Candidate"]
        .str.replace(".pdf", "", case=False)
        .tolist()
    )
    strong_candidates = (
        filtered_df[filtered_df["Final Decision"] == "Strong Fit"]["Candidate"]
        .str.replace(".pdf", "", case=False)
        .tolist()
    )

    total_str = f"Candidates: {', '.join(total_names) if total_names else 'None'}"
    top_str = f"Top performer(s): {', '.join(top_candidates) if top_candidates else 'None'}"
    avg_str = "Average AI Score across all currently filtered matches."
    strong_str = f"Strong Fits: {', '.join(strong_candidates) if strong_candidates else 'None'}"

    css_card = (
        "flex: 1; background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%); "
        "padding: 25px 20px; border-radius: 20px; box-shadow: 0 10px 25px rgba(15,23,42,0.06); "
        "text-align: center; border: 1px solid #e2e8f0; border-top: 6px solid #ff6b6b; "
        "cursor: help; transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease;"
    )
    css_title = (
        "margin: 0; font-size: 14px; font-weight: 700; color: #64748b; "
        "font-family: 'Inter', sans-serif; text-transform: uppercase; letter-spacing: 1px;"
    )
    css_val = (
        "margin: 12px 0 0 0; font-size: 48px; font-weight: 900; color: #0f172a; "
        "font-family: 'Inter', sans-serif; line-height: 1;"
    )

    hover_style = """
    <style>
        .val-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 15px 35px rgba(255, 107, 107, 0.15) !important;
            border-color: #ffb3b3 !important;
        }
    </style>
    """

    metrics_html = f"""
    {hover_style}
    <div style="display: flex; gap: 25px; width: 100%;">
        <div class="val-card" title="{total_str}" style="{css_card}">
            <p style="{css_title}">Total Matches</p>
            <p style="{css_val}">{len(filtered_df)}</p>
        </div>
        <div class="val-card" title="{top_str}" style="{css_card}">
            <p style="{css_title}">Highest Score</p>
            <p style="{css_val}">{highest_score}</p>
        </div>
        <div class="val-card" title="{avg_str}" style="{css_card}">
            <p style="{css_title}">Average Score</p>
            <p style="{css_val}">{int(filtered_df["Score"].mean())}</p>
        </div>
        <div class="val-card" title="{strong_str}" style="{css_card}">
            <p style="{css_title}">Strong Candidates</p>
            <p style="{css_val}">{strong_fits}</p>
        </div>
    </div>
    """
    st.markdown(metrics_html, unsafe_allow_html=True)


def _render_leaderboard(filtered_df: pd.DataFrame) -> None:
    html_df = filtered_df[["Rank", "Candidate", "Score", "Strengths", "Gaps", "Final Decision"]].copy()

    html_df["Strengths"] = html_df["Strengths"].apply(_make_hover)
    html_df["Gaps"] = html_df["Gaps"].apply(_make_hover)
    html_df["Final Decision"] = html_df["Final Decision"].apply(_style_decision)
    html_df["Rank"] = html_df["Rank"].apply(lambda x: f'<span style="font-weight: 800; opacity: 0.6;">#{x}</span>')
    html_df["Score"] = html_df["Score"].apply(lambda x: f'<span style="font-weight: 900; font-size: 1.15em;">{x}</span>')
    html_df["Candidate"] = html_df["Candidate"].apply(
        lambda x: f'<span style="font-weight: 700;">{str(x).replace(".pdf", "")}</span>'
    )

    table_style = """
    <style>
    .custom-tbl { width: 100%; border-collapse: collapse; font-family: 'Inter', sans-serif; background-color: transparent; text-align: center; table-layout: fixed; }
    .custom-tbl th { background-color: rgba(128,128,128,0.05); color: inherit; opacity: 0.8; font-weight: 800; padding: 10px 12px; text-transform: uppercase; font-size: 11px; letter-spacing: 1px; border-bottom: 2px solid #94a3b8; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; text-align: center; }
    .custom-tbl td { padding: 8px 12px; border-bottom: 1px solid #cbd5e1; color: inherit; font-size: 14px; vertical-align: middle; white-space: nowrap; overflow: visible; text-align: center; position: relative; }
    .custom-tbl tr { transition: all 0.2s ease; }
    .custom-tbl tr:hover { background-color: rgba(128,128,128,0.05); box-shadow: inset 4px 0 0 0 #3b82f6; }
    .custom-tbl th:nth-child(1), .custom-tbl td:nth-child(1) { width: 5%; }
    .custom-tbl th:nth-child(2), .custom-tbl td:nth-child(2) { width: 16%; }
    .custom-tbl th:nth-child(3), .custom-tbl td:nth-child(3) { width: 8%; }
    .custom-tbl th:nth-child(4), .custom-tbl td:nth-child(4) { width: 28%; }
    .custom-tbl th:nth-child(5), .custom-tbl td:nth-child(5) { width: 28%; }
    .custom-tbl th:nth-child(6), .custom-tbl td:nth-child(6) { width: 15%; }

    /* Popup bubble */
    .tbl-popup-trigger { position: relative; display: inline-block; }
    .tbl-popup {
        visibility: hidden;
        opacity: 0;
        min-width: 280px;
        max-width: 380px;
        background: #1e293b;
        color: #e2e8f0;
        font-size: 13px;
        font-weight: 400;
        line-height: 1.7;
        text-align: left;
        border-radius: 12px;
        padding: 14px 16px;
        position: absolute;
        z-index: 9999;
        bottom: calc(100% + 10px);
        left: 50%;
        transform: translateX(-50%);
        box-shadow: 0 12px 35px rgba(0,0,0,0.3);
        transition: opacity 0.2s ease, visibility 0.2s ease;
        pointer-events: none;
        white-space: normal;
        word-wrap: break-word;
    }
    .tbl-popup::after {
        content: '';
        position: absolute;
        top: 100%;
        left: 50%;
        transform: translateX(-50%);
        border: 7px solid transparent;
        border-top-color: #1e293b;
    }
    .tbl-popup-trigger:hover .tbl-popup,
    .tbl-popup-trigger.pinned .tbl-popup {
        visibility: visible;
        opacity: 1;
        pointer-events: auto;
    }
    </style>

    <script>
    (function() {
        function initPopups() {
            document.querySelectorAll('.tbl-popup-trigger').forEach(function(trigger) {
                if (trigger.dataset.popupInit) return;
                trigger.dataset.popupInit = '1';
                trigger.addEventListener('click', function(e) {
                    e.stopPropagation();
                    var isPinned = trigger.classList.contains('pinned');
                    document.querySelectorAll('.tbl-popup-trigger.pinned').forEach(function(el) {
                        el.classList.remove('pinned');
                    });
                    if (!isPinned) trigger.classList.add('pinned');
                });
            });
            document.addEventListener('click', function() {
                document.querySelectorAll('.tbl-popup-trigger.pinned').forEach(function(el) {
                    el.classList.remove('pinned');
                });
            });
        }
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initPopups);
        } else {
            initPopups();
            setTimeout(initPopups, 500);
        }
    })();
    </script>
    """

    st.markdown(table_style, unsafe_allow_html=True)
    st.markdown('<div style="border-radius: 12px; overflow: hidden; border: 1px solid rgba(128,128,128,0.2); box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-top: 1rem;">', unsafe_allow_html=True)
    st.markdown(html_df.to_html(escape=False, index=False, classes="custom-tbl"), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def _render_overview_tab(filtered_df: pd.DataFrame) -> None:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin: 0; color: #0f172a;'>Candidate Leaderboard</h3>", unsafe_allow_html=True)
    _render_leaderboard(filtered_df)

    st.markdown("<br><br>", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        st.markdown("<h3 style='margin: 0; color: #0f172a;'>Score Distribution</h3>", unsafe_allow_html=True)
        st.bar_chart(filtered_df.set_index("Candidate")["Score"], use_container_width=True)

    with c2:
        st.markdown("<h3 style='margin: 0; color: #0f172a;'>Export Database</h3>", unsafe_allow_html=True)
        st.info("Download the full parsed dataframe as an Excel document.")
        export_buffer = io.BytesIO()
        filtered_df.to_excel(export_buffer, index=False)

        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="Download Full Report (Excel)",
            data=export_buffer,
            file_name="screening_results.xlsx",
            mime="application/vnd.ms-excel",
            use_container_width=True,
            type="primary"
        )


def _parse_bullet_points(text: str) -> list[str]:
    """Splits a strengths/gaps block into individual bullet point strings."""
    lines = text.strip().splitlines()
    points = [ln.lstrip("-• ").strip() for ln in lines if ln.strip().lstrip("-• ").strip()]
    return points


def _bullet_list_html(points: list[str], accent: str) -> str:
    """Renders a list of points as styled HTML bullet rows."""
    rows = "".join(
        f"""<div style="display:flex; align-items:flex-start; gap:10px; margin-bottom:10px;">
               <span style="min-width:8px; height:8px; border-radius:50%; background:{accent};
                            margin-top:6px; flex-shrink:0; display:inline-block;"></span>
               <span style="font-size:14px; color:#334155; line-height:1.6;">{p}</span>
           </div>"""
        for p in points
    )
    return rows or f'<p style="color:#94a3b8; font-size:13px;">No data available.</p>'


def _decision_badge_html(decision: str) -> str:
    cfg = {
        "Strong Fit":   ("#dcfce7", "#15803d", "#166534"),
        "Moderate Fit": ("#fef9c3", "#854d0e", "#713f12"),
        "Not Fit":      ("#fee2e2", "#b91c1c", "#991b1b"),
    }
    bg, color, border = cfg.get(decision, ("#f1f5f9", "#475569", "#64748b"))
    return (
        f'<span style="display:inline-block; background:{bg}; color:{color}; '
        f'border:1.5px solid {border}22; padding:6px 18px; border-radius:30px; '
        f'font-weight:700; font-size:0.9em; letter-spacing:0.3px;">{decision}</span>'
    )


def _score_ring_html(score: int) -> str:
    if score >= 80:
        ring_color = "#16a34a"
    elif score >= 60:
        ring_color = "#d97706"
    else:
        ring_color = "#dc2626"
    return f"""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;
                width:110px; height:110px; border-radius:50%;
                border: 6px solid {ring_color}; margin: 0 auto 12px auto;">
        <span style="font-size:28px; font-weight:900; color:#0f172a; line-height:1;">{score}</span>
        <span style="font-size:11px; font-weight:600; color:#64748b; letter-spacing:1px;">/ 100</span>
    </div>"""


def _render_details_tab(filtered_df: pd.DataFrame) -> None:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin: 0; color: #0f172a;'>AI Reasoning Breakdown</h3>", unsafe_allow_html=True)
    st.caption("Structured breakdown of the AI evaluation for each candidate.")
    st.markdown("<br>", unsafe_allow_html=True)

    for _, row in filtered_df.iterrows():
        candidate_name = str(row["Candidate"]).replace(".pdf", "")
        with st.expander(
            f"Rank {row['Rank']}: {candidate_name} — Score: {row['Score']}/100",
            expanded=(row["Rank"] == 1)
        ):
            eval_tab, raw_tab = st.tabs(["Structured Evaluation", "Raw PDF Text"])

            with eval_tab:
                st.markdown("<br>", unsafe_allow_html=True)

                strengths = _parse_bullet_points(str(row["Strengths"]))
                gaps = _parse_bullet_points(str(row["Gaps"]))
                decision = str(row["Final Decision"])

                # Top row: score ring + decision
                left, right = st.columns([1, 3], gap="large")

                with left:
                    st.markdown(
                        f"""
                        <div style="background: linear-gradient(145deg,#ffffff,#f8fafc);
                                    border:1px solid #e2e8f0; border-radius:16px;
                                    padding:24px 16px; text-align:center;
                                    box-shadow:0 4px 12px rgba(15,23,42,0.06);">
                            <p style="margin:0 0 8px 0; font-size:11px; font-weight:700;
                                      color:#64748b; text-transform:uppercase; letter-spacing:1px;">AI Score</p>
                            {_score_ring_html(row['Score'])}
                            <p style="margin:8px 0 0 0; font-size:11px; font-weight:700;
                                      color:#64748b; text-transform:uppercase; letter-spacing:1px;">Decision</p>
                            <div style="margin-top:8px;">{_decision_badge_html(decision)}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with right:
                    col_s, col_g = st.columns(2, gap="large")

                    with col_s:
                        st.markdown(
                            f"""
                            <div style="background:#f0fdf4; border:1px solid #bbf7d0;
                                        border-radius:14px; padding:20px 18px;
                                        min-height:200px;">
                                <p style="margin:0 0 14px 0; font-size:12px; font-weight:800;
                                          color:#15803d; text-transform:uppercase; letter-spacing:1px;">
                                    Strengths
                                </p>
                                {_bullet_list_html(strengths, '#16a34a')}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with col_g:
                        st.markdown(
                            f"""
                            <div style="background:#fff7ed; border:1px solid #fed7aa;
                                        border-radius:14px; padding:20px 18px;
                                        min-height:200px;">
                                <p style="margin:0 0 14px 0; font-size:12px; font-weight:800;
                                          color:#c2410c; text-transform:uppercase; letter-spacing:1px;">
                                    Gaps
                                </p>
                                {_bullet_list_html(gaps, '#ea580c')}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                st.markdown("<br>", unsafe_allow_html=True)

            with raw_tab:
                st.text_area(
                    "Read-only PDF Extraction",
                    row["RawText"],
                    height=300,
                    disabled=True,
                    key=f"text_{row['Candidate']}"
                )


def render_dashboard() -> None:
    st.markdown(
        "<h2 style='margin-top: -10px; color: #0f172a; letter-spacing: -1px;'>Screening Dashboard</h2>",
        unsafe_allow_html=True
    )

    if st.sidebar.button("New Assessment", use_container_width=True, help="Clear results and start a new resume screening"):
        reset_session()
        st.rerun()

    st.sidebar.markdown("<hr style='margin: 1.5em 0;'>", unsafe_allow_html=True)

    raw_df = pd.DataFrame(st.session_state["screening_results"])
    raw_df["Final Decision"] = raw_df["Score"].apply(get_final_decision)

    st.sidebar.markdown("""
        <div style='text-align: center; margin-bottom: 2.5rem;'>
            <h2 style='color: #0f172a; margin-bottom: 0.2rem; font-size: 28px; letter-spacing: -1px;'>Filters</h2>
            <p style='color: #64748b; font-weight: 500;'>Refine your search</p>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("**Minimum Score Requirement:**")
    min_score = st.sidebar.slider(
        "Minimum AI Score", min_value=0, max_value=100, value=40, step=5, label_visibility="collapsed"
    )

    st.sidebar.markdown("<br>**Final Decision Approval:**", unsafe_allow_html=True)
    selected_decisions = st.sidebar.multiselect(
        "Filter by Decision",
        options=["Strong Fit", "Moderate Fit", "Not Fit"],
        default=["Strong Fit", "Moderate Fit", "Not Fit"],
        label_visibility="collapsed"
    )

    filtered_df = raw_df[
        (raw_df["Score"] >= min_score) &
        (raw_df["Final Decision"].isin(selected_decisions))
    ]

    if filtered_df.empty:
        st.warning("No candidates matched your filter criteria. Adjust the sidebar settings.")
        return

    filtered_df = filtered_df.sort_values(by="Score", ascending=False).reset_index(drop=True)
    filtered_df["Rank"] = filtered_df.index + 1

    strong_fits = len(filtered_df[filtered_df["Final Decision"] == "Strong Fit"])

    st.markdown("<br>", unsafe_allow_html=True)
    _render_metrics(filtered_df, strong_fits)
    st.markdown("---")

    tab_overview, tab_details = st.tabs(["Ranked Leaderboard", "Deep Dive Analysis"])

    with tab_overview:
        _render_overview_tab(filtered_df)

    with tab_details:
        _render_details_tab(filtered_df)

    st.markdown("---")

    if strong_fits == 0:
        st.error("No strong candidates found. Consider reviewing the strictness of your job requirements.")
    else:
        st.success(f"You have {strong_fits} solid match(es). Focus your interviews on these top candidates.")
