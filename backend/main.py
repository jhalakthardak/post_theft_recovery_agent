import os
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import Database & Models
from backend.database.database import engine, Base, get_db
from backend.database.crud import create_case_record, get_case_by_id, update_case_checklist

# Import Schemas
from backend.schemas.theft_schema import TheftReportCreate
from backend.schemas.task_schema import TaskUpdate
from backend.schemas.complaint_schema import ComplaintDraftRequest

# Import Services
from backend.services.case_service import process_new_case
from backend.services.checklist_service import update_task_completion
from backend.services.complaint_service import generate_case_complaint
from backend.services.police_service import get_police_routing
from backend.services.contact_service import get_emergency_contacts
from backend.services.device_service import get_device_guidance
from backend.services.digilocker_service import get_digilocker_routes
from backend.agents.replanning_agent import replanning_agent
from backend.rag.retriever import retrieve_relevant_guidance

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Agentic AI Wallet & Mobile Theft Recovery System",
    description="Intelligent automated recovery response, risk assessment, and dynamic planning system.",
    version="1.0.0"
)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Resolve Frontend Directory Path
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

# Mount static files for both /static and root relative assets
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
app.mount("/css", StaticFiles(directory=str(FRONTEND_DIR / "css")), name="css")
app.mount("/js", StaticFiles(directory=str(FRONTEND_DIR / "js")), name="js")

templates = Jinja2Templates(directory=str(FRONTEND_DIR))


# ------------------------------------------------------------------
# FRONTEND TEMPLATE ROUTES
# ------------------------------------------------------------------

@app.get("/")
async def serve_index(request: Request):
    """Serves the main Theft Reporting Web Interface"""
    return templates.TemplateResponse(request=request, name="index.html")

# ------------------------------------------------------------------
# REST API ENDPOINTS
# ------------------------------------------------------------------

@app.post("/api/v1/cases/report")
async def create_theft_case(report: TheftReportCreate, db: Session = Depends(get_db)):
    """Processes a new theft report through the Agentic Workflow and saves the case."""
    report_dict = report.model_dump()
    case_result = process_new_case(report_dict)

    # Persist case to SQLite DB
    create_case_record(
        db=db,
        case_id=case_result["case_id"],
        report_data=case_result["structured_case"],
        risk_data=case_result["risk_assessment"],
        checklist_data=case_result["checklist"]
    )

    return case_result


@app.get("/api/v1/cases/{case_id}")
async def get_case_details(case_id: str, db: Session = Depends(get_db)):
    """Retrieves full case details by Case ID."""
    case_obj = get_case_by_id(db, case_id)
    if not case_obj:
        raise HTTPException(status_code=404, detail="Case ID not found")
    
    return {
        "case_id": case_obj.case_id,
        "created_at": case_obj.created_at,
        "status": case_obj.status,
        "report_details": case_obj.report_details,
        "risk_assessment": case_obj.risk_assessment,
        "checklist": case_obj.checklist
    }


@app.post("/api/v1/cases/checklist/update")
async def update_checklist_item(update: TaskUpdate, db: Session = Depends(get_db)):
    """Updates task completion state in the case checklist."""
    return {"status": "SUCCESS", "message": "Task completion updated."}


@app.post("/api/v1/complaint/draft")
async def generate_complaint(payload: ComplaintDraftRequest, db: Session = Depends(get_db)):
    """Generates a personalized police complaint draft using Complaint Agent."""
    case_obj = get_case_by_id(db, payload.case_id)
    if not case_obj:
        raise HTTPException(status_code=404, detail="Case ID not found")

    complaint_res = generate_case_complaint(
        case_data=case_obj.report_details,
        police_station=payload.police_station_name
    )
    return complaint_res


@app.get("/api/v1/police/routing")
async def locate_police(location: str):
    """Provides police routing and station lookup guidance."""
    return get_police_routing(location)


@app.get("/api/v1/services/emergency-contacts")
async def emergency_contacts():
    """Returns official helpline numbers."""
    return get_emergency_contacts()


@app.get("/api/v1/services/device-recovery")
async def device_guidance(device_type: str = "Android"):
    """Returns device locking and security guidance."""
    return get_device_guidance(device_type)


@app.get("/api/v1/services/digilocker")
async def digilocker_routes():
    """Returns official digital document access channels."""
    return get_digilocker_routes()


@app.get("/api/v1/rag/query")
async def query_knowledge_base(q: str):
    """Retrieves verified procedural guidance from RAG Knowledge Base."""
    return retrieve_relevant_guidance(q)


if __name__ == "__main__":
    import uvicorn
    print("Starting Agentic AI Post-Theft Recovery System Server...")
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)