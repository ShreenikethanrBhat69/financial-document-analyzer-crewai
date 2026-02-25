from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import logging



from database import init_db, save_analysis
from crewai import Crew, Process
from agents import (
    financial_analyst,
    verifier,
    investment_advisor,
    risk_assessor
)
from task import (
    analyze_document_task,
    investment_analysis_task,
    risk_assessment_task,
    verification_task
)

# =====================================
# App + Logging Setup
# =====================================
app = FastAPI(title="Financial Document Analyzer")

# Initialize database at startup
init_db()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =====================================
# Crew Runner
# =====================================
def run_crew(query: str, file_path: str):
    """Run the CrewAI financial analysis pipeline."""

    financial_crew = Crew(
        agents=[
            financial_analyst,
            risk_assessor,
            investment_advisor,
            verifier,
        ],
        tasks=[
            analyze_document_task,
            risk_assessment_task,
            investment_analysis_task,
            verification_task,
        ],
        process=Process.sequential,
        verbose=True,
    )

    result = financial_crew.kickoff(
        inputs={
            "query": query,
            "file_path": file_path,
        }
    )

    return result


# =====================================
# Health Check
# =====================================
@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}


# =====================================
# Main Analysis Endpoint
# =====================================
@app.post("/analyze")
async def analyze_financial_document_endpoint(
    file: UploadFile = File(...),
    query: str = Form(
        default="Analyze this financial document for investment insights"
    ),
):
    """Analyze uploaded financial document."""

    file_id = str(uuid.uuid4())
    os.makedirs("data", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    file_path = f"data/financial_document_{file_id}.pdf"
    output_path = f"outputs/analysis_{file_id}.txt"

    result_text = ""
    status = "success"

    try:
        # ✅ Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # ✅ Validate query
        if not query or not query.strip():
            query = "Analyze this financial document for investment insights"

        # ✅ Run CrewAI pipeline
        response = run_crew(
            query=query.strip(),
            file_path=file_path,
        )

        result_text = str(response)

    except Exception as e:
        logger.exception("System Error occurred")

        # ✅ Capture failure but DO NOT stop persistence
        result_text = f"Analysis failed: {str(e)}"
        status = "failed"

    # =====================================
    # ✅ ALWAYS SAVE TO DATABASE (KEY FIX)
    # =====================================
    try:
        save_analysis(
            file_id,
            query,
            file.filename,
            result_text
        )
    except Exception as db_error:
        logger.exception(f"Database save failed: {db_error}")

    # =====================================
    # ✅ Save output file
    # =====================================
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result_text)
    except Exception as file_error:
        logger.exception(f"Output save failed: {file_error}")

    return {
        "status": status,
        "query": query,
        "analysis": result_text,
        "file_processed": file.filename,
        "saved_to": output_path,
    }


# =====================================
# Local Run
# =====================================
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)