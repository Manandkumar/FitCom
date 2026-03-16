# ============================================================
# Syntra AI Health Coach Engine
# Author: Anand Kumar
# ============================================================

def generate_ai_advice(row):

    advice = []

    bmi = row["BMI"]
    bodyfat = row["BodyFat"]
    muscle = row["MuscleMass"]
    water = row["BodyWater"]
    visceral = row["VisceralFat"]

    # BMI analysis
    if bmi > 25:
        advice.append("Your BMI is slightly high. Focus on fat reduction through cardio and calorie balance.")
    elif bmi < 18:
        advice.append("Your BMI is low. Consider increasing protein intake and resistance training.")

    # Body fat analysis
    if bodyfat > 20:
        advice.append("Body fat is above optimal. Increase daily activity and monitor nutrition quality.")
    else:
        advice.append("Body fat is within a healthy range. Maintain current training consistency.")

    # Muscle analysis
    if muscle < 30:
        advice.append("Muscle mass is lower than ideal. Strength training 3–4 times per week is recommended.")

    # Hydration
    if water < 50:
        advice.append("Body water percentage indicates possible dehydration. Increase daily water intake.")

    # Visceral fat
    if visceral > 10:
        advice.append("Visceral fat is elevated. Prioritize sleep, reduce sugar intake, and maintain regular workouts.")

    if not advice:
        advice.append("Your body composition is balanced. Continue maintaining your current routine.")

    return advice