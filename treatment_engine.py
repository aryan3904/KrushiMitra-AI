from treatment_knowledge import TREATMENT_KNOWLEDGE


# ==========================================
# 🔢 Helper: Map Confidence → Severity
# ==========================================
def get_severity(confidence):
    if confidence < 0.70:
        return "Mild"
    elif confidence < 0.90:
        return "Moderate"
    else:
        return "Severe"


# ==========================================
# 🔢 Helper: Interpolate Dosage
# ==========================================
def interpolate_dosage(min_val, max_val, confidence):
    """
    Linearly interpolate dosage between min and max
    based on confidence.
    """
    confidence = min(max(confidence, 0.0), 1.0)
    return round(min_val + (max_val - min_val) * confidence, 2)


# ==========================================
# 🔢 Helper: Adjust Interval Based on Severity
# ==========================================
def adjust_interval(base_interval, severity):
    if severity == "Mild":
        return base_interval
    elif severity == "Moderate":
        return max(base_interval - 2, 5)
    else:  # Severe
        return max(base_interval - 3, 4)


# ==========================================
# 🧠 MAIN ENGINE
# ==========================================
def generate_treatment_plan(crop, problem_name, confidence):
    """
    crop: string
    problem_name: disease or pest name
    confidence: float (0.0 – 1.0)
    """

    if crop not in TREATMENT_KNOWLEDGE:
        return None

    crop_data = TREATMENT_KNOWLEDGE[crop]

    # Determine if disease or pest
    if "diseases" in crop_data and problem_name in crop_data["diseases"]:
        problem_data = crop_data["diseases"][problem_name]
    elif "pests" in crop_data and problem_name in crop_data["pests"]:
        problem_data = crop_data["pests"][problem_name]
    else:
        return None

    severity = get_severity(confidence)

    result = {
        "severity": severity,
        "chemical": [],
        "organic": [],
        "cultural": problem_data.get("cultural", []),
        "expected_recovery_days": problem_data.get("expected_recovery_days", 10),
        "recovery_phases": {}
    }

    # ===============================
    # 💊 Chemical Treatment
    # ===============================
    for chem in problem_data.get("chemical", []):
        if chem.get("dosage_min") is not None:
            dosage = interpolate_dosage(
                chem["dosage_min"],
                chem["dosage_max"],
                confidence
            )
        else:
            dosage = None

        interval = adjust_interval(
            chem.get("interval_days", 7),
            severity
        )

        result["chemical"].append({
            "name": chem["name"],
            "dosage": f"{dosage} {chem['unit']}" if dosage else "As per label",
            "interval": f"Every {interval} days"
        })

    # ===============================
    # 🌿 Organic Treatment
    # ===============================
    for org in problem_data.get("organic", []):
        if org.get("dosage_min") is not None:
            dosage = interpolate_dosage(
                org["dosage_min"],
                org["dosage_max"],
                confidence
            )
        else:
            dosage = None

        interval = adjust_interval(
            org.get("interval_days", 7),
            severity
        )

        result["organic"].append({
            "name": org["name"],
            "dosage": f"{dosage} {org['unit']}" if dosage else "As per label",
            "interval": f"Every {interval} days"
        })

    # ===============================
    # 🗺 Recovery Phases
    # ===============================
    result["recovery_phases"] = {
        "phase_1": [
            "Apply first spray immediately.",
            "Remove heavily affected plant parts."
        ],
        "phase_2": [
            "Repeat treatment as per interval.",
            "Monitor spread daily."
        ],
        "phase_3": [
            "Continue preventive care.",
            "Maintain proper field hygiene."
        ]
    }

    return result
