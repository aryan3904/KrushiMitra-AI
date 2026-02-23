# ==========================================
# 🧠 Manual Symptom Risk Engine
# ==========================================

# Base confidence from severity selection
DISEASE_BASE_CONFIDENCE = {
    "Mild": 0.60,
    "Moderate": 0.80,
    "Severe": 0.95
}

# Pest infestation base mapping (numeric style)
PEST_BASE_CONFIDENCE = {
    "1-2": 0.65,
    "3-5": 0.80,
    "5+": 0.95,
    "Not Sure": 0.75
}


# ==========================================
# 🔢 Helper: Yes/No/Not Sure Weight
# ==========================================
def apply_factor(answer, weight):
    """
    Yes → full weight
    No → 0
    Not Sure → half weight
    """
    if answer == "Yes":
        return weight
    elif answer == "Not Sure":
        return weight / 2
    else:
        return 0


# ==========================================
# 🌿 DISEASE CONFIDENCE CALCULATION
# ==========================================
def calculate_disease_confidence(severity, humidity, spread):
    """
    severity: Mild/Moderate/Severe
    humidity: Yes/No/Not Sure
    spread: Yes/No/Not Sure
    """

    base = DISEASE_BASE_CONFIDENCE.get(severity, 0.70)

    # Disease escalation factors
    humidity_weight = 0.05
    spread_weight = 0.07

    adjustment = (
        apply_factor(humidity, humidity_weight) +
        apply_factor(spread, spread_weight)
    )

    final_confidence = base + adjustment

    # Cap safely
    return min(final_confidence, 0.98)


# ==========================================
# 🐛 PEST CONFIDENCE CALCULATION
# ==========================================
def calculate_pest_confidence(insects_per_plant, damage_percent, rapid_increase):
    """
    insects_per_plant: "1-2" / "3-5" / "5+" / "Not Sure"
    damage_percent: "<10" / "10-30" / "30+" / "Not Sure"
    rapid_increase: Yes/No/Not Sure
    """

    base = PEST_BASE_CONFIDENCE.get(insects_per_plant, 0.75)

    # Damage mapping
    damage_weight_map = {
        "<10": 0.03,
        "10-30": 0.07,
        "30+": 0.12,
        "Not Sure": 0.05
    }

    damage_weight = damage_weight_map.get(damage_percent, 0.05)

    # Rapid increase weight
    spread_weight = 0.08

    adjustment = (
        damage_weight +
        apply_factor(rapid_increase, spread_weight)
    )

    final_confidence = base + adjustment

    return min(final_confidence, 0.98)
