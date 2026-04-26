from app.agents import *
from app.db import SessionLocal, PendingRequest


def store_to_db(data):
    db = SessionLocal()

    record = PendingRequest(
        request_id=data["request_id"],
        customer_id=data["customer_id"],
        change_type="NAME_CHANGE",
        old_value=data["old_name"],
        new_value=data["new_name"],
        extracted_old=data.get("extracted_old", ""),
        extracted_new=data.get("extracted_new", ""),
        confidence_score=data.get("confidence_score", 0),
        status="AI_VERIFIED_PENDING_HUMAN",
        summary=data.get("summary", ""),
        file_path=data["file_path"]
    )

    db.add(record)
    db.commit()
    db.close()

    return data


def run_pipeline(data):
    data = validate(data)
    if not data["validation_passed"]:
        return data

    data = run_ocr(data)
    data = extract_fields(data)
    data = score(data)
    data = generate_summary(data)
    data = store_to_db(data)

    return data