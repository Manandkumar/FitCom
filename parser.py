# -------------------------------------------------------
# FitCom - Smart Body Report Parser
# Author: Anand Kumar
#
# Purpose:
# Extract fitness metrics from OCR text even when
# OCR output contains noise or partial keywords.
# -------------------------------------------------------

import re


# -------------------------------------------------------
# Extract first numeric value from a line
# -------------------------------------------------------

def extract_number(line):

    numbers = re.findall(r"\d+\.\d+|\d+", str(line))

    if numbers:
        return float(numbers[0])

    return None


# -------------------------------------------------------
# Extract all metrics from OCR text
# -------------------------------------------------------

def extract_all_metrics(text):

    metrics = {

        "Weight": None,
        "BMI": None,
        "BodyFat": None,
        "FatMass": None,
        "MuscleMass": None,
        "SkeletalMuscle": None,
        "VisceralFat": None,
        "BMR": None,
        "BodyWater": None,
        "Protein": None,
        "BoneMass": None,
        "BodyAge": None,
        "WHR": None
    }

    lines = text.lower().split("\n")

    for line in lines:

        value = extract_number(line)

        if value is None:
            continue

        # Weight
        if ("weight" in line) and metrics["Weight"] is None:
            metrics["Weight"] = value

        # BMI
        elif "bmi" in line and metrics["BMI"] is None:
            metrics["BMI"] = value

        # Body Fat
        elif ("body fat" in line or "fat %" in line) and metrics["BodyFat"] is None:
            metrics["BodyFat"] = value

        # Fat Mass
        elif ("fat mass" in line or "fat kg" in line) and metrics["FatMass"] is None:
            metrics["FatMass"] = value

        # Muscle Mass
        elif ("muscle mass" in line or "muscle" in line) and metrics["MuscleMass"] is None:
            metrics["MuscleMass"] = value

        # Skeletal Muscle
        elif ("skeletal" in line) and metrics["SkeletalMuscle"] is None:
            metrics["SkeletalMuscle"] = value

        # Visceral Fat
        elif ("visceral" in line) and metrics["VisceralFat"] is None:
            metrics["VisceralFat"] = value

        # BMR
        elif ("bmr" in line or "basal metabolic" in line) and metrics["BMR"] is None:
            metrics["BMR"] = value

        # Body Water
        elif ("water" in line) and metrics["BodyWater"] is None:
            metrics["BodyWater"] = value

        # Protein
        elif ("protein" in line) and metrics["Protein"] is None:
            metrics["Protein"] = value

        # Bone Mass
        elif ("bone" in line) and metrics["BoneMass"] is None:
            metrics["BoneMass"] = value

        # Body Age
        elif ("body age" in line or "age" in line) and metrics["BodyAge"] is None:
            metrics["BodyAge"] = value

        # WHR
        elif ("whr" in line or "waist hip" in line) and metrics["WHR"] is None:
            metrics["WHR"] = value

    return metrics