"""Renders the landing page: hero banner, input forms, and screening pipeline trigger."""

import streamlit as st

from core.pdf_parser import read_pdf
from core.analyzer import analyze_resume, parse_result


def render_landing_page() -> None:
    st.markdown("""
        <div style='text-align: center; margin-bottom: 1.5rem; padding: 2.5rem 1.5rem; background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border-radius: 24px; box-shadow: 0 20px 40px rgba(15,23,42,0.15); border-bottom: 5px solid #ff6b6b; position: relative; overflow: hidden;'>
            <div style="position: absolute; top: -50%; left: -20%; width: 50%; height: 200%; background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.03) 50%, rgba(255,255,255,0) 100%); transform: rotate(25deg);"></div>
            <h1 style='color: #ffffff; font-size: 3.2rem; margin-bottom: 0.5rem; letter-spacing: -1px; line-height: 1.1;'>AI Talent Matcher</h1>
            <p style='color: #94a3b8; font-size: 1.15rem; font-weight: 400; max-width: 600px; margin: 0 auto;'>The lightning-fast AI engine that evaluates candidate resumes against your job descriptions.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="background-color: #ffffff; padding: 0.5rem 2rem; text-align: center; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); max-width: 1200px; margin: 0 auto 1.5rem auto;">
            <h3 style="margin-top: 0.2rem; margin-bottom: 0px; color: #3b82f6;">Setup Your Assessment</h3>
            <p style="margin-bottom: 0.5rem; font-size: 0.95rem;">Upload the requirements and candidate pool to begin the AI screening.</p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1], gap="large")

    with col1:
        st.markdown("**1. Official Job Requirements**")
        job_description = st.text_area(
            "Job Description",
            height=125,
            label_visibility="collapsed",
            placeholder="e.g. We are looking for a Senior Software Engineer with 5+ years of experience in Python, AWS..."
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**2. Custom Instructions (Optional)**")
        custom_instructions = st.text_area(
            "Custom Instructions",
            height=125,
            label_visibility="collapsed",
            placeholder="e.g. Ignore lack of college degree, highly value startup experience."
        )

    with col2:
        st.markdown("**3. Upload Candidates**")
        st.info("The AI engine will parse and evaluate all uploaded PDFs simultaneously.")
        uploaded_files = st.file_uploader(
            "Upload Resumes",
            accept_multiple_files=True,
            type=["pdf"],
            label_visibility="collapsed"
        )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col_bottom_left, center_col, _ = st.columns([1, 1, 1])

    with col_bottom_left:
        with st.popover("Read: Best Practices"):
            st.markdown("### Best Practices for AI Hiring")
            st.write("This application automatically screens and ranks candidate resumes against your Job Description.")
            st.markdown("**How to get the most accurate results:**")
            st.markdown("- **Detailed Requirements:** The more detailed your Job Description, the more precise the Match Score.")
            st.markdown("- **Custom Instructions:** Tell the AI what trade-offs you allow (e.g. 'Prioritize candidates with startup experience').")
            st.markdown("- **PDFs Only:** Ensure candidates submit standard, text-based PDF resumes.")
            st.info("The AI provides a Score out of 100, identifies Gaps and Strengths, and auto-recommends candidates.")

    with center_col:
        analyze_clicked = st.button("Run Intelligent Screening", type="primary", use_container_width=True)

    if analyze_clicked:
        if not job_description or not uploaded_files:
            st.error("Please provide both a Job Description and at least one Candidate Resume.")
        else:
            results = []

            st.markdown("---")
            st.markdown("<h3 style='text-align: center; color: #ff6b6b;'>Processing Candidates</h3>", unsafe_allow_html=True)
            progress_bar = st.progress(0)
            status_text = st.empty()

            for index, file in enumerate(uploaded_files):
                status_text.markdown(
                    f"<p style='text-align: center; color: #64748b; font-weight: 600;'>"
                    f"Reading and Evaluating: <strong style='color: #0f172a;'>{file.name}</strong> "
                    f"({index + 1}/{len(uploaded_files)})</p>",
                    unsafe_allow_html=True
                )

                text = read_pdf(file)
                raw_output = analyze_resume(job_description, text, custom_instructions)

                result = parse_result(raw_output, file.name)
                result["RawText"] = text
                results.append(result)

                progress_bar.progress((index + 1) / len(uploaded_files))

            st.session_state["screening_results"] = results
            st.rerun()
