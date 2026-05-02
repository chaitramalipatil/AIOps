"""Sample enterprise data for dashboard, incidents, and analytics (simulated)."""

from __future__ import annotations

from datetime import datetime, timedelta
import random

import pandas as pd

random.seed(42)


def metric_cards() -> dict[str, int | float]:
    return {
        "total_incidents": 1847,
        "open_incidents": 63,
        "resolved_today": 24,
        "automation_success_pct": 94.2,
        "avg_resolution_hours": 4.6,
    }


def incident_trend_df(days: int = 30) -> pd.DataFrame:
    end = datetime.now().date()
    dates = [end - timedelta(days=i) for i in range(days - 1, -1, -1)]
    opened = [random.randint(8, 28) for _ in dates]
    resolved = [max(0, o - random.randint(-3, 5)) for o in opened]
    return pd.DataFrame({"date": dates, "opened": opened, "resolved": resolved})


def incident_categories_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "category": ["Network", "Access", "Email", "Hardware", "Application", "Other"],
            "count": [412, 318, 276, 198, 156, 87],
        }
    )


def resolution_performance_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "team": ["L1", "L2", "L3", "Automation"],
            "within_sla_pct": [88, 91, 96, 99],
            "avg_hours": [2.1, 5.4, 12.8, 0.3],
        }
    )


def mock_incidents() -> list[dict]:
    now = datetime.now()
    return [
        {
            "number": "INC0012847",
            "short_description": "VPN disconnects intermittently for remote users",
            "priority": "2 - High",
            "state": "In Progress",
            "description": "Users on GlobalProtect report drops every 20–40 minutes. Affects ~15 users since Tuesday.",
            "opened_at": (now - timedelta(days=2)).strftime("%Y-%m-%d %H:%M"),
            "assigned_to": "N. Park (Network)",
        },
        {
            "number": "INC0012851",
            "short_description": "Outlook sync failure after mailbox migration",
            "priority": "3 - Moderate",
            "state": "New",
            "description": "Mailbox moved to Exchange Online; OST rebuild stuck at 78%. Multiple users same building.",
            "opened_at": (now - timedelta(hours=8)).strftime("%Y-%m-%d %H:%M"),
            "assigned_to": "Unassigned",
        },
        {
            "number": "INC0012854",
            "short_description": "SAP GUI timeout on finance VLAN",
            "priority": "2 - High",
            "state": "On Hold",
            "description": "Vendor engaged. Firewall logs show intermittent RST from proxy cluster B.",
            "opened_at": (now - timedelta(days=1)).strftime("%Y-%m-%d %H:%M"),
            "assigned_to": "R. Chen (Apps)",
        },
        {
            "number": "INC0012859",
            "short_description": "Printer queue stuck — Building C Floor 3",
            "priority": "4 - Low",
            "state": "Resolved",
            "description": "Spooler service restarted; driver updated to v4.2. Issue cleared.",
            "opened_at": (now - timedelta(days=3)).strftime("%Y-%m-%d %H:%M"),
            "assigned_to": "M. Silva (Desktop)",
        },
        {
            "number": "INC0012862",
            "short_description": "MFA push not received on corporate Android",
            "priority": "3 - Moderate",
            "state": "In Progress",
            "description": "Entra ID sign-in logs show successful policy match; device push channel errors spike 09:00–11:00 UTC.",
            "opened_at": (now - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M"),
            "assigned_to": "J. Okonkwo (Identity)",
        },
    ]


def recurring_issues() -> list[tuple[str, int]]:
    return [
        ("VPN / remote access drops", 142),
        ("Password & MFA resets", 98),
        ("Email sync & calendar", 76),
        ("Printer & scanning", 54),
        ("Wi‑Fi guest portal", 41),
    ]


def root_cause_distribution() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "cause": ["Config change", "Capacity", "Third-party", "User error", "Unknown"],
            "pct": [22, 18, 26, 14, 20],
        }
    )


def incident_heatmap_df() -> pd.DataFrame:
    hours = [f"{h:02d}:00" for h in range(8, 20)]
    days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    data = [[random.randint(2, 18) for _ in hours] for _ in days]
    return pd.DataFrame(data, index=days, columns=hours)


def sla_trend_df() -> pd.DataFrame:
    end = datetime.now().date()
    dates = [end - timedelta(days=i) for i in range(13, -1, -1)]
    return pd.DataFrame(
        {
            "date": dates,
            "sla_pct": [round(91 + random.random() * 6, 1) for _ in dates],
        }
    )


def engineer_performance_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "engineer": ["A. Kumar", "L. Rossi", "S. Tan", "P. Meyer", "K. Jones"],
            "tickets_closed": [48, 52, 39, 44, 41],
            "csat": [4.6, 4.8, 4.4, 4.7, 4.5],
        }
    )


def automation_impact_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "week": ["W1", "W2", "W3", "W4"],
            "hours_saved": [120, 142, 138, 155],
        }
    )
