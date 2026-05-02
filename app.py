import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

_api_key = os.getenv("OPENAI_API_KEY")
_client = OpenAI(api_key=_api_key) if _api_key else None

st.set_page_config(page_title="AI Support Assistant", page_icon="🤖")

st.title("🤖 AI Support Assistant")
st.write("Enter your IT issue below:")

user_input = st.text_area("Describe your issue", height=150, placeholder="e.g. VPN not working for user")


def analyze_issue(issue: str) -> str:
    if not _client:
        raise ValueError(
            "OPENAI_API_KEY is not set. Copy `.env.example` to `.env` and add your key."
        )
    prompt = f"""
You are an IT support assistant.

Analyze the issue and provide:
- Summary
- Root cause
- Resolution steps

Issue: {issue}
"""
    response = _client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content or ""


if st.button("Analyze Issue"):
    if not user_input.strip():
        st.warning("Please enter an issue")
    elif not _client:
        st.error(
            "Missing OpenAI API key. Create a `.env` file with `OPENAI_API_KEY=...` "
            "(see `.env.example`)."
        )
    else:
        with st.spinner("Analyzing..."):
            try:
                result = analyze_issue(user_input.strip())
            except Exception as e:
                st.error(f"Request failed: {e}")
            else:
                st.success("Analysis complete")
                st.markdown(result)
