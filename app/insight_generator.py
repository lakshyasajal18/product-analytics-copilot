import streamlit as st

from google import genai
from google.genai.errors import ClientError


client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

def generate_insight(question, dataframe):
    """
    Generate a structured product analytics insight
    from the query result.
    """

    prompt = f"""
You are a senior Product Data Analyst.

A product manager asked:

{question}

The SQL query returned:

{dataframe.to_string(index=False)}

Return exactly this format:

SUMMARY:
One concise sentence summarizing the result.

INSIGHT:
One evidence-based business insight.

RECOMMENDATION:
One practical next step.

Rules:
- Do not invent numbers.
- Only use the provided data.
- Do not assume causation.
- Do not claim one segment converts better unless conversion rates are shown.
- Keep each section to 1-2 sentences.
- Keep the full response under 100 words.
- Do not use markdown bullets.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )

        return response.text.strip()

    except ClientError as error:
        if error.code == 429:
            raise RuntimeError(
                "Gemini's usage limit has been reached. "
                "Please try again after the quota resets."
            ) from error

        raise RuntimeError(
            "Gemini could not generate the insight."
        ) from error