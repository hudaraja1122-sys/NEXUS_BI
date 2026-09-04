from __future__ import annotations

import json
import os
from typing import Any, Dict, List
from dotenv import load_dotenv
from groq import Groq
from app.tools.analytics import (
    tool_get_kpis,
    tool_temporal_performance,
    tool_category_drilldown,
    tool_sub_entity_investigation,
    tool_discount_impact_audit,
)

load_dotenv()


def run_autonomous_investigation(dataset_id: str, user_prompt: str) -> Dict[str, Any]:
    """Executes an autonomous multi-step investigation loop with self-evaluating evidence recursion."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not configured in backend/.env")

    trace: List[Dict[str, str]] = []

    # --- STEP 1: Baseline Macro KPIs ---
    trace.append({
        "step": "Macro Audit",
        "tool": "tool_get_kpis()",
        "action": "Computing net revenue, total profit, and average discount across dataset.",
        "status": "Completed"
    })
    kpis = tool_get_kpis(dataset_id)

    # --- STEP 2: Temporal Investigation ---
    trace.append({
        "step": "Temporal Trend Analysis",
        "tool": "tool_temporal_performance()",
        "action": "Comparing quarter-over-quarter margins to detect chronological collapse.",
        "status": "Completed"
    })
    quarterly_data = tool_temporal_performance(dataset_id)

    # --- STEP 3: Dimensional Decomposition ---
    trace.append({
        "step": "Categorical Decomposition",
        "tool": "tool_category_drilldown()",
        "action": "Isolating gross margin variance across product categories.",
        "status": "Completed"
    })
    category_data = tool_category_drilldown(dataset_id)

    # --- STEP 4: AUTONOMOUS DECISION EVALUATOR (Agentic Loop) ---
    # The agent detects negative profit or margin erosion and autonomously fires a follow-up tool
    most_distressed_cat = category_data[0]["name"] if category_data else "Electronics"
    lowest_profit = category_data[0]["profit"] if category_data else 0

    recursive_product_data = []
    discount_audit_data = []

    if lowest_profit < 0 or any(q.get("profit", 0) < 0 for q in quarterly_data):
        trace.append({
            "step": "Anomaly Triggered Follow-Up",
            "tool": f"tool_sub_entity_investigation('{most_distressed_cat}')",
            "action": f"Autonomous recursion: Detected negative profit (${lowest_profit}) in '{most_distressed_cat}'. Investigating specific product root-causes.",
            "status": "Investigating"
        })
        recursive_product_data = tool_sub_entity_investigation(dataset_id, culprit_category=most_distressed_cat)

        trace.append({
            "step": "Root-Cause Correlation",
            "tool": "tool_discount_impact_audit()",
            "action": "Auditing price elasticity and discount tiers to verify margin destruction.",
            "status": "Completed"
        })
        discount_audit_data = tool_discount_impact_audit(dataset_id)
    else:
        trace.append({
            "step": "Evidence Sufficiency Check",
            "tool": "evaluator",
            "action": "Metrics within nominal bounds. No deep distress recursion triggered.",
            "status": "Completed"
        })

    # --- STEP 5: Synthesis via Groq / Llama ---
    evidence_bundle = {
        "user_query": user_prompt,
        "kpis": kpis,
        "quarterly_comparison": quarterly_data,
        "category_breakdown": category_data,
        "root_cause_products": recursive_product_data,
        "discount_tier_audit": discount_audit_data,
    }

    client = Groq(api_key=api_key)
    try:
        models = [m.id for m in client.models.list().data]
        selected_model = next((m for m in ["groq/compound-mini","groq/compound","llama-3.3-70b-versatile", "llama-3.1-70b-versatile", "llama3-70b-8192", "mixtral-8x7b-32768"] if m in models), models[0])
    except Exception:
        selected_model = "llama-3.3-70b-versatile"

    system_prompt = (
        "You are NEXUS BI, an autonomous executive AI data investigator.\n"
        "You have executed a deterministic multi-step investigation loop.\n"
        "Synthesize the provided analytical results into a grounded business report.\n"
        "Rules:\n"
        "1. Never fabricate data. Reference only the exact numbers in the calculated evidence.\n"
        "2. Detail the exact root cause discovered by the follow-up recursive step.\n"
        "3. Provide prioritized recommendations grounded in these findings.\n"
        "Return strictly valid JSON matching this schema:\n"
        "{\n"
        '  "summary_text": "2-3 concise sentences detailing what happened, why, and the root cause.",\n'
        '  "findings": [\n'
        '    {"title": "Finding Title", "metric": "-$2,470.00", "detail": "Specific calculated insight."}\n'
        "  ],\n"
        '  "recommendations": [\n'
        '    {"priority": "High" | "Medium", "action": "Actionable directive", "reason": "Calculated evidence justification"}\n'
        "  ],\n"
        '  "chart": {\n'
        '    "chart_type": "bar" | "line",\n'
        '    "title": "Chart Title",\n'
        '    "x_axis": "quarter" | "name" | "product_name" | "discount_tier",\n'
        '    "y_axis": "profit" | "value" | "total_profit"\n'
        "  },\n"
        '  "chart_source": "quarterly" | "category" | "products" | "discount"\n'
        "}"
    )

    completion = client.chat.completions.create(
        model=selected_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Evidence Bundle:\n{json.dumps(evidence_bundle)}"},
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
    )

    result = json.loads(completion.choices[0].message.content or "{}")

    # Resolve Chart Data
    chart_source = result.get("chart_source", "category")
    if chart_source == "quarterly":
        chart_data = quarterly_data
    elif chart_source == "products" and recursive_product_data:
        chart_data = recursive_product_data
    elif chart_source == "discount" and discount_audit_data:
        chart_data = discount_audit_data
    else:
        chart_data = category_data

    result["data"] = chart_data
    result["kpis"] = kpis
    result["trace"] = trace
    return result