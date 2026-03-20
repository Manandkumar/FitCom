# -------------------------------------------------------
# FitCom - Fitness Analysis Engine (FINAL)
# -------------------------------------------------------

def analyze(bodyfat):
    """
    Analyze body fat and return health insight.
    Supports both float (DB) and string inputs.
    """

    try:
        # ---------------------------------------------------
        # Normalize Input (handle DB + old string formats)
        # ---------------------------------------------------
        if isinstance(bodyfat, str):
            value = float(bodyfat.split()[0])
        else:
            value = float(bodyfat)

        # ---------------------------------------------------
        # Analysis Logic
        # ---------------------------------------------------
        if value >= 30:
            return "🚨 FitCom Insight: Body fat is very high. Immediate lifestyle and diet changes recommended."

        elif value > 25:
            return "⚠️ FitCom Insight: Body fat is high. Focus on fat loss and calorie deficit."

        elif value > 20:
            return "⚠️ FitCom Insight: Body fat slightly above optimal range. Improve diet and activity."

        elif value >= 12:
            return "✅ FitCom Insight: Body fat is in a healthy range. Maintain consistency."

        else:
            return "🔥 FitCom Insight: Very lean body composition. Ensure proper nutrition and recovery."

    except Exception:
        return "⚠️ FitCom could not analyze body fat value."