# -------------------------------------------------------
# FitCom - OCR Engine (FINAL - SAFE)
# -------------------------------------------------------

import cv2
import numpy as np
import pytesseract


def preprocess_image(pil_image):

    try:
        img = np.array(pil_image)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.convertScaleAbs(gray, alpha=2.5, beta=20)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)

        thresh = cv2.threshold(
            blur,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]

        return thresh

    except Exception:
        return None


def extract_text(pil_image):

    processed = preprocess_image(pil_image)

    if processed is None:
        return ""

    try:
        text = pytesseract.image_to_string(
            processed,
            config=r'--oem 3 --psm 6'
        )
        return text

    except Exception:
        return ""