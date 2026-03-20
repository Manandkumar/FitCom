# -------------------------------------------------------
# FitCom - Smart Parser (FINAL - SAFE + DB ALIGNED)
# -------------------------------------------------------

import re


def extract_number(line):
    numbers = re.findall(r"\d+\.\d+|\d+", str(line))
    return float(numbers[0]) if numbers else None


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
        "ProteinMass": None,  # 🔥 fixed
        "BoneMass": None,
        "BodyAge": None,
        "WHR": None
    }

    lines = text.lower().split("\n")

    for line in lines:

        value = extract_number(line)

        if value is None:
            continue

        if "weight" in line and not metrics["Weight"]:
            metrics["Weight"] = value

        elif "bmi" in line and not metrics["BMI"]:
            metrics["BMI"] = value

        elif "body fat" in line or "fat %" in line:
            if not metrics["BodyFat"]:
                metrics["BodyFat"] = value

        elif "fat mass" in line:
            if not metrics["FatMass"]:
                metrics["FatMass"] = value

        elif "muscle" in line:
            if not metrics["MuscleMass"]:
                metrics["MuscleMass"] = value

        elif "skeletal" in line:
            if not metrics["SkeletalMuscle"]:
                metrics["SkeletalMuscle"] = value

        elif "visceral" in line:
            if not metrics["VisceralFat"]:
                metrics["VisceralFat"] = value

        elif "bmr" in line:
            if not metrics["BMR"]:
                metrics["BMR"] = value

        elif "water" in line:
            if not metrics["BodyWater"]:
                metrics["BodyWater"] = value

        elif "protein" in line:
            if not metrics["ProteinMass"]:
                metrics["ProteinMass"] = value

        elif "bone" in line:
            if not metrics["BoneMass"]:
                metrics["BoneMass"] = value

        elif "body age" in line or "age" in line:
            if not metrics["BodyAge"]:
                metrics["BodyAge"] = value

        elif "whr" in line:
            if not metrics["WHR"]:
                metrics["WHR"] = value

    return metrics