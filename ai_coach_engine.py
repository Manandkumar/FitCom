# ============================================================
# FitCom - AI Health Coach Engine
# Author: Anand Kumar
#
# Description:
# Generates health insights based on body composition
# metrics entered in FitCom.
#
# The logic is rule-based and designed to mimic a
# lightweight AI health advisor.
# ============================================================


# ------------------------------------------------------------
# Generate Advice
# ------------------------------------------------------------
# Produces personalized recommendations.
#
# Returns
# -------
# list[str]
# ------------------------------------------------------------

def generate_advice(row):

    advice = []

    if row["BMI"] > 25:
        advice.append("Your BMI is above the optimal range. Consider gradual fat reduction.")

    elif row["BMI"] < 18.5:
        advice.append("BMI indicates underweight. Focus on muscle gain and nutrition.")

    if row["BodyFat"] > 20:
        advice.append("Body fat percentage slightly high. Add cardio workouts.")

    if row["MuscleMass"] > 45:
        advice.append("Excellent muscle mass for your height.")

    if row["VisceralFat"] > 10:
        advice.append("Visceral fat elevated. Reduce processed foods and increase activity.")

    if row["BodyWater"] < 50:
        advice.append("Body hydration appears low. Increase daily water intake.")

    if not advice:
        advice.append("Your body composition is within a healthy range. Keep maintaining your routine.")

    return advice