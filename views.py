"""Enterprise page layouts (Streamlit)."""

from __future__ import annotations

import random
import uuid
from datetime import datetime
from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from openai import OpenAI

import analysis
import mock_data


def _init_session() -> None:
    defaults: dict[str, Any] = {
        "page": "dashboard",
        "demo_mode": False,
        "threads": {},
        "active_thread": None,
        "sn_selected": None,
        "sn_ai_cache": {},
        "automation_runs": {},
        "chart_range": 30,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
    if not st.session_state.threads:
        tid = str(uuid.uuid4())[:8]
        st.session_state.threads = {
            tid: {"title": "New conversation", "messages": []},
        }
        st.session_state.active_thread = tid


def render_top_bar() -> None:
    st.markdown(
        '<p style="font-size:1.35rem;font-weight:700;color:#0f172a;margin:0 0 0.25rem 0;">'
        "AI Support Assistant"
        '<span class="ai-gradient-text" style="margin-left:10px;font-size:0.95rem;">AIOps</span>'
        "</p>"
        '<p style="color:#64748b;margin:0 0 1rem 0;font-size:0.9rem;">Enterprise IT operations copilot</p>',
        unsafe_allow_html=True,
    )
    c1, c2, c3, c4 = st.columns([4.2, 0.35, 0.35, 0.35])
    with c1:
        st.text_input(
            "global_search",
            placeholder="🔎  Search incidents, knowledge, devices…",
            label_visibility="collapsed",
            key="header_search_dummy",
        )
    with c2:
        st.caption("🔔")
    with c3:
        st.caption("💬")
    with c4:
        st.caption("👤")


def _nav_button(label: str, icon: str, page_id: str) -> None:
    active = st.session_state.page == page_id
    face = f"{icon}  {label}"
    btype = "primary" if active else "secondary"
    if st.button(face, use_container_width=True, type=btype, key=f"nav_{page_id}"):
        st.session_state.page = page_id
        st.rerun()


def render_sidebar_nav() -> None:
    st.markdown("##### Navigate")
    _nav_button("Dashboard", "📊", "dashboard")
    _nav_button("AI Chat Assistant", "💬", "chat")
    _nav_button("Incidents", "🎫", "incidents")
    _nav_button("AIOps Insights", "🧠", "aiops")
    _nav_button("Automation", "⚙️", "automation")
    _nav_button("Analytics", "📈", "analytics")
    _nav_button("Settings", "🔧", "settings")
    st.divider()
    st.caption("Assistant")
    st.checkbox(
        "Demo mode (no API)",
        help="Offline structured responses — no OpenAI usage.",
        key="demo_mode",
    )
    st.caption(
        "[OpenAI billing](https://platform.openai.com/account/billing) · "
        "[ServiceNow](https://www.servicenow.com/) (simulated)"
    )


def render_dashboard() -> None:
    m = mock_data.metric_cards()
    st.markdown("### Dashboard overview")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("Total incidents", f"{m['total_incidents']:,}")
    with c2:
        st.metric("Open", m["open_incidents"])
    with c3:
        st.metric("Resolved today", m["resolved_today"])
    with c4:
        st.metric("Automation success", f"{m['automation_success_pct']}%")
    with c5:
        st.metric("Avg resolution", f"{m['avg_resolution_hours']} h")

    st.divider()
    r = st.radio("Trend window", ["Last 7 days", "Last 30 days"], horizontal=True, key="dash_trend_win")
    days = 7 if r.startswith("Last 7") else 30
    trend = mock_data.incident_trend_df(days)

    g1, g2 = st.columns((1.55, 1.0))
    with g1:
        with st.container(border=True):
            st.markdown("**Incident trends**")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=trend["date"], y=trend["opened"], name="Opened", line=dict(color="#4f46e5", width=2)))
            fig.add_trace(go.Scatter(x=trend["date"], y=trend["resolved"], name="Resolved", line=dict(color="#059669", width=2)))
            fig.update_layout(
                height=320,
                margin=dict(l=10, r=10, t=30, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(248,250,252,0.9)",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                font=dict(family="DM Sans, sans-serif", color="#334155"),
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=True, gridcolor="#e2e8f0")
            st.plotly_chart(fig, use_container_width=True, key="dash_line")
    with g2:
        with st.container(border=True):
            st.markdown("**Incident categories**")
            cat = mock_data.incident_categories_df()
            fig2 = px.pie(cat, values="count", names="category", hole=0.55, color_discrete_sequence=px.colors.sequential.Purple_r)
            fig2.update_layout(height=320, margin=dict(t=30, b=10, l=10, r=10), showlegend=True, paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#334155"))
            st.plotly_chart(fig2, use_container_width=True, key="dash_pie")

    with st.container(border=True):
        st.markdown("**Resolution performance by team**")
        perf = mock_data.resolution_performance_df()
        fig3 = go.Figure(
            data=[
                go.Bar(name="Within SLA %", x=perf["team"], y=perf["within_sla_pct"], marker_color="#6366f1"),
                go.Bar(name="Avg hours", x=perf["team"], y=perf["avg_hours"], marker_color="#38bdf8", yaxis="y2"),
            ]
        )
        fig3.update_layout(
            height=340,
            barmode="group",
            margin=dict(l=40, r=40, t=30, b=40),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(248,250,252,0.9)",
            yaxis=dict(title="SLA %", range=[0, 100]),
            yaxis2=dict(title="Hours", overlaying="y", side="right", showgrid=False),
            font=dict(family="DM Sans, sans-serif", color="#334155"),
            legend=dict(orientation="h", y=1.1),
        )
        st.plotly_chart(fig3, use_container_width=True, key="dash_bar")


def _active_messages() -> list[dict[str, Any]]:
    tid = st.session_state.active_thread
    return st.session_state.threads[tid]["messages"]


def _new_thread() -> None:
    tid = str(uuid.uuid4())[:8]
    st.session_state.threads[tid] = {"title": "New conversation", "messages": []}
    st.session_state.active_thread = tid


def render_chat_area(openai_client: OpenAI | None, demo_mode: bool) -> None:
    st.markdown("### AI Chat Assistant")
    st.caption("Describe an issue — responses include summary, root cause, steps, confidence, and related incidents.")

    hist, main = st.columns([0.28, 0.72], gap="medium")
    with hist:
        with st.container(border=True):
            st.markdown("**Conversations**")
            if st.button("+ New conversation", use_container_width=True, key="new_conv"):
                _new_thread()
                st.rerun()
            for tid, data in list(st.session_state.threads.items())[::-1][:12]:
                title = data["title"][:42] + ("…" if len(data["title"]) > 42 else "")
                label = f"{'● ' if tid == st.session_state.active_thread else '○ '}{title}"
                if st.button(label, key=f"th_{tid}", use_container_width=True):
                    st.session_state.active_thread = tid
                    st.rerun()

    with main:
        msgs = _active_messages()
        for idx, msg in enumerate(msgs):
            with st.chat_message(msg["role"]):
                if msg["role"] == "assistant" and msg.get("structured"):
                    _render_structured_analysis(msg["structured"], key_prefix=f"m{idx}")
                elif msg["role"] == "assistant" and msg.get("content"):
                    st.markdown(msg["content"])
                else:
                    st.markdown(msg.get("content", ""))

        if prompt := st.chat_input("Describe the IT issue (e.g. VPN not working for user)…"):
            if len(msgs) == 0:
                st.session_state.threads[st.session_state.active_thread]["title"] = (
                    prompt[:48] + ("…" if len(prompt) > 48 else "")
                )
            msgs.append({"role": "user", "content": prompt})
            with st.spinner("AI is analyzing…"):
                structured = _run_analysis(prompt, openai_client, demo_mode)
            if structured.get("_error"):
                msgs.append(
                    {
                        "role": "assistant",
                        "content": structured["_error"],
                        "structured": None,
                    }
                )
            else:
                msgs.append({"role": "assistant", "content": "", "structured": structured})
            st.rerun()


def _run_analysis(issue: str, client: OpenAI | None, demo: bool) -> dict[str, Any]:
    try:
        if demo:
            return analysis.analyze_structured_demo(issue)
        if not client:
            return {"_error": "No API key. Enable Demo mode or set OPENAI_API_KEY in `.env`."}
        return analysis.analyze_structured_api(client, issue)
    except Exception as e:
        friendly = analysis.friendly_api_message(e)
        if friendly:
            return {"_error": friendly}
        return {"_error": f"Request failed: {e}"}


def _render_structured_analysis(d: dict[str, Any], key_prefix: str = "r") -> None:
    if d.get("_error"):
        st.markdown(d["_error"])
        return
    st.markdown(
        '<div style="background:linear-gradient(135deg,rgba(99,102,241,0.12),rgba(37,99,235,0.08));'
        'border:1px solid rgba(99,102,241,0.25);border-radius:14px;padding:14px 16px;margin-bottom:12px;">'
        "<strong style='color:#312e81;'>Copilot output</strong>"
        "<span style='color:#64748b;font-size:0.85rem;margin-left:8px;'>Structured triage</span></div>",
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown("##### 🔍 Issue summary")
            st.write(d.get("summary", ""))
    with c2:
        with st.container(border=True):
            st.markdown("##### ⚠️ Possible root cause")
            st.markdown(d.get("root_cause", ""))
    with st.container(border=True):
        st.markdown("##### 🛠️ Suggested resolution steps")
        for i, step in enumerate(d.get("resolution_steps") or [], start=1):
            st.markdown(f"{i}. {step}")
    c3, c4 = st.columns([0.45, 0.55])
    with c3:
        with st.container(border=True):
            st.markdown("##### 📊 Confidence")
            conf = int(d.get("confidence", 0))
            st.progress(min(100, max(0, conf)) / 100.0)
            st.caption(f"{conf}% model confidence (indicative)")
    with c4:
        with st.container(border=True):
            st.markdown("##### 🔗 Related incidents (simulated)")
            for idx, ri in enumerate(d.get("related_incidents") or []):
                label = f"{ri.get('id', '')} — {(ri.get('title') or '')[:50]}"
                if st.button(label, key=f"{key_prefix}_rel_{ri.get('id')}_{idx}"):
                    st.session_state.sn_selected = ri.get("id")
                    st.session_state.page = "incidents"
                    st.toast("Opened Incidents workspace")
                    st.rerun()


def render_incidents(openai_client: OpenAI | None, demo_mode: bool) -> None:
    st.markdown("### Incidents · ServiceNow (simulated)")
    incs = mock_data.mock_incidents()
    left, right = st.columns([0.38, 0.62], gap="medium")

    with left:
        with st.container(border=True):
            st.markdown("**Active queue**")
            for inc in incs:
                sel = st.session_state.sn_selected == inc["number"]
                short = inc["short_description"][:44] + ("…" if len(inc["short_description"]) > 44 else "")
                if st.button(
                    f"{inc['number']} · {short}\n{inc['priority']} · {inc['state']}",
                    key=f"incpick_{inc['number']}",
                    use_container_width=True,
                    type="primary" if sel else "secondary",
                ):
                    st.session_state.sn_selected = inc["number"]
                    st.rerun()

    with right:
        inc = next((i for i in incs if i["number"] == st.session_state.sn_selected), incs[0])
        if st.session_state.sn_selected is None:
            st.session_state.sn_selected = inc["number"]

        with st.container(border=True):
            st.markdown(f"#### `{inc['number']}`")
            st.caption(f"{inc['priority']} · **{inc['state']}** · Opened {inc['opened_at']}")
            st.write(inc["short_description"])
            st.write(inc["description"])
            st.markdown(f"**Assigned to:** {inc['assigned_to']}")

        cache_key = inc["number"]
        with st.container(border=True):
            st.markdown("##### 🤖 AI analysis panel")
            if st.button("👉 Analyze with AI", type="primary", key=f"sn_ai_{cache_key}"):
                with st.spinner("AI is analyzing…"):
                    if demo_mode:
                        st.session_state.sn_ai_cache[cache_key] = analysis.analyze_incident_record_demo(inc)
                    elif openai_client:
                        try:
                            st.session_state.sn_ai_cache[cache_key] = analysis.analyze_structured_api(
                                openai_client,
                                f"Incident {inc['number']}: {inc['short_description']}\n{inc['description']}",
                            )
                        except Exception as e:
                            msg = analysis.friendly_api_message(e) or str(e)
                            st.session_state.sn_ai_cache[cache_key] = {"_error": msg}
                    else:
                        st.session_state.sn_ai_cache[cache_key] = {
                            "_error": "Set API key or use Demo mode.",
                        }
                st.toast("Analysis updated")
                st.rerun()

            cached = st.session_state.sn_ai_cache.get(cache_key)
            if cached:
                if cached.get("_error"):
                    st.markdown(cached["_error"])
                else:
                    _render_structured_analysis(cached, key_prefix=f"sn_{cache_key}")
            else:
                st.caption("Run **Analyze with AI** to populate AI summary, root cause, and suggested fix.")

        with st.expander("Similar incidents (sample)"):
            st.write("- INC0012401 — Same VPN gateway pool saturation")
            st.write("- INC0012510 — MFA push delay during peak login")


def render_aiops() -> None:
    st.markdown("### AIOps insights")
    st.caption("Illustrative analytics — connect your observability stack for live clustering.")

    rng = random.Random(7)
    clusters = []
    for cid, center in enumerate([(2, 3), (7, 8), (5, 2)]):
        for _ in range(22):
            clusters.append(
                {
                    "x": center[0] + rng.gauss(0, 0.65),
                    "y": center[1] + rng.gauss(0, 0.65),
                    "cluster": f"Theme {cid + 1}",
                }
            )
    cdf = pd.DataFrame(clusters)
    with st.container(border=True):
        st.markdown("**Incident clustering (2-D projection — simulated)**")
        fig0 = px.scatter(
            cdf,
            x="x",
            y="y",
            color="cluster",
            color_discrete_sequence=px.colors.qualitative.Bold,
        )
        fig0.update_layout(
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(248,250,252,0.9)",
            xaxis=dict(showgrid=True, gridcolor="#e2e8f0", title="Component A"),
            yaxis=dict(showgrid=True, gridcolor="#e2e8f0", title="Component B"),
            legend_title_text="Cluster",
        )
        st.plotly_chart(fig0, use_container_width=True, key="aiops_cluster")

    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown("**Top recurring issues**")
            rec = mock_data.recurring_issues()
            df = pd.DataFrame(rec, columns=["Issue", "Count"])
            fig = px.bar(df, x="Count", y="Issue", orientation="h", color="Count", color_continuous_scale="Purples")
            fig.update_layout(height=320, showlegend=False, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(248,250,252,0.9)", yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig, use_container_width=True, key="aiops_bar")
    with c2:
        with st.container(border=True):
            st.markdown("**Root cause distribution**")
            rc = mock_data.root_cause_distribution()
            fig2 = px.bar(rc, x="cause", y="pct", color="pct", color_continuous_scale="Blues")
            fig2.update_layout(height=320, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(248,250,252,0.9)", showlegend=False, xaxis_title="", yaxis_title="% share")
            st.plotly_chart(fig2, use_container_width=True, key="aiops_rc_bar")

    with st.container(border=True):
        st.markdown("**Incident heatmap (hour × weekday)**")
        hm = mock_data.incident_heatmap_df()
        fig3 = px.imshow(hm, labels=dict(x="Hour (UTC)", y="Day", color="Volume"), color_continuous_scale="Blues", aspect="auto")
        fig3.update_layout(height=360, paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#334155"))
        st.plotly_chart(fig3, use_container_width=True, key="aiops_hm")

    with st.container(border=True):
        st.markdown("##### 💡 AI recommendations")
        st.success("Reduce repeated VPN tickets by pushing a self-heal script to remote clients (pilot 10%).")
        st.info("Automate DNS flush + adapter reset for L1 — projected **~40 h/month** saved.")
        st.warning("Spike in MFA failures 09:00–11:00 UTC — schedule IdP health check with vendor.")


def render_automation() -> None:
    st.markdown("### Automation & utilities")
    st.caption("Simulated runbooks — no commands execute on your machine.")

    utilities = [
        ("Restart VPN", "Restarts VPN agent service (simulated)."),
        ("Flush DNS", "Clears local resolver cache (simulated)."),
        ("Restart Service", "Bounces a named Windows service (simulated)."),
        ("Clear Cache", "Clears temp app cache for supported clients (simulated)."),
    ]

    if "automation_runs" not in st.session_state:
        st.session_state.automation_runs = {}

    for name, desc in utilities:
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**{name}**")
                st.caption(desc)
                st_data = st.session_state.automation_runs.get(name, {"status": "—", "last": "Never"})
                st.caption(f"Last status: **{st_data['status']}** · Last run: **{st_data['last']}**")
            with c2:
                if st.button("Run", key=f"run_util_{name}"):
                    st.session_state.automation_runs[name] = {
                        "status": "Success",
                        "last": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    st.toast(f"{name} completed (simulated)")
                    st.rerun()
        with st.expander(f"Execution log — {name}", expanded=False):
            st.code("[INFO] Job queued\n[INFO] Policy check OK\n[INFO] Completed with exit 0", language="text")


def render_analytics() -> None:
    st.markdown("### Analytics")
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown("**SLA compliance trend**")
            sla = mock_data.sla_trend_df()
            fig = px.area(sla, x="date", y="sla_pct", color_discrete_sequence=["#4f46e5"])
            fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(248,250,252,0.9)", yaxis_range=[85, 100], showlegend=False)
            st.plotly_chart(fig, use_container_width=True, key="an_sla")
    with c2:
        with st.container(border=True):
            st.markdown("**Automation impact (hours saved)**")
            imp = mock_data.automation_impact_df()
            fig2 = px.line(imp, x="week", y="hours_saved", markers=True, color_discrete_sequence=["#059669"])
            fig2.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(248,250,252,0.9)", showlegend=False)
            st.plotly_chart(fig2, use_container_width=True, key="an_imp")

    with st.container(border=True):
        st.markdown("**Engineer performance (sample)**")
        eng = mock_data.engineer_performance_df()
        fig3 = go.Figure(
            data=[
                go.Bar(name="Closed", x=eng["engineer"], y=eng["tickets_closed"], marker_color="#6366f1"),
            ]
        )
        fig3.update_layout(height=320, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(248,250,252,0.9)", yaxis_title="Tickets closed")
        st.plotly_chart(fig3, use_container_width=True, key="an_eng")


def render_settings() -> None:
    st.markdown("### Settings")
    dm = st.session_state.get("demo_mode", False)
    with st.container(border=True):
        st.markdown("**Environment**")
        st.write(f"- Demo mode: **{'On' if dm else 'Off'}**")
        st.write("- ServiceNow: **simulated data** (no live CMDB connection).")
        st.write("- Charts: **Plotly** · Theme: **Enterprise light**")
    with st.expander("About this build"):
        st.write(
            "AI Support Assistant is a portfolio-style AIOps UI. "
            "Wire your real ServiceNow / observability APIs by replacing `mock_data` and REST calls."
        )


def render_page(openai_client: OpenAI | None) -> None:
    demo_mode = bool(st.session_state.get("demo_mode", False))
    page = st.session_state.page
    if page == "dashboard":
        render_dashboard()
    elif page == "chat":
        render_chat_area(openai_client, demo_mode)
    elif page == "incidents":
        render_incidents(openai_client, demo_mode)
    elif page == "aiops":
        render_aiops()
    elif page == "automation":
        render_automation()
    elif page == "analytics":
        render_analytics()
    elif page == "settings":
        render_settings()
    else:
        st.session_state.page = "dashboard"
        st.rerun()
