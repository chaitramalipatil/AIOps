"""Global CSS for enterprise light theme (Streamlit)."""

ENTERPRISE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&display=swap');

html, body, [class*="css"]  {
  font-family: 'DM Sans', system-ui, sans-serif;
}

.block-container {
  padding-top: 1.25rem !important;
  padding-bottom: 2rem !important;
  max-width: 1400px !important;
}

/* Light shell */
.stApp {
  background: linear-gradient(165deg, #f0f4fb 0%, #f8fafc 45%, #eef2ff 100%);
}

/* Sidebar */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #1e3a5f 0%, #172554 55%, #0f172a 100%) !important;
  border-right: 1px solid rgba(255,255,255,0.08);
}
section[data-testid="stSidebar"] * {
  color: #e2e8f0 !important;
}
section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span {
  color: #cbd5e1 !important;
}
section[data-testid="stSidebar"] .stMarkdown a {
  color: #93c5fd !important;
}

/* Primary buttons */
.stButton > button[kind="primary"] {
  background: linear-gradient(90deg, #4f46e5 0%, #2563eb 100%) !important;
  border: none !important;
  color: white !important;
  font-weight: 600 !important;
  border-radius: 10px !important;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
}
.stButton > button[kind="primary"]:hover {
  box-shadow: 0 6px 20px rgba(79, 70, 229, 0.45);
  transform: translateY(-1px);
}

.stButton > button {
  border-radius: 10px !important;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

/* Inputs */
.stTextInput input, .stTextArea textarea, [data-baseweb="textarea"] {
  border-radius: 10px !important;
  border-color: #cbd5e1 !important;
  background: #ffffff !important;
}

/* Cards (Streamlit container border) */
div[data-testid="stVerticalBlockBorderWrapper"] {
  border-radius: 14px !important;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06), 0 8px 24px rgba(15, 23, 42, 0.06) !important;
  border-color: #e2e8f0 !important;
  background: #ffffff !important;
}

/* Metrics */
[data-testid="stMetricValue"] {
  color: #0f172a !important;
  font-weight: 700 !important;
}
[data-testid="stMetricLabel"] {
  color: #64748b !important;
  font-weight: 500 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
  gap: 8px;
  background: transparent;
}
.stTabs [data-baseweb="tab"] {
  border-radius: 10px 10px 0 0;
  font-weight: 600;
}

/* Scrollbars */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 8px; }
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

/* Chat message entrance */
[data-testid="stChatMessage"] {
  animation: asstFade 0.38s ease-out;
}
@keyframes asstFade {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Gradient text utility */
.ai-gradient-text {
  background: linear-gradient(90deg, #6366f1, #2563eb, #7c3aed);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 700;
}
"""


def inject_theme() -> None:
    import streamlit as st

    st.markdown(f"<style>{ENTERPRISE_CSS}</style>", unsafe_allow_html=True)
