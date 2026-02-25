## Importing libraries and files
import os
from crewai.tools import BaseTool
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
from crewai_tools import SerperDevTool

load_dotenv()


# =====================================
# Search Tool (Web context)
# =====================================
search_tool = SerperDevTool()


# =====================================
# Financial PDF Reader Tool
# =====================================
class FinancialDocumentTool(BaseTool):
    name: str = "Financial Document Reader"
    description: str = (
        "Reads a financial PDF document and returns the extracted text "
        "for downstream financial analysis."
    )

    def _run(self, path: str = "data/sample.pdf") -> str:
        """Read and extract text from a PDF file."""
        try:
            if not os.path.exists(path):
                return f"Error: File not found at {path}"

            docs = PyPDFLoader(path).load()

            full_report = ""
            for data in docs:
                content = data.page_content
                content = content.replace("\n\n", "\n")  # optimized cleanup
                full_report += content + "\n"

            return full_report.strip()

        except Exception as e:
            return f"Error reading PDF: {str(e)}"


# Initialize the tool instance
pdf_read_tool = FinancialDocumentTool()











# ## Creating Investment Analysis Tool
# class InvestmentTool:
#     # BUG FIX: Added @tool decorator so CrewAI can use this class method
#     @tool("analyze_investment_tool")
#     def analyze_investment_tool(financial_document_data: str):
#         """Process and analyze the financial document data format."""
#         processed_data = financial_document_data
        
#         # Clean up the data format
#         i = 0
#         while i < len(processed_data):
#             if processed_data[i:i+2] == "  ":  # Remove double spaces
#                 processed_data = processed_data[:i] + processed_data[i+1:]
#             else:
#                 i += 1
                
#         return processed_data

# ## Creating Risk Assessment Tool
# class RiskTool:
#     # BUG FIX: Added @tool decorator
#     @tool("create_risk_assessment_tool")
#     def create_risk_assessment_tool(financial_document_data: str):        
#         """Tool for risk assessment logic."""
#         return f"Risk assessment initialized for data: {financial_document_data[:50]}..."