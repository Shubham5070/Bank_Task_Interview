from fastapi import FastAPI, UploadFile, Form, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import shutil
import uuid

from app.graph import run_pipeline
from app.db import Base, engine, SessionLocal, PendingRequest

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Serve UI
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.post("/submit")
async def submit(
    customer_id: str = Form(...),
    old_name: str = Form(...),
    new_name: str = Form(...),
    file: UploadFile = File(...)
):
    request_id = str(uuid.uuid4())
    file_path = f"uploads/{request_id}.png"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = run_pipeline({
        "request_id": request_id,
        "customer_id": customer_id,
        "old_name": old_name,
        "new_name": new_name,
        "file_path": file_path
    })

    return result


@app.get("/pending")
def get_pending():
    db = SessionLocal()
    records = db.query(PendingRequest).filter(
        PendingRequest.status == "AI_VERIFIED_PENDING_HUMAN"
    ).all()

    result = []
    for r in records:
        result.append({
            "request_id": r.request_id,
            "customer_id": r.customer_id,
            "old_name": r.old_value,
            "new_name": r.new_value,
            "confidence_score": r.confidence_score,
            "summary": r.summary
        })

    db.close()
    return result


@app.post("/approve/{request_id}")
def approve(request_id: str):
    db = SessionLocal()
    record = db.query(PendingRequest).filter_by(request_id=request_id).first()

    if not record:
        return {"error": "Not found"}

    record.status = "APPROVED"
    record.checker_decision = "APPROVED"
    db.commit()
    db.close()

    return {"message": "Approved and sent to RPS", "rps_response": {"status": "SUCCESS"}}


@app.post("/reject/{request_id}")
def reject(request_id: str):
    db = SessionLocal()
    record = db.query(PendingRequest).filter_by(request_id=request_id).first()

    if not record:
        return {"error": "Not found"}

    record.status = "REJECTED"
    record.checker_decision = "REJECTED"
    db.commit()
    db.close()

    return {"message": "Rejected"}