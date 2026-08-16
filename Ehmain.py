"""
EHEPS International Organization - Vertex AI Core Platform Engine
Deployable on Google Cloud Run with Vertex AI and BigQuery integration.
"""

import os
import json
import logging
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting, HarmCategory, HarmBlockThreshold
from google.cloud import bigquery
from google.cloud import secretmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("eheps_ai_engine")

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "eheps-ai-platform")
REGION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=REGION)

# Gemini Model Definition
ai_model = GenerativeModel(
    model_name="gemini-1.5-pro-preview-0409",
    system_instruction=[
        "You are the central AI Engine for EHEPS International Organization.",
        "Your mission is to support humanitarian relief, grant proposals, and educational programs.",
        "You must support high-accuracy translations and extraction across English, Dari (دری), and Pashto (پښتو).",
        "Maintain strict neutrality, auditable references, and data confidentiality."
    ]
)

# BigQuery Client for Vector and Audit Logs
bq_client = bigquery.Client(project=PROJECT_ID)

app = FastAPI(
    title="EHEPS AI Platform API",
    description="Multilingual Humanitarian & Grant Intelligence API on Vertex AI",
    version="1.0.0"
)

class AIRequest(BaseModel):
    action: str
    text: str
    source_email: Optional[str] = "executive@eheps.com"
    target_language: Optional[str] = "Dari"

class AIResponse(BaseModel):
    status: str
    action: str
    output: str
    model_used: str

def log_audit_event(source: str, action: str, length: int):
    """Asynchronously logs transaction metadata to BigQuery for NGO compliance."""
    try:
        table_id = f"{PROJECT_ID}.audit_dataset.ai_access_logs"
        rows_to_insert = [{
            "timestamp": bigquery.Timestamp.now(),
            "source_identity": source,
            "action_executed": action,
            "input_char_length": length
        }]
        bq_client.insert_rows_json(table_id, rows_to_insert)
    except Exception as e:
        logger.warning(f"Audit log insertion skipped: {e}")

@app.get("/health")
def health_check():
    return {"status": "operational", "organization": "EHEPS International Organization"}

@app.post("/api/v1/process", response_model=AIResponse)
async def process_ai_task(request: AIRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Text payload cannot be empty.")

    # Tailor prompts by action
    if request.action == "multilingual_summary":
        prompt = (
            f"Provide a structured humanitarian summary of the following document. "
            f"Output the summary in three distinct sections: English, Dari (Farsi-Kabuli), and Pashto.\n\n"
            f"Document Content:\n{request.text}"
        )
    elif request.action == "grant_check":
        prompt = (
            f"Analyze this grant request or RFP. Extract key compliance criteria, submission deadlines, "
            f"eligible funding ceilings, and required humanitarian KPIs:\n\n{request.text}"
        )
    elif request.action == "humanitarian_extract":
        prompt = (
            f"Extract all quantitative and qualitative metrics from this field report: "
            f"beneficiary counts, aid items distributed, locations in Afghanistan or international regions, "
            f"and urgent supply deficits:\n\n{request.text}"
        )
    else:
        prompt = f"Analyze and respond to the following request accurately:\n\n{request.text}"

    try:
        response = ai_model.generate_content(
            prompt,
            generation_config={"temperature": 0.2, "max_output_tokens": 4096}
        )
        
        # Log audit entry
        log_audit_event(request.source_email, request.action, len(request.text))

        return AIResponse(
            status="success",
            action=request.action,
            output=response.text,
            model_used="gemini-1.5-pro"
        )
    except Exception as err:
        logger.error(f"Vertex AI Generation Error: {str(err)}")
        raise HTTPException(status_code=500, detail=f"AI Engine Error: {str(err)}")
