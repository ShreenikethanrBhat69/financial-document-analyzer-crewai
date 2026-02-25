# Financial Document Analyzer (CrewAI Debug Assignment)

## Overview

This project is a **multi-agent financial document analysis system** built using CrewAI and FastAPI.  
The original codebase contained multiple deterministic bugs and inefficient prompts. These issues have been identified, fixed, and enhanced to produce reliable, production-ready financial insights.

The system allows users to upload financial PDF documents and receive structured analysis including financial insights, risk evaluation, and investment recommendations.

---

## ✅ Bugs Identified & Fixed

###  Deterministic Code Fixes

- Fixed incorrect LLM initialization (`llm = llm` bug)
- Corrected tool configuration (`tool` → `tools`)
- Replaced broken PDF loader with `PyPDFLoader`
- Fixed task naming conflicts
- Ensured proper Crew input propagation (`query`, `file_path`)
- Implemented safe file cleanup
- Fixed requirements installation typo
- Improved error handling across pipeline

---

###  Prompt Engineering Improvements

- Removed hallucination-encouraging instructions
- Enforced document-grounded financial analysis
- Standardized agent goals using `{query}`
- Improved professional tone across agents
- Added structured expected outputs
- Reduced randomness using lower temperature

---

###  Architecture Improvements

- Implemented sequential multi-agent workflow
- Added task dependency chaining
- Improved logging and observability
- Enabled dynamic PDF upload via API (replacing static `sample.pdf`)
- Added fault-tolerant execution flow

---

##  Bonus Implementation — Database Integration

Implemented SQLite persistence to store analysis results and metadata.

**Features:**

- Automatic database initialization  
- Stores query, filename, and results  
- Fault-tolerant saving (even if AI call fails)  
- Enables future analytics and auditing  

**Database:** `analysis.db`  
**Table:** `analyses`

---

## System Architecture

### Agents

1. Financial Analyst — extracts financial insights  
2. Risk Assessor — evaluates potential risks  
3. Investment Advisor — provides recommendations  
4. Compliance Verifier — validates accuracy  

### Processing Flow

PDF Upload → Financial Analysis → Risk Assessment → Investment Advice → Verification

---

## Setup Instructions

Follow the steps below to run the project locally.

---

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-url>
cd financial-document-analyzer-crewai
```

---

### 2️⃣ Create Virtual Environment

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment:

**Windows (PowerShell / CMD)**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

You should now see `(venv)` in your terminal.

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_key
SERPER_API_KEY=your_serper_key
```

⚠️ Valid OpenAI billing is required.

---

### 5️⃣ Run the Application

```bash
uvicorn main:app --reload
```

---

##  API Documentation

After starting the server, open:

http://127.0.0.1:8000/docs

---

###  POST `/analyze`

Upload a financial PDF to receive:

- financial analysis  
- risk assessment  
- investment recommendation  
- verification report  

**Request:** multipart/form-data  
**Field:** `file`

---

## Sample Test

You may upload:

- Tesla financial report  
- Any corporate financial PDF  

The system supports **dynamic uploads** instead of relying on a static `sample.pdf`.

---

##  Notes

- Designed for deterministic financial analysis  
- Handles failures gracefully  
- Results persist even if AI quota fails  
- Built with scalability and observability in mind  

---

## Author

**Shreenikethan R Bhat**

---

## 🏁 Submission Status

✅ Deterministic bugs fixed  
✅ Prompt quality improved  
✅ Multi-agent pipeline working  
✅ FastAPI integration complete  
✅ Database bonus implemented  
