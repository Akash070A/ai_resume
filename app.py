import streamlit as st
import openai
import pandas as pd
from PyPDF2 import PdfReader
import io

# 🔑 API KEY HERE
openai.api_key = "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"

# 🎨 PAGE SETTINGS
st.set_page_config(page_title="AI Hiring Dashboard", layout="wide")

# 🎨 CUSTOM UI
st.markdown("""
<style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# 🎯 HEADER
st.markdown("""
# 🧠 AI Hiring Dashboard
### Intelligent Resume Screening System
""")

# 📌 SIDEBAR INPUT
st.sidebar.header("📥 Input Data")

jd = st.sidebar.text_area("📄 Paste Job Description")

files = st.sidebar.file_uploader(
    "📂 Upload Resume PDFs",
    accept_multiple_files=True
)

# 📄 PDF → TEXT
def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

# 🤖 AI ANALYSIS
def analyze(jd, resume):
    prompt = f"""
    Compare the resume with job description.

    Job Description:
    {jd}

    Resume:
    {resume}

    Output strictly in format:

    Score: number (0-100)
    Strengths:
    - point 1
    - point 2
    - point 3

    Gaps:
    - point 1
    - point 2
    - point 3

    Recommendation: Strong Fit / Moderate Fit / Not Fit
    """

    response = openai.ChatCompletion.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['choices'][0]['message']['content']

# 🧠 RULE-BASED DECISION
def final_decision(score):
    if score >= 80:
        return "Strong Fit"
    elif score >= 60:
        return "Moderate Fit"
    else:
        return "Not Fit"

# 🚀 RUN BUTTON
if st.sidebar.button("🚀 Run Screening"):

    if not jd or not files:
        st.warning("⚠️ Please add Job Description and upload resumes.")
    else:
        results = []

        with st.spinner("Analyzing resumes..."):

            for file in files:
                text = read_pdf(file)
                output = analyze(jd, text)

                # Extract score safely
                try:
                    score_line = output.split("Score:")[1].split("\n")[0]
                    score = int(score_line.strip())
                except:
                    score = 0

                results.append({
                    "Candidate": file.name,
                    "Score": score,
                    "Analysis": output
                })

        df = pd.DataFrame(results)

        # 🔢 SORT + RANK
        df = df.sort_values(by="Score", ascending=False).reset_index(drop=True)
        df["Rank"] = df.index + 1

        # 🤖 FINAL DECISION
        df["Final Decision"] = df["Score"].apply(final_decision)

        # 📊 DASHBOARD
        st.subheader("📊 Hiring Overview")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Candidates", len(df))
        c2.metric("Top Score", df["Score"].max())
        c3.metric("Average Score", int(df["Score"].mean()))
        c4.metric("Strong Fits", len(df[df["Final Decision"] == "Strong Fit"]))

        # 🏆 RANKING TABLE
        st.subheader("🏆 Candidate Ranking")

        st.dataframe(
            df[["Rank", "Candidate", "Score", "Final Decision"]],
            use_container_width=True
        )

        # 📈 CHART
        st.subheader("📈 Score Distribution")
        st.bar_chart(df.set_index("Candidate")["Score"])

        # 📄 DETAILS
        st.subheader("📄 Detailed Analysis")

        for i, row in df.iterrows():
            with st.expander(f"{row['Rank']}. {row['Candidate']} (Score: {row['Score']})"):
                st.write(row["Analysis"])

        # 📥 DOWNLOAD EXCEL
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False)

        st.download_button(
            label="📥 Download Results (Excel)",
            data=buffer,
            file_name="screening_results.xlsx",
            mime="application/vnd.ms-excel"
        )

        # 💡 INSIGHTS
        st.subheader("💡 Hiring Insights")

        strong = len(df[df["Final Decision"] == "Strong Fit"])
        moderate = len(df[df["Final Decision"] == "Moderate Fit"])
        weak = len(df[df["Final Decision"] == "Not Fit"])

        if strong == 0:
            st.warning("No strong candidates found. Consider adjusting requirements.")

        if moderate > strong:
            st.info("Many moderate candidates detected. Training programs can improve hiring quality.")

        if weak > strong:
            st.error("High rejection rate. Improve sourcing or job description clarity.")

        st.success("Tip: Focus on candidates with score above 70 for faster hiring.")

# FOOTER
st.markdown("---")
st.caption("🚀 AI Resume Screening System | Built for Hiring Automation")