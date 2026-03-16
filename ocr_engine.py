# -------------------------------------------------------
# FitCom - OCR Engine
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
    gray = cv2.convertScaleAbs(gray, alpha=2, beta=0)

    # Remove noise
    blur = cv2.GaussianBlur(gray, (3,3), 0)

    # Threshold
    thresh = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return thresh


def extract_text(pil_image):

    processed = preprocess_image(pil_image)

    text = pytesseract.image_to_string(
        processed,
        config="--oem 3 --psm 6"
    )

    return text