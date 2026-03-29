# ============================================================
# FitCom - Utility Functions (Final Clean Version)
# ============================================================


# ------------------------------------------------------------
# BMI Calculation
# ------------------------------------------------------------
def calculate_bmi(weight, height_in):
    if height_in == 0:
        return 0

    height_m = height_in * 0.0254
    bmi = weight / (height_m ** 2)

    return round(bmi, 2)


# ------------------------------------------------------------
# HEALTH SCORE (Single Source of Truth)
# ------------------------------------------------------------
def calculate_health_score(data):
    """
    Calculates health score (0–100) and status
    """

    score = 0

    # BMI
    bmi = data.get("BMI", 0)
    if 18.5 <= bmi <= 24.9:
        score += 20
    elif 25 <= bmi <= 29.9:
        score += 10

    # Body Fat
    bf = data.get("BodyFat", 0)
    if 10 <= bf <= 20:
        score += 20
    elif 20 < bf <= 25:
        score += 10

    # Muscle Mass
    if data.get("MuscleMass", 0) >= 40:
        score += 15

    # Visceral Fat
    if data.get("VisceralFat", 0) < 10:
        score += 15

    # BMR
    if data.get("BMR", 0) >= 1200:
        score += 10

    # Weight Range
    if 50 <= data.get("Weight", 0) <= 90:
        score += 10

    score = min(score, 100)

    # Status
    if score >= 75:
        status = "🔥 Excellent"
    elif score >= 50:
        status = "👍 Good"
    else:
        status = "⚠️ Needs Improvement"

    return score, status