TREATMENT_KNOWLEDGE = {

    # =========================
    # 🌾 RICE
    # =========================
    "Rice": {
        "diseases": {
            "Blast": {
                "type": "disease",
                "chemical": [
                    {
                        "name": "Tricyclazole 75% WP",
                        "dosage_min": 0.5,
                        "dosage_max": 0.6,
                        "unit": "g/L",
                        "interval_days": 7
                    }
                ],
                "organic": [
                    {
                        "name": "Pseudomonas fluorescens",
                        "dosage_min": 5,
                        "dosage_max": 10,
                        "unit": "g/L",
                        "interval_days": 10
                    }
                ],
                "cultural": [
                    "Avoid excess nitrogen application",
                    "Maintain proper plant spacing",
                    "Use resistant varieties"
                ],
                "expected_recovery_days": 12
            }
        },
        "pests": {
            "Stem Borer": {
                "type": "pest",
                "chemical": [
                    {
                        "name": "Chlorantraniliprole 18.5% SC",
                        "dosage_min": 0.3,
                        "dosage_max": 0.4,
                        "unit": "ml/L",
                        "interval_days": 10
                    }
                ],
                "organic": [
                    {
                        "name": "Neem Oil 0.3%",
                        "dosage_min": 3,
                        "dosage_max": 5,
                        "unit": "ml/L",
                        "interval_days": 7
                    }
                ],
                "cultural": [
                    "Remove and destroy dead hearts",
                    "Install pheromone traps",
                    "Maintain field sanitation"
                ],
                "expected_recovery_days": 10
            }
        }
    },

    # =========================
    # 🌾 WHEAT
    # =========================
    "Wheat": {
        "diseases": {
            "Rust": {
                "type": "disease",
                "chemical": [
                    {
                        "name": "Propiconazole 25% EC",
                        "dosage_min": 0.5,
                        "dosage_max": 1.0,
                        "unit": "ml/L",
                        "interval_days": 10
                    }
                ],
                "organic": [
                    {
                        "name": "Bacillus subtilis",
                        "dosage_min": 5,
                        "dosage_max": 8,
                        "unit": "g/L",
                        "interval_days": 10
                    }
                ],
                "cultural": [
                    "Use resistant varieties",
                    "Avoid dense planting",
                    "Remove infected crop residues"
                ],
                "expected_recovery_days": 14
            }
        },
        "pests": {
            "Aphids": {
                "type": "pest",
                "chemical": [
                    {
                        "name": "Imidacloprid 17.8% SL",
                        "dosage_min": 0.3,
                        "dosage_max": 0.5,
                        "unit": "ml/L",
                        "interval_days": 7
                    }
                ],
                "organic": [
                    {
                        "name": "Neem Extract",
                        "dosage_min": 3,
                        "dosage_max": 5,
                        "unit": "ml/L",
                        "interval_days": 7
                    }
                ],
                "cultural": [
                    "Encourage natural predators",
                    "Avoid excess nitrogen fertilization"
                ],
                "expected_recovery_days": 7
            }
        }
    },

    # =========================
    # 🍅 TOMATO
    # =========================
    "Tomato": {
        "diseases": {
            "Late Blight": {
                "type": "disease",
                "chemical": [
                    {
                        "name": "Mancozeb 75% WP",
                        "dosage_min": 2.0,
                        "dosage_max": 3.0,
                        "unit": "g/L",
                        "interval_days": 7
                    }
                ],
                "organic": [
                    {
                        "name": "Neem Oil",
                        "dosage_min": 3,
                        "dosage_max": 5,
                        "unit": "ml/L",
                        "interval_days": 7
                    }
                ],
                "cultural": [
                    "Remove infected leaves",
                    "Avoid overhead irrigation",
                    "Improve air circulation"
                ],
                "expected_recovery_days": 12
            }
        },
        "pests": {
            "Whitefly": {
                "type": "pest",
                "chemical": [
                    {
                        "name": "Thiamethoxam 25% WG",
                        "dosage_min": 0.25,
                        "dosage_max": 0.4,
                        "unit": "g/L",
                        "interval_days": 7
                    }
                ],
                "organic": [
                    {
                        "name": "Neem Oil Spray",
                        "dosage_min": 3,
                        "dosage_max": 5,
                        "unit": "ml/L",
                        "interval_days": 5
                    }
                ],
                "cultural": [
                    "Use yellow sticky traps",
                    "Remove heavily infested leaves"
                ],
                "expected_recovery_days": 8
            }
        }
    },

    # =========================
    # 🥔 POTATO
    # =========================
    "Potato": {
        "diseases": {
            "Early Blight": {
                "type": "disease",
                "chemical": [
                    {
                        "name": "Chlorothalonil 75% WP",
                        "dosage_min": 2.0,
                        "dosage_max": 2.5,
                        "unit": "g/L",
                        "interval_days": 7
                    }
                ],
                "organic": [
                    {
                        "name": "Copper Oxychloride",
                        "dosage_min": 2,
                        "dosage_max": 3,
                        "unit": "g/L",
                        "interval_days": 10
                    }
                ],
                "cultural": [
                    "Remove infected foliage",
                    "Maintain crop rotation"
                ],
                "expected_recovery_days": 14
            }
        },
        "pests": {
            "Cutworm": {
                "type": "pest",
                "chemical": [
                    {
                        "name": "Lambda Cyhalothrin 5% EC",
                        "dosage_min": 0.5,
                        "dosage_max": 1.0,
                        "unit": "ml/L",
                        "interval_days": 7
                    }
                ],
                "organic": [
                    {
                        "name": "Neem Cake",
                        "dosage_min": 250,
                        "dosage_max": 500,
                        "unit": "kg/acre",
                        "interval_days": 30
                    }
                ],
                "cultural": [
                    "Deep ploughing before planting",
                    "Manual removal of larvae"
                ],
                "expected_recovery_days": 10
            }
        }
    },

        # =========================
    # 🌽 MAIZE
    # =========================
    "Maize": {
        "diseases": {
            "Leaf Blight": {
                "type": "disease",
                "chemical": [
                    {
                        "name": "Mancozeb 75% WP",
                        "dosage_min": 2.0,
                        "dosage_max": 2.5,
                        "unit": "g/L",
                        "interval_days": 7
                    }
                ],
                "organic": [
                    {
                        "name": "Trichoderma viride",
                        "dosage_min": 5,
                        "dosage_max": 10,
                        "unit": "g/L",
                        "interval_days": 10
                    }
                ],
                "cultural": [
                    "Use disease-free seeds",
                    "Avoid continuous maize cropping",
                    "Maintain field sanitation"
                ],
                "expected_recovery_days": 12
            }
        },
        "pests": {
            "Fall Armyworm": {
                "type": "pest",
                "chemical": [
                    {
                        "name": "Emamectin Benzoate 5% SG",
                        "dosage_min": 0.3,
                        "dosage_max": 0.5,
                        "unit": "g/L",
                        "interval_days": 5
                    }
                ],
                "organic": [
                    {
                        "name": "Neem Oil 0.3%",
                        "dosage_min": 3,
                        "dosage_max": 5,
                        "unit": "ml/L",
                        "interval_days": 5
                    }
                ],
                "cultural": [
                    "Install pheromone traps",
                    "Destroy egg masses manually",
                    "Encourage natural predators"
                ],
                "expected_recovery_days": 10
            }
        }
    },

    # =========================
    # 🌱 COTTON
    # =========================
    "Cotton": {
        "diseases": {
            "Leaf Curl Virus": {
                "type": "disease",
                "chemical": [],
                "organic": [],
                "cultural": [
                    "Remove infected plants immediately",
                    "Control whitefly population",
                    "Use resistant varieties"
                ],
                "expected_recovery_days": 15
            }
        },
        "pests": {
            "Bollworm": {
                "type": "pest",
                "chemical": [
                    {
                        "name": "Spinosad 45% SC",
                        "dosage_min": 0.3,
                        "dosage_max": 0.5,
                        "unit": "ml/L",
                        "interval_days": 7
                    }
                ],
                "organic": [
                    {
                        "name": "Neem Seed Kernel Extract",
                        "dosage_min": 3,
                        "dosage_max": 5,
                        "unit": "ml/L",
                        "interval_days": 5
                    }
                ],
                "cultural": [
                    "Install pheromone traps",
                    "Remove damaged bolls",
                    "Deep ploughing after harvest"
                ],
                "expected_recovery_days": 12
            }
        }
    },

    # =========================
    # 🥜 GROUNDNUT
    # =========================
    "Groundnut": {
        "diseases": {
            "Leaf Spot": {
                "type": "disease",
                "chemical": [
                    {
                        "name": "Chlorothalonil 75% WP",
                        "dosage_min": 2.0,
                        "dosage_max": 2.5,
                        "unit": "g/L",
                        "interval_days": 10
                    }
                ],
                "organic": [
                    {
                        "name": "Copper Oxychloride",
                        "dosage_min": 2,
                        "dosage_max": 3,
                        "unit": "g/L",
                        "interval_days": 10
                    }
                ],
                "cultural": [
                    "Avoid overhead irrigation",
                    "Practice crop rotation"
                ],
                "expected_recovery_days": 14
            }
        },
        "pests": {
            "Aphids": {
                "type": "pest",
                "chemical": [
                    {
                        "name": "Imidacloprid 17.8% SL",
                        "dosage_min": 0.3,
                        "dosage_max": 0.5,
                        "unit": "ml/L",
                        "interval_days": 7
                    }
                ],
                "organic": [
                    {
                        "name": "Neem Oil",
                        "dosage_min": 3,
                        "dosage_max": 5,
                        "unit": "ml/L",
                        "interval_days": 7
                    }
                ],
                "cultural": [
                    "Encourage ladybird beetles",
                    "Avoid excessive nitrogen fertilization"
                ],
                "expected_recovery_days": 7
            }
        }
    },

    # =========================
    # 🌿 CHILLI
    # =========================
    "Chilli": {
        "diseases": {
            "Anthracnose": {
                "type": "disease",
                "chemical": [
                    {
                        "name": "Carbendazim 50% WP",
                        "dosage_min": 1.0,
                        "dosage_max": 1.5,
                        "unit": "g/L",
                        "interval_days": 10
                    }
                ],
                "organic": [
                    {
                        "name": "Trichoderma viride",
                        "dosage_min": 5,
                        "dosage_max": 10,
                        "unit": "g/L",
                        "interval_days": 10
                    }
                ],
                "cultural": [
                    "Remove infected fruits",
                    "Ensure proper drainage"
                ],
                "expected_recovery_days": 12
            }
        },
        "pests": {
            "Thrips": {
                "type": "pest",
                "chemical": [
                    {
                        "name": "Fipronil 5% SC",
                        "dosage_min": 1.0,
                        "dosage_max": 1.5,
                        "unit": "ml/L",
                        "interval_days": 7
                    }
                ],
                "organic": [
                    {
                        "name": "Neem Oil",
                        "dosage_min": 3,
                        "dosage_max": 5,
                        "unit": "ml/L",
                        "interval_days": 5
                    }
                ],
                "cultural": [
                    "Use blue sticky traps",
                    "Maintain field hygiene"
                ],
                "expected_recovery_days": 8
            }
        }
    },

    # =========================
    # 🧅 ONION
    # =========================
    "Onion": {
        "diseases": {
            "Downy Mildew": {
                "type": "disease",
                "chemical": [
                    {
                        "name": "Metalaxyl + Mancozeb",
                        "dosage_min": 2.0,
                        "dosage_max": 2.5,
                        "unit": "g/L",
                        "interval_days": 7
                    }
                ],
                "organic": [
                    {
                        "name": "Copper Oxychloride",
                        "dosage_min": 2,
                        "dosage_max": 3,
                        "unit": "g/L",
                        "interval_days": 10
                    }
                ],
                "cultural": [
                    "Avoid water stagnation",
                    "Ensure adequate spacing"
                ],
                "expected_recovery_days": 12
            }
        },
        "pests": {
            "Onion Thrips": {
                "type": "pest",
                "chemical": [
                    {
                        "name": "Spinosad 45% SC",
                        "dosage_min": 0.3,
                        "dosage_max": 0.5,
                        "unit": "ml/L",
                        "interval_days": 7
                    }
                ],
                "organic": [
                    {
                        "name": "Neem Oil",
                        "dosage_min": 3,
                        "dosage_max": 5,
                        "unit": "ml/L",
                        "interval_days": 5
                    }
                ],
                "cultural": [
                    "Remove heavily infested leaves",
                    "Install sticky traps"
                ],
                "expected_recovery_days": 8
            }
        }
    }
}


    

