# ============================================================
# FitCom - AI Coach Engine (FINAL - SAFE)
# ============================================================

def generate_ai_advice(row):

    advice = []

    bmi = float(row.get("BMI", 0) or 0)
    bodyfat = float(row.get("BodyFat", 0) or 0)
    muscle = float(row.get("MuscleMass", 0) or 0)
    water = float(row.get("BodyWater", 0) or 0)
    visceral = float(row.get("VisceralFat", 0) or 0)

    # BMI
    if bmi > 25:
        advice.append("Your BMI is slightly high. Focus on fat reduction.")
    elif bmi < 18:
        advice.append("Your BMI is low. Increase nutrition and strength training.")

    # Body fat
    if bodyfat > 20:
        advice.append("Body fat is above optimal. Add cardio and improve diet.")
    else:
        advice.append("Body fat is in a healthy range.")

    # Muscle
    if muscle < 30:
        advice.append("Muscle mass is low. Add resistance training.")

    # Hydration
    if water < 50:
        advice.append("Hydration is low. Increase water intake.")

    # Visceral fat
    if visceral > 10:
        advice.append("Visceral fat is high. Reduce sugar and improve sleep.")

    if not advice:
        advice.append("Your body composition is well balanced. Keep it up!")

    return advice