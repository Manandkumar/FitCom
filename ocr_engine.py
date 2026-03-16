# -------------------------------------------------------
# FitCom - Enhanced OCR Engine
# Author: Anand Kumar
# -------------------------------------------------------

import cv2
import numpy as np
import pytesseract


def preprocess_image(pil_image):

    img = np.array(pil_image)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Increase contrast
    gray = cv2.convertScaleAbs(gray, alpha=2.5, beta=20)

    # Remove noise
    blur = cv2.GaussianBlur(gray, (3,3), 0)

    # Threshold
    thresh = cv2.threshold(
        blur,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    return thresh


def extract_text(pil_image):

    processed = preprocess_image(pil_image)

    # OCR configuration
    custom_config = r'--oem 3 --psm 6'

    text = pytesseract.image_to_string(
        processed,
        config=custom_config
    )

    return text