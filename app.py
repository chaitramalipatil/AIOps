"""AI Support Assistant (AIOps Chatbot) — enterprise Streamlit shell."""

import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from enterprise_theme import inject_theme
import views

load_dotenv()

_api_key = os.getenv("OPENAI_API_KEY")
_client = OpenAI(api_key=_api_key) if _api_key else None

st.set_page_config(
    page_title="AI Support Assistant | AIOps",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_theme()
views._init_session()

with st.sidebar:
    st.markdown("### AI Support Assistant")
    st.caption("AIOps · IT Operations Copilot")
    st.divider()
    views.render_sidebar_nav()

views.render_top_bar()
st.divider()
views.render_page(_client)
