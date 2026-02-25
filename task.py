## Importing libraries and files
from crewai import Task
from agents import (
    financial_analyst,
    verifier,
    investment_advisor,
    risk_assessor
)
from tools import pdf_read_tool, search_tool


# ==========================================
# Financial Analysis Task
# ==========================================
analyze_document_task = Task(
    description=(
        "Analyze the financial document at {file_path} to address the user's query: {query}. "
        "Extract key financial metrics, revenue trends, profitability indicators, "
        "and important operational highlights. Base all findings strictly on the document."
    ),
    expected_output=(
        "A detailed financial analysis report containing relevant KPIs, "
        "supporting figures from the document, and a clear summary of fiscal health."
    ),
    agent=financial_analyst,
    tools=[pdf_read_tool, search_tool],
    async_execution=False,
)


# ==========================================
# Risk Assessment Task
# ==========================================
risk_assessment_task = Task(
    description=(
        "Using the financial analysis, identify and evaluate major risks mentioned "
        "in the financial document at {file_path} relevant to the query: {query}. "
        "Focus on market, credit, liquidity, and operational risks."
    ),
    expected_output=(
        "A structured risk assessment outlining the top 3–5 risks, their "
        "potential business impact, and practical mitigation considerations."
    ),
    agent=risk_assessor,
    tools=[pdf_read_tool, search_tool],
    context=[analyze_document_task],  # ✅ chained
    async_execution=False,
)


# ==========================================
# Investment Strategy Task
# ==========================================
investment_analysis_task = Task(
    description=(
        "Based on the financial and risk analysis of {file_path}, develop "
        "professional investment insights relevant to the query: {query}. "
        "Evaluate growth potential, valuation signals, and strategic outlook."
    ),
    expected_output=(
        "A structured investment recommendation (buy/sell/hold) supported by "
        "financial evidence, growth drivers, and risk considerations."
    ),
    agent=investment_advisor,
    tools=[pdf_read_tool, search_tool],
    context=[analyze_document_task, risk_assessment_task],  # ✅ chained
    async_execution=False,
)


# ==========================================
# Verification Task
# ==========================================
verification_task = Task(
    description=(
        "Review the complete financial, risk, and investment analysis for accuracy. "
        "Verify that all claims are supported by the source document at {file_path}."
    ),
    expected_output=(
        "A verification statement confirming factual accuracy, noting any "
        "unsupported claims, inconsistencies, or confirming full compliance."
    ),
    agent=verifier,
    tools=[pdf_read_tool],
    context=[
        analyze_document_task,
        risk_assessment_task,
        investment_analysis_task
    ],  # ✅ full validation chain
    async_execution=False,
)