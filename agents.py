## Importing libraries and files
import os
from crewai import LLM, Agent
from dotenv import load_dotenv

load_dotenv()

# Import the tool instances from tools.py
from tools import pdf_read_tool, search_tool


# ================================
# LLM Configuration
# ================================
# Lower temperature for more deterministic financial outputs
llm = LLM(
    model="gpt-4o-mini",
    temperature=0.2
)


# ================================
# Financial Analyst Agent
# ================================
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal=(
        "Provide accurate, data-driven financial insights based strictly "
        "on the provided document for the query: {query}"
    ),
    verbose=True,
    memory=True,  # Analyst benefits from memory
    backstory=(
        "You are a seasoned Senior Financial Analyst with extensive experience "
        "interpreting corporate financial statements. You prioritize objectivity, "
        "accuracy, and rely strictly on verifiable financial data."
    ),
    tools=[pdf_read_tool, search_tool],
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=False  # safer for controlled pipeline
)


# ================================
# Compliance Verifier Agent
# ================================
verifier = Agent(
    role="Financial Compliance Auditor",
    goal=(
        "Verify the accuracy of the financial analysis for the query: {query} "
        "against the original source document."
    ),
    verbose=True,
    memory=False,  # memory not needed
    backstory=(
        "You are a meticulous compliance officer responsible for validating that "
        "every financial claim is supported by the uploaded document. You strictly "
        "prevent hallucinations and enforce regulatory standards."
    ),
    tools=[pdf_read_tool],
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=False
)


# ================================
# Investment Advisor Agent
# ================================
investment_advisor = Agent(
    role="Investment Strategy Specialist",
    goal=(
        "Formulate sustainable investment recommendations for the query: {query} "
        "based only on verified financial data."
    ),
    verbose=True,
    memory=False,
    backstory=(
        "You are a certified investment strategist focused on long-term value "
        "creation. You provide balanced, risk-aware investment recommendations "
        "based strictly on validated financial insights."
    ),
    tools=[pdf_read_tool, search_tool],
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=False
)


# ================================
# Risk Assessor Agent
# ================================
risk_assessor = Agent(
    role="Financial Risk Manager",
    goal=(
        "Identify and quantify financial, market, and operational risks "
        "related to the query: {query}."
    ),
    verbose=True,
    memory=False,
    backstory=(
        "You are an expert in financial risk management. You use both quantitative "
        "and qualitative analysis to identify vulnerabilities and clearly "
        "communicate potential downside risks to stakeholders."
    ),
    tools=[pdf_read_tool, search_tool],
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=False
)