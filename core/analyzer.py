"""Handles LLM communication via the Groq API and parses the structured response."""

import re

import openai

from config import GROQ_API_KEY, GROQ_API_BASE, MODEL_NAME

openai.api_key = GROQ_API_KEY
openai.api_base = GROQ_API_BASE


def analyze_resume(job_description: str, resume_text: str, custom_instructions: str) -> str:
    """Sends the resume and job description to the LLM and returns the raw response."""
    system_instruction = custom_instructions if custom_instructions else "None provided"

    prompt = f"""
    Compare the resume with job description.

    Job Description:
    {job_description}

    Additional Evaluation Criteria:
    {system_instruction}

    Resume:
    {resume_text}

    Output strictly in the following format:

    Score: [number between 0-100]
    Strengths:
    - [point 1]
    - [point 2]
    - [point 3]

    Gaps:
    - [point 1]
    - [point 2]
    - [point 3]

    Recommendation: Strong Fit / Moderate Fit / Not Fit
    """

    try:
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error during analysis: {str(e)}"


def parse_result(output: str, file_name: str) -> dict:
    """Parses the LLM's raw text output into a structured result dictionary."""
    try:
        match = re.search(r"Score.*?(\d+)", output, re.IGNORECASE)
        score = int(match.group(1)) if match else 0
        score = max(0, min(100, score))
    except Exception:
        score = 0

    strengths_text = "N/A"
    gaps_text = "N/A"
    try:
        s_match = re.search(r"Strengths:(.*?)(?=Gaps:)", output, re.IGNORECASE | re.DOTALL)
        if s_match:
            strengths_text = s_match.group(1).strip()

        g_match = re.search(r"Gaps:(.*?)(?=Recommendation:|$)", output, re.IGNORECASE | re.DOTALL)
        if g_match:
            gaps_text = g_match.group(1).strip()
    except Exception:
        pass

    return {
        "Candidate": file_name,
        "Score": score,
        "Strengths": strengths_text,
        "Gaps": gaps_text,
        "Analysis": output,
        "RawText": "",
    }
