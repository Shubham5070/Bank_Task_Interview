import pytesseract
from PIL import Image
from rapidfuzz import fuzz
import ollama
import json

# Windows fix
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def validate(data):
    data["validation_passed"] = data["old_name"] != data["new_name"]
    return data


def run_ocr(data):
    img = Image.open(data["file_path"]).convert("L")
    text = pytesseract.image_to_string(img)
    data["raw_text"] = text.strip()
    return data


def extract_fields(data):
    prompt = f"""
    Determine if this is a marriage certificate.

    If YES:
    Extract:
    - Bride Name
    - Married Name

    If NO:
    return:
    {{
      "is_valid_doc": false
    }}

    If YES:
    return:
    {{
      "is_valid_doc": true,
      "bride_name": "...",
      "married_name": "..."
    }}

    Document:
    {data["raw_text"]}
    """

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        content = response["message"]["content"]
        start = content.find("{")
        end = content.rfind("}") + 1
        extracted = json.loads(content[start:end])
    except:
        extracted = {"is_valid_doc": False}

    data["is_valid_doc"] = extracted.get("is_valid_doc", False)
    data["extracted_old"] = extracted.get("bride_name", "")
    data["extracted_new"] = extracted.get("married_name", "")

    return data


def score(data):
    if not data.get("is_valid_doc"):
        data["confidence_score"] = 10
        return data

    old_score = fuzz.ratio(data["old_name"], data["extracted_old"])
    new_score = fuzz.ratio(data["new_name"], data["extracted_new"])

    data["confidence_score"] = (old_score + new_score) / 2
    return data


def generate_summary(data):
    prompt = f"""
    You are a banking verification assistant.

    Old Name: {data['old_name']}
    Extracted Old: {data['extracted_old']}
    New Name: {data['new_name']}
    Extracted New: {data['extracted_new']}
    Confidence: {data['confidence_score']}

    Give:
    - Short Summary
    - Recommendation (APPROVE or REJECT)
    """

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )
    data["summary"] = response["message"]["content"]
    return data