"""Structured IT issue analysis via OpenAI (JSON) or local demo templates."""

from __future__ import annotations

import json
import re
from typing import Any

from openai import APIStatusError, OpenAI

ANALYSIS_JSON_INSTRUCTIONS = """
Return a single JSON object only (no markdown fences) with these keys:
- "summary": string, 2-4 sentences
- "root_cause": string, bullet-style paragraph or short list as one string
- "resolution_steps": array of strings, each one clear action step
- "confidence": integer 0-100, your confidence in the diagnosis
- "related_incidents": array of objects with "id" (string like INC0012847) and "title" (string), max 4 items, plausible IT examples
"""


def nested_error_code(body: object) -> str | None:
    if not isinstance(body, dict):
        return None
    c = body.get("code")
    if isinstance(c, str):
        return c
    err = body.get("error")
    if isinstance(err, dict):
        c2 = err.get("code")
        if isinstance(c2, str):
            return c2
    return None


def api_error_code(exc: APIStatusError) -> str | None:
    if exc.code:
        return exc.code
    return nested_error_code(exc.body)


def friendly_api_message(exc: BaseException) -> str | None:
    if not isinstance(exc, APIStatusError):
        return None
    code = api_error_code(exc) or ""
    if exc.status_code == 429 and code == "insufficient_quota":
        return (
            "**OpenAI quota exhausted.** Add billing or credits: "
            "[platform.openai.com/account/billing](https://platform.openai.com/account/billing). "
            "Use **Demo mode (no API)** in the sidebar for offline responses."
        )
    if exc.status_code == 401:
        return "**Invalid API key.** Check `OPENAI_API_KEY` in `.env`."
    if exc.status_code == 429:
        return "**Rate limited.** Retry shortly or check usage on OpenAI."
    return None


def _parse_analysis_json(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("not a dict")
    return data


def normalize_analysis(raw: dict[str, Any]) -> dict[str, Any]:
    steps = raw.get("resolution_steps") or raw.get("steps") or []
    if isinstance(steps, str):
        steps = [s.strip() for s in steps.split("\n") if s.strip()]
    if not isinstance(steps, list):
        steps = []
    steps = [str(s) for s in steps if s]

    related = raw.get("related_incidents") or []
    if not isinstance(related, list):
        related = []
    clean_related = []
    for r in related[:4]:
        if isinstance(r, dict) and r.get("id"):
            clean_related.append({"id": str(r["id"]), "title": str(r.get("title", ""))})

    conf = raw.get("confidence", 72)
    try:
        conf = int(float(conf))
    except (TypeError, ValueError):
        conf = 72
    conf = max(0, min(100, conf))

    return {
        "summary": str(raw.get("summary", "")).strip() or "No summary provided.",
        "root_cause": str(raw.get("root_cause", raw.get("cause", ""))).strip()
        or "See resolution steps.",
        "resolution_steps": steps or ["Gather logs and escalate per runbook."],
        "confidence": conf,
        "related_incidents": clean_related,
    }


def analyze_structured_demo(issue: str) -> dict[str, Any]:
    low = issue.lower()
    themes: list[str] = []
    if "vpn" in low:
        themes.append("VPN / remote access")
    if any(x in low for x in ("email", "outlook", "mail")):
        themes.append("Email / collaboration")
    if any(x in low for x in ("password", "login", "mfa", "2fa", "sso")):
        themes.append("Authentication")
    if any(x in low for x in ("printer", "print")):
        themes.append("Printing")
    if any(x in low for x in ("wifi", "network", "internet", "dns")):
        themes.append("Network connectivity")
    if any(x in low for x in ("slow", "latency", "performance")):
        themes.append("Performance")
    focus = ", ".join(themes) if themes else "General IT operations"

    summary = (
        f"Reported: {issue.strip()[:280]}{'…' if len(issue.strip()) > 280 else ''} "
        f"Mapped focus areas: {focus}. Pattern suggests a mix of client configuration "
        f"and possible upstream service health checks worth validating."
    )
    root = (
        "- Session or token expiry, stale VPN profile, or split-tunnel policy mismatch.\n"
        "- Network path: corporate firewall, DNS, or proxy blocking required endpoints.\n"
        "- For auth/email: IdP sync delay, conditional access, or local credential cache."
    )
    steps = [
        "Confirm blast radius (single user vs team) and exact error strings.",
        "Verify recent changes (patch Tuesday, GPO, firewall, IdP cert rotation).",
        "Run first-line remediation: restart client, re-enroll VPN, flush DNS if policy allows.",
        "Collect logs (VPN client, Windows event, IdP sign-in) and open L2 with evidence.",
    ]
    related = [
        {"id": "INC0012847", "title": "VPN disconnects intermittently for remote users"},
        {"id": "INC0012862", "title": "MFA push not received on corporate Android"},
        {"id": "INC0012851", "title": "Outlook sync failure after mailbox migration"},
    ]
    conf = 78 if "vpn" in low else 71
    return normalize_analysis(
        {
            "summary": summary,
            "root_cause": root,
            "resolution_steps": steps,
            "confidence": conf,
            "related_incidents": related,
        }
    )


def analyze_structured_api(client: OpenAI, issue: str) -> dict[str, Any]:
    user_msg = f"""{ANALYSIS_JSON_INSTRUCTIONS}

Issue to analyze:
{issue}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an enterprise IT support copilot. Output valid JSON only.",
            },
            {"role": "user", "content": user_msg},
        ],
        response_format={"type": "json_object"},
    )
    text = response.choices[0].message.content or "{}"
    try:
        raw = _parse_analysis_json(text)
    except (json.JSONDecodeError, ValueError):
        raw = {
            "summary": text[:500],
            "root_cause": "Unable to parse model output as JSON.",
            "resolution_steps": ["Retry analysis", "Check API response format"],
            "confidence": 40,
            "related_incidents": [],
        }
    return normalize_analysis(raw)


def analyze_incident_record_demo(inc: dict) -> dict[str, Any]:
    desc = inc.get("short_description", "")
    body = f"{desc}\n\n{inc.get('description', '')}"
    out = analyze_structured_demo(body)
    out["summary"] = f"[{inc.get('number')}] {out['summary'][:200]}"
    return out
