import pytesseract
from PIL import Image

# 🔥 MUST ADD THIS
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = Image.open("test.png")
text = pytesseract.image_to_string(img)

print("\n--- OCR OUTPUT ---\n")
print(text if text.strip() else "⚠️ No text detected")