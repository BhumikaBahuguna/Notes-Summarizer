import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import cv2
import numpy as np

def preprocess_image(pil_img: Image.Image) -> Image.Image:
    """Apply basic preprocessing for better OCR."""
    img = np.array(pil_img.convert("RGB"))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Denoise & sharpen text
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    th = cv2.adaptiveThreshold(gray, 255,
                               cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 31, 10)
    return Image.fromarray(th)

def ocr_image(pil_img: Image.Image, lang: str = "eng") -> str:
    pre = preprocess_image(pil_img)
    return pytesseract.image_to_string(pre, lang=lang)

def ocr_pdf(pdf_path: str, lang: str = "eng", dpi: int = 300) -> str:
    pages = convert_from_path(pdf_path, dpi=dpi)
    texts = []
    for p in pages:
        texts.append(ocr_image(p, lang=lang))
    return "\n\n".join(texts)
if __name__ == "__main__":
    img_path = "../tests/day1.jpg"  # your test image
    text = ocr_image(Image.open(img_path), lang="eng")
    print("===== OCR OUTPUT =====")
    print(text)
