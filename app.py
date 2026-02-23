from flask import Flask, render_template, request, session, g, url_for , redirect
import joblib
import tensorflow as tf
import numpy as np
from tensorflow.keras.utils import load_img, img_to_array
import os
import pandas as pd
from treatment_engine import generate_treatment_plan
from treatment_knowledge import TREATMENT_KNOWLEDGE
from manual_symptoms import (
    calculate_disease_confidence,
    calculate_pest_confidence
)


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-change-me")


SUPPORTED_LANGS = ["en", "hi", "mr", "gu"]
LANG_LABELS = {"en": "English", "hi": "हिंदी", "mr": "मराठी", "gu": "ગુજરાતી"}

I18N = {
   
    "app_title": {"en": "Krushi Mitra AI", "hi": "कृषि मित्र AI", "mr": "कृषी मित्र AI", "gu": "કૃષિ મિત્ર AI"},
    "namaste": {"en": "Namaste!", "hi": "नमस्ते!", "mr": "नमस्कार!", "gu": "નમસ્તે!"},
    "home_intro": {"en": "I am Krushi Mitra.", "hi": "मैं कृषि मित्र हूँ।", "mr": "मी कृषी मित्र आहे.", "gu": "હું કૃષિ મિત્ર છું."},
    "home_q": {"en": "How can I help you today?", "hi": "आज मैं आपकी कैसे मदद कर सकता हूँ?", "mr": "आज मी तुम्हाला कशी मदत करू?", "gu": "આજે હું તમારી કેવી મદદ કરી શકું?"},
    "back_home": {"en": "Back to Home", "hi": "होम पर जाएँ", "mr": "होमला जा", "gu": "હોમ પર જાઓ"},
    "start_again": {"en": "Start Again", "hi": "फिर से शुरू करें", "mr": "पुन्हा सुरू करा", "gu": "ફરીથી શરૂ કરો"},

 
    "opt_crop": {"en": "Crop Selection & Planning", "hi": "फसल चयन और योजना", "mr": "पीक निवड आणि नियोजन", "gu": "પાક પસંદગી અને યોજના"},
    "opt_disease": {"en": "Detect Crop Disease", "hi": "फसल रोग पहचान", "mr": "पीक रोग ओळखा", "gu": "પાક રોગ શોધો"},
        "opt_fertilizer": {
        "en": "Fertilizer Suggestion",
        "hi": "खाद सलाह",
        "mr": "खत सल्ला",
        "gu": "ખાતર સલાહ"
    },
    "opt_weather": {
        "en": "Treatment Recommendation",
        "hi": "मौसम जानकारी",
        "mr": "हवामान माहिती",
        "gu": "ઉપચાર ભલામણ"
    },
    "opt_market": {
        "en": "Market Price",
        "hi": "बाजार भाव",
        "mr": "बाजार भाव",
        "gu": "બજાર ભાવ"
    },
    "opt_schemes": {
        "en": "Government Schemes",
        "hi": "सरकारी योजनाएँ",
        "mr": "शासकीय योजना",
        "gu": "સરકારી યોજનાઓ"
    },


    # ----- CROP FLOW -----
    "crop_intro": {
        "en": "I will help you choose the right crop.",
        "hi": "मैं आपको सही फसल चुनने में मदद करूंगा।",
        "mr": "मी तुम्हाला योग्य पीक निवडण्यात मदत करेन.",
        "gu": "હું તમને સાચો પાક પસંદ કરવામાં મદદ કરીશ."
    },
    "select_season": {
        "en": "Please select your season.",
        "hi": "कृपया अपना मौसम चुनें।",
        "mr": "कृपया हंगाम निवडा.",
        "gu": "કૃપા કરીને તમારો હંગામ પસંદ કરો."
    },
    "you_selected": {"en": "You selected", "hi": "आपने चुना", "mr": "तुम्ही निवडलं", "gu": "તમે પસંદ કર્યું"},
    "select_soil": {
        "en": "Please select your soil type.",
        "hi": "कृपया अपनी मिट्टी का प्रकार चुनें।",
        "mr": "कृपया मातीचा प्रकार निवडा.",
        "gu": "કૃપા કરીને તમારો માટીનો પ્રકાર પસંદ કરો."
    },
    "select_water": {
        "en": "Please select water availability.",
        "hi": "कृपया पानी की उपलब्धता चुनें।",
        "mr": "कृपया पाण्याची उपलब्धता निवडा.",
        "gu": "કૃપા કરીને પાણીની ઉપલબ્ધતા પસંદ કરો."
    },
    "based_on": {
        "en": "Based on your land conditions, the best crops for you are:",
        "hi": "आपकी जमीन की स्थिति के आधार पर, आपके लिए सबसे अच्छी फसलें:",
        "mr": "तुमच्या जमिनीच्या स्थितीनुसार, तुमच्यासाठी उत्तम पिके:",
        "gu": "તમારી જમીનની સ્થિતિના આધારે, તમારા માટે શ્રેષ્ઠ પાકો છે:"
    },

    # ----- LABELS -----
    "season": {"en": "Season", "hi": "मौसम", "mr": "हंगाम", "gu": "હંગામ"},
    "soil": {"en": "Soil", "hi": "मिट्टी", "mr": "माती", "gu": "માટી"},
    "water": {"en": "Water", "hi": "पानी", "mr": "पाणी", "gu": "પાણી"},

    # ----- DISEASE -----
    "upload_leaf": {
        "en": "Upload a tomato leaf image to detect disease.",
        "hi": "रोग पहचानने के लिए टमाटर के पत्ते की फोटो अपलोड करें।",
        "mr": "रोग ओळखण्यासाठी टोमॅटो पानाचा फोटो अपलोड करा.",
        "gu": "રોગ શોધવા માટે ટોમેટો પાનનો ફોટો અપલોડ કરો."
    },
    "detect": {"en": "Detect Disease", "hi": "रोग पहचानें", "mr": "रोग ओळखा", "gu": "રોગ શોધો"},
    "predicted_disease": {"en": "Predicted Disease", "hi": "अनुमानित रोग", "mr": "अंदाजित रोग", "gu": "અંદાજિત રોગ"},
    "what_means": {"en": "What this means", "hi": "इसका अर्थ", "mr": "याचा अर्थ", "gu": "આનો અર્થ શું છે"},
    "suggested_action": {"en": "Suggested Action", "hi": "सुझाव", "mr": "सुचवलेली कृती", "gu": "સૂચવેલ ક્રિયા"},

    # ----- OPTION DESCRIPTIONS -----
    "opt_crop_desc": {"en": "Plan your crops based on season, soil & water", "hi": "मौसम, मिट्टी और पानी के आधार पर अपनी फसल की योजना बनाएं", "mr": "हंगाम, माती आणि पाण्यावर आधारित आपल्या पिकांची योजना करा", "gu": "હંગામ, માટી અને પાણીના આધારે તમારા પાકની યોજના બનાવો"},
    "opt_disease_desc": {"en": "AI-powered plant disease detection", "hi": "AI-संचालित पौध रोग पहचान", "mr": "AI-चालित वनस्पती रोग शोध", "gu": "AI-ચાલિત છોડ રોગ શોધ"},
    "coming_soon": {"en": "Coming soon", "hi": "जल्द आ रहा है", "mr": "लवकरच येत आहे", "gu": "જલ્દી આવી રહ્યું છે"},

    # ----- DISEASE MESSAGES -----
    "great_news": {"en": "Great news!", "hi": "बड़ी खबर!", "mr": "छान बातमी!", "gu": "સરસ સમાચાર!"},
    "healthy_msg": {"en": "Your tomato plant appears healthy. Continue with proper care and monitoring.", "hi": "आपका टमाटर पौधा स्वस्थ दिख रहा है। उचित देखभाल और निगरानी जारी रखें।", "mr": "तुमचा टोमॅटो वनस्पती निरोगी दिसत आहे. योग्य काळजी आणि निरीक्षण सुरू ठेवा.", "gu": "તમારો ટોમેટો છોડ સ્વસ્થ દેખાય છે. યોગ્ય સંભાળ અને નિરીક્ષણ ચાલુ રાખો."},
    "action_required": {"en": "Action Required", "hi": "कार्रवाई आवश्यक", "mr": "कृती आवश्यक", "gu": "ક્રિયા જરૂરી"},
    "disease_detected": {"en": "Disease detected. Please follow the recommended treatment below.", "hi": "रोग का पता चला। कृपया नीचे दी गई अनुशंसित उपचार का पालन करें।", "mr": "रोग आढळला. कृपया खालील शिफारस केलेली उपचार पद्धत पाळा.", "gu": "રોગ શોધાયો. કૃપા કરીને નીચે આપેલ સૂચવેલ સારવાર અનુસરો."},
    "check_another": {"en": "Check Another Leaf", "hi": "एक और पत्ता जांचें", "mr": "दुसरे पान तपासा", "gu": "બીજું પાન તપાસો"},
    "upload_different": {"en": "Upload a different image", "hi": "एक अलग फोटो अपलोड करें", "mr": "वेगळा फोटो अपलोड करा", "gu": "અલગ ફોટો અપલોડ કરો"},
    "return_main": {"en": "Return to main menu", "hi": "मुख्य मेनू पर वापस जाएं", "mr": "मुख्य मेनूवर परत जा", "gu": "મુખ્ય મેનૂ પર પાછા જાઓ"},
    "powered_by": {"en": "Powered by AI • Supports Tomato Disease Detection", "hi": "AI द्वारा संचालित • टमाटर रोग पहचान का समर्थन करता है", "mr": "AI द्वारे चालवलेले • टोमॅटो रोग शोधास समर्थन देते", "gu": "AI દ્વારા ચાલિત • ટોમેટો રોગ શોધને સમર્થન આપે છે"},

    # ----- SEASON OPTIONS -----
    "kharif_season": {"en": "Kharif Season", "hi": "खरीफ मौसम", "mr": "खरीप हंगाम", "gu": "ખરીફ હંગામ"},
    "kharif_desc": {"en": "June-October • Monsoon crops", "hi": "जून-अक्टूबर • मानसून फसलें", "mr": "जून-ऑक्टोबर • पावसाळी पिके", "gu": "જૂન-ઑક્ટોબર • પાવસાળી પાક"},
    "rabi_season": {"en": "Rabi Season", "hi": "रबी मौसम", "mr": "रबी हंगाम", "gu": "રબી હંગામ"},
    "rabi_desc": {"en": "October-March • Winter crops", "hi": "अक्टूबर-मार्च • सर्दी की फसलें", "mr": "ऑक्टोबर-मार्च • हिवाळी पिके", "gu": "ઑક્ટોબર-માર્ચ • શિયાળાના પાક"},
    "zaid_season": {"en": "Zaid Season", "hi": "जायद मौसम", "mr": "जायद हंगाम", "gu": "જાયદ હંગામ"},
    "zaid_desc": {"en": "March-June • Summer crops", "hi": "मार्च-जून • गर्मी की फसलें", "mr": "मार्च-जून • उन्हाळी पिके", "gu": "માર્ચ-જૂન • ઉનાળાના પાક"},

    # ----- SOIL TYPES -----
    "black_soil": {"en": "Black Soil", "hi": "काली मिट्टी", "mr": "काळी माती", "gu": "કાળી માટી"},
    "black_desc": {"en": "Clay-rich, high fertility", "hi": "मिट्टी से भरपूर, उच्च उर्वरता", "mr": "मातीने समृद्ध, उच्च सुपीकता", "gu": "માટીથી સમૃદ્ધ, ઉચ્ચ ઉર્વરતા"},
    "red_soil": {"en": "Red Soil", "hi": "लाल मिट्टी", "mr": "लाल माती", "gu": "લાલ માટી"},
    "red_desc": {"en": "Iron-rich, well-drained", "hi": "लोहा से भरपूर, अच्छी जल निकासी", "mr": "लोखंडाने समृद्ध, चांगली पाणी निचरा", "gu": "લોખંડથી સમૃદ્ધ, સારી પાણી નિકાસ"},
    "loamy_soil": {"en": "Loamy Soil", "hi": "दोमट मिट्टी", "mr": "दुमट माती", "gu": "દુમટ માટી"},
    "loamy_desc": {"en": "Balanced texture, fertile", "hi": "संतुलित बनावट, उर्वरक", "mr": "संतुलित रचना, सुपीक", "gu": "સંતુલિત બનાવટ, ઉર્વર"},
    "sandy_soil": {"en": "Sandy Soil", "hi": "रेतीली मिट्टी", "mr": "वाळू माती", "gu": "રેતાળ માટી"},
    "sandy_desc": {"en": "Well-drained, low fertility", "hi": "अच्छी जल निकासी, कम उर्वरता", "mr": "चांगली पाणी निचरा, कमी सुपीकता", "gu": "સારી પાણી નિકાસ, ઓછી ઉર્વરતા"},
    "clay_soil": {"en": "Clay Soil", "hi": "चिकनी मिट्टी", "mr": "चिकणमाती", "gu": "ચીકણી માટી"},
    "clay_desc": {"en": "Heavy, retains moisture", "hi": "भारी, नमी बनाए रखती है", "mr": "जड, ओल धरून ठेवते", "gu": "ભારે, ભેજ રાખે છે"},

    # ----- WATER AVAILABILITY -----
    "low_water": {"en": "Low Water", "hi": "कम पानी", "mr": "कमी पाणी", "gu": "ઓછું પાણી"},
    "low_desc": {"en": "Rainfed or minimal irrigation", "hi": "बारिश पर निर्भर या न्यूनतम सिंचाई", "mr": "पावसावर अवलंबून किंवा किमान पाणी देता", "gu": "વરસાદ પર આધારિત અથવા ન્યૂનતમ સિંચાઈ"},
    "medium_water": {"en": "Medium Water", "hi": "मध्यम पानी", "mr": "मध्यम पाणी", "gu": "મધ્યમ પાણી"},
    "medium_desc": {"en": "Moderate irrigation available", "hi": "मध्यम सिंचाई उपलब्ध", "mr": "मध्यम पाणी देता उपलब्ध", "gu": "મધ્યમ સિંચાઈ ઉપલબ્ધ"},
    "high_water": {"en": "High Water", "hi": "अधिक पानी", "mr": "जास्त पाणी", "gu": "વધુ પાણી"},
    "high_desc": {"en": "Abundant irrigation access", "hi": "प्रचुर सिंचाई पहुंच", "mr": "प्रचंड पाणी देता प्रवेश", "gu": "પ્રચુર સિંચાઈ પહોંચ"},

    # ----- CROP PLANNING -----
    "view_plan": {"en": "View Plan", "hi": "योजना देखें", "mr": "योजना पहा", "gu": "યોજના જુઓ"},
    "complete_guide": {"en": "Complete farming guide", "hi": "पूर्ण कृषि मार्गदर्शिका", "mr": "पूर्ण शेती मार्गदर्शिका", "gu": "સંપૂર્ણ ખેતી માર્ગદર્શિકા"},
    "choose_different": {"en": "Choose different parameters", "hi": "अलग पैरामीटर चुनें", "mr": "वेगळे पॅरामीटर्स निवडा", "gu": "અલગ પરિમાણો પસંદ કરો"},

    # ----- CROP PLAN HEADINGS -----
    "farming_guide": {"en": "Farming Guide", "hi": "कृषि मार्गदर्शिका", "mr": "शेती मार्गदर्शिका", "gu": "ખેતી માર્ગદર્શિકા"},
    "complete_guide_desc": {"en": "Complete farming guide for successful cultivation", "hi": "सफल खेती के लिए पूर्ण कृषि मार्गदर्शिका", "mr": "यशस्वी शेतीसाठी संपूर्ण शेती मार्गदर्शिका", "gu": "સફળ ખેતી માટે સંપૂર્ણ ખેતી માર્ગદર્શિકા"},
    "sowing_season": {"en": "Sowing Season", "hi": "बुआई मौसम", "mr": "पेरणी हंगाम", "gu": "વાવણી હંગામ"},
    "seed_selection": {"en": "Seed Selection", "hi": "बीज चयन", "mr": "बियाणे निवड", "gu": "બીજ પસંદગી"},
    "land_prep": {"en": "Land Preparation", "hi": "जमीन की तैयारी", "mr": "जमिन तयारी", "gu": "જમીન તૈયારી"},
    "fertilizer_plan": {"en": "Fertilizer Plan", "hi": "खाद योजना", "mr": "खत योजना", "gu": "ખાતર યોજના"},
    "irrigation_guide": {"en": "Irrigation Guide", "hi": "सिंचाई मार्गदर्शिका", "mr": "पाणी मार्गदर्शिका", "gu": "સિંચાઈ માર્ગદર્શિકા"},
    "common_diseases": {"en": "Common Diseases", "hi": "सामान्य रोग", "mr": "सामान्य रोग", "gu": "સામાન્ય રોગ"},
    "harvest_time": {"en": "Harvest Time", "hi": "कटाई समय", "mr": "कापणी वेळ", "gu": "કાપણી સમય"},
    "plan_another": {"en": "Plan Another Crop", "hi": "एक और फसल की योजना बनाएं", "mr": "दुसरे पीक योजना करा", "gu": "બીજો પાક યોજના બનાવો"},
    "coming_soon_title": {"en": "Coming Soon", "hi": "जल्द आ रहा है", "mr": "लवकरच येत आहे", "gu": "જલ્દી આવી રહ્યું છે"},
    "detailed_guide": {"en": "Detailed farming guide for", "hi": "के लिए विस्तृत कृषि मार्गदर्शिका", "mr": "साठी तपशीलवार शेती मार्गदर्शिका", "gu": "માટે વિગતવાર ખેતી માર્ગદર્શિકા"},
    "being_prepared": {"en": "is being prepared.", "hi": "तैयार की जा रही है।", "mr": "तयार केली जात आहे.", "gu": "તૈયાર કરવામાં આવી રહી છે."},
    "footer_note": {"en": "Based on agricultural best practices • Consult local experts for specific conditions", "hi": "कृषि की सर्वोत्तम प्रथाओं पर आधारित • विशिष्ट स्थितियों के लिए स्थानीय विशेषज्ञों से सलाह लें", "mr": "कृषीच्या सर्वोत्तम पद्धतींवर आधारित • विशिष्ट परिस्थितीसाठी स्थानिक तज्ञांचा सल्ला घ्या", "gu": "કૃષિની શ્રેષ્ઠ પદ્ધતિઓ પર આધારિત • ચોક્કસ સ્થિતિઓ માટે સ્થાનિક નિષ્ણાતોની સલાહ લો"},
}

@app.before_request
def set_language():
    lang = request.args.get("lang") or session.get("lang") or "en"
    if lang not in SUPPORTED_LANGS:
        lang = "en"
    session["lang"] = lang
    g.lang = lang

def t(key):
    return I18N.get(key, {}).get(g.lang, I18N.get(key, {}).get("en", key))

def lang_url(lang):
    args = dict(request.args)
    args["lang"] = lang
    return url_for(request.endpoint or "home", **(request.view_args or {}), **args)

@app.context_processor
def inject_i18n():
    return dict(
        t=t,
        current_lang=g.lang,
        supported_langs=SUPPORTED_LANGS,
        lang_labels=LANG_LABELS,
        lang_url=lang_url
    )

# =============================
# 🌱 LOAD CROP DATA
# =============================
crop_df = pd.read_csv("crop_data.csv")

def get_crop_suggestions(season, soil, water):
    # Filter by season and soil first
    matching_crops = crop_df[(crop_df['Season'] == season) & (crop_df['Soil'] == soil)]
    
    # If no exact matches, fall back to season only
    if matching_crops.empty:
        matching_crops = crop_df[crop_df['Season'] == season]
    
    # If still no matches, return empty list
    if matching_crops.empty:
        return []
    
    # Create water priority mapping
    water_priority = {'High': 3, 'Medium': 2, 'Low': 1}
    matching_crops = matching_crops.copy()
    matching_crops['water_score'] = matching_crops['Water'].map(water_priority)
    user_water_score = water_priority.get(water, 1)
    
    # Calculate match score based on water availability
    matching_crops['match_score'] = abs(matching_crops['water_score'] - user_water_score)
    
    # Sort by match score (best matches first)
    matching_crops = matching_crops.sort_values('match_score')
    
    # Get unique crops, up to 3 suggestions
    suggested_crops = []
    seen_crops = set()
    
    for _, row in matching_crops.iterrows():
        crop = row['Crop']
        if crop not in seen_crops:
            suggested_crops.append(crop)
            seen_crops.add(crop)
            if len(suggested_crops) >= 3:
                break
    
    return suggested_crops

# =============================
# 🌱 LOAD CROP ML MODEL (keeping for compatibility)
# =============================
# crop_data = joblib.load("crop_model.pkl")
# crop_model = crop_data["model"]
# le_season = crop_data["le_season"]
# le_soil = crop_data["le_soil"]
# le_water = crop_data["le_water"]
# le_crop = crop_data["le_crop"]

# =============================
# 🌾 CROP PLANNING DATA
# =============================
CROP_PLANS = {
    "Millet": {
        "sowing": "June–July",
        "seed": "Improved millet varieties (certified seeds)",
        "land": "Light sandy or red soil, good drainage",
        "fertilizer": "Low input crop – FYM + small nitrogen dose",
        "irrigation": "Mostly rainfed, 1–2 irrigations if required",
        "diseases": "Downy mildew, rust",
        "harvest": "September–October",
        "steps": [
            "Prepare the land by plowing and harrowing to create a fine seedbed",
            "Apply FYM (Farm Yard Manure) 5-10 tons per hectare during land preparation",
            "Sow seeds directly in rows 30-45 cm apart at a depth of 2-3 cm",
            "Apply pre-emergence herbicide if weeds are a problem",
            "Thin seedlings to maintain proper plant spacing (15-20 cm within rows)",
            "Apply nitrogen fertilizer in split doses at 30 and 60 days after sowing",
            "Monitor for pests like grasshoppers and apply control measures if needed",
            "Harvest when grains are mature and panicles turn golden yellow"
        ],
        "youtube": "https://www.youtube.com/watch?v=example_millet"
    },

    "Rice": {
        "sowing": "June–July",
        "seed": "Certified paddy seeds, nursery required",
        "land": "Clay or loamy soil with water retention",
        "fertilizer": "Nitrogen in split doses, phosphorus basal",
        "irrigation": "Standing water 2–5 cm",
        "diseases": "Blast, leaf blight",
        "harvest": "October–November",
        "steps": [
            "Prepare nursery bed with fine tilth and sow pre-soaked seeds",
            "Maintain nursery with proper watering and protection from birds",
            "Prepare main field by puddling when seedlings are 25-30 days old",
            "Transplant seedlings in rows 20x15 cm spacing",
            "Apply basal dose of phosphorus and potassium before transplanting",
            "Maintain 2-5 cm standing water throughout the crop period",
            "Apply nitrogen in 3 split doses at 15, 30, and 45 days after transplanting",
            "Monitor for pests like stem borer and brown plant hopper",
            "Drain water 10-15 days before harvest when grains are mature",
            "Harvest when 80-85% grains are straw colored"
        ],
        "youtube": "https://www.youtube.com/watch?v=example_rice"
    },

    "Wheat": {
        "sowing": "October–November",
        "seed": "Certified wheat seeds (100–120 kg/ha)",
        "land": "Loamy soil with good fertility",
        "fertilizer": "Nitrogen + phosphorus as per soil test",
        "irrigation": "4–5 irrigations at critical stages",
        "diseases": "Rust, smut",
        "harvest": "March–April",
        "steps": [
            "Prepare field by deep plowing and leveling for uniform sowing",
            "Treat seeds with fungicide to prevent smut disease",
            "Sow seeds in rows 20-22 cm apart at 4-5 cm depth",
            "Apply basal dose of phosphorus and half nitrogen at sowing",
            "First irrigation at crown root initiation (20-25 DAS)",
            "Apply remaining nitrogen in 2-3 split doses",
            "Second irrigation at tillering stage, third at jointing stage",
            "Fourth irrigation at flowering stage, fifth at grain filling",
            "Monitor for rust diseases and apply fungicides if needed",
            "Harvest when grains are hard and moisture content is 12-14%"
        ],
        "youtube": "https://www.youtube.com/watch?v=example_wheat"
    },

    "Maize": {
        "sowing": "June–July",
        "seed": "Hybrid maize seeds",
        "land": "Loamy soil with good drainage",
        "fertilizer": "Nitrogen-rich fertilizer in splits",
        "irrigation": "Regular irrigation, avoid waterlogging",
        "diseases": "Stem borer, leaf blight",
        "harvest": "90–110 days after sowing",
        "steps": [
            "Prepare field with proper tillage and create ridges/furrows",
            "Treat seeds with fungicide and insecticide before sowing",
            "Sow seeds in rows 60-75 cm apart, 2-3 seeds per hill at 4-5 cm depth",
            "Thin to one healthy seedling per hill after germination",
            "Apply full phosphorus and potassium, half nitrogen as basal dose",
            "Apply remaining nitrogen in 2 split doses at knee-high and tasseling",
            "First irrigation immediately after sowing, then at regular intervals",
            "Monitor for stem borer and apply control measures",
            "Apply earthing up at knee-high stage for better root development",
            "Harvest when husks turn brown and grains become hard"
        ],
        "youtube": "https://www.youtube.com/watch?v=example_maize"
    },

    "Cotton": {
        "sowing": "June–July",
        "seed": "Bt cotton hybrid seeds",
        "land": "Black soil with good moisture retention",
        "fertilizer": "Balanced NPK, avoid excess nitrogen",
        "irrigation": "Moderate, critical at flowering",
        "diseases": "Bollworm, leaf curl virus",
        "harvest": "November–January",
        "steps": [
            "Prepare field with deep plowing and create raised beds",
            "Treat Bt cotton seeds with fungicide before sowing",
            "Sow seeds in rows 90-120 cm apart at 3-4 cm depth",
            "Maintain plant spacing of 60-75 cm within rows",
            "Apply basal dose of phosphorus and potassium",
            "Apply nitrogen in 3-4 split doses starting from 30 DAS",
            "First irrigation after sowing, then at square formation",
            "Critical irrigations at flowering and boll development stages",
            "Monitor for bollworm and sucking pests regularly",
            "Harvest when 60-70% bolls open and lint is white"
        ],
        "youtube": "https://www.youtube.com/watch?v=example_cotton"
    },

    "Groundnut": {
        "sowing": "June–July",
        "seed": "Bold, disease-free kernels",
        "land": "Sandy or red soil with drainage",
        "fertilizer": "Gypsum + phosphorus",
        "irrigation": "Light but frequent irrigation",
        "diseases": "Leaf spot, rust",
        "harvest": "October",
        "steps": [
            "Prepare field with light tillage to avoid soil compaction",
            "Treat seeds with fungicide and rhizobium culture",
            "Sow seeds in rows 30-45 cm apart at 5-6 cm depth",
            "Maintain 15-20 cm spacing between plants within rows",
            "Apply gypsum 200-300 kg/ha at sowing or pegging stage",
            "Apply phosphorus as basal dose, avoid excess nitrogen",
            "Irrigate immediately after sowing and keep soil moist",
            "Apply light irrigations at pegging and pod development stages",
            "Monitor for leaf spot disease and apply fungicides",
            "Harvest when 70-80% pods are mature and leaves turn yellow"
        ],
        "youtube": "https://www.youtube.com/watch?v=example_groundnut"
    },

    "Gram": {
        "sowing": "October–November",
        "seed": "Certified chickpea seeds",
        "land": "Well-drained loamy soil",
        "fertilizer": "Phosphorus and molybdenum",
        "irrigation": "2-3 irrigations, avoid waterlogging",
        "diseases": "Wilt, blight",
        "harvest": "February–March",
        "steps": [
            "Prepare field with minimum tillage to preserve soil moisture",
            "Treat seeds with fungicide and rhizobium culture",
            "Sow seeds in rows 30-45 cm apart at 5-6 cm depth",
            "Maintain 10-15 cm spacing between plants",
            "Apply phosphorus as basal dose, avoid nitrogen fertilizers",
            "Apply molybdenum through foliar spray if deficiency observed",
            "First irrigation at branching stage, second at pod filling",
            "Third irrigation if needed at maturity stage",
            "Monitor for wilt disease and remove affected plants",
            "Harvest when pods turn yellow and 80% leaves dry"
        ],
        "youtube": "https://www.youtube.com/watch?v=example_gram"
    },

    "Mustard": {
        "sowing": "October–November",
        "seed": "Quality mustard seeds",
        "land": "Fertile loamy soil",
        "fertilizer": "Nitrogen and phosphorus",
        "irrigation": "2-3 irrigations",
        "diseases": "Alternaria blight, white rust",
        "harvest": "February–March",
        "steps": [
            "Prepare fine seedbed with proper tillage",
            "Treat seeds with fungicide before sowing",
            "Broadcast seeds uniformly or sow in rows 30 cm apart",
            "Lightly cover seeds with soil and press with wooden plank",
            "Apply nitrogen and phosphorus as basal dose",
            "First irrigation immediately after sowing",
            "Second irrigation at buttoning stage, third at pod filling",
            "Monitor for aphids and apply insecticides if needed",
            "Apply fungicides for blight control if observed",
            "Harvest when 80% siliquae turn yellow"
        ],
        "youtube": "https://www.youtube.com/watch?v=example_mustard"
    },

    "Barley": {
        "sowing": "October–November",
        "seed": "Certified barley seeds",
        "land": "Well-drained fertile soil",
        "fertilizer": "Nitrogen and phosphorus",
        "irrigation": "3-4 irrigations",
        "diseases": "Rust, smut",
        "harvest": "March–April",
        "steps": [
            "Prepare field with proper plowing and leveling",
            "Treat seeds with fungicide to prevent smut",
            "Sow seeds in rows 20-25 cm apart at 4-5 cm depth",
            "Apply basal dose of phosphorus and half nitrogen",
            "First irrigation at crown root initiation stage",
            "Apply remaining nitrogen in 2 split doses",
            "Monitor for rust diseases and apply fungicides",
            "Irrigate at tillering, jointing, and grain filling stages",
            "Harvest when grains are hard and moisture content low"
        ],
        "youtube": "https://www.youtube.com/watch?v=example_barley"
    },

    "Vegetables": {
        "sowing": "Season dependent",
        "seed": "Hybrid vegetable seeds",
        "land": "Loamy soil rich in organic matter",
        "fertilizer": "Organic manure + balanced NPK",
        "irrigation": "Frequent light irrigation",
        "diseases": "Aphids, leaf curl, blight",
        "harvest": "30–90 days",
        "steps": [
            "Prepare raised beds or nursery for seedling production",
            "Sow seeds in nursery or directly in field based on crop",
            "Transplant seedlings when 3-4 true leaves appear",
            "Maintain proper spacing as per crop requirements",
            "Apply well-decomposed organic manure before planting",
            "Apply balanced NPK fertilizers in split doses",
            "Provide frequent light irrigations to keep soil moist",
            "Install trellis/net for climbing vegetables",
            "Monitor for pests and diseases regularly",
            "Harvest at appropriate maturity stage for each vegetable"
        ],
        "youtube": "https://www.youtube.com/watch?v=example_vegetables"
    },

    "Sugarcane": {
        "sowing": "February–March",
        "seed": "Disease-free sugarcane setts",
        "land": "Deep fertile soil with good drainage",
        "fertilizer": "Heavy nitrogen and potassium",
        "irrigation": "Frequent irrigation",
        "diseases": "Red rot, smut",
        "harvest": "12–18 months",
        "steps": [
            "Prepare field with deep plowing and create furrows",
            "Select healthy, disease-free sugarcane setts",
            "Treat setts with fungicide before planting",
            "Plant setts in furrows 75-90 cm apart, 15-20 cm within rows",
            "Cover setts with soil and provide immediate irrigation",
            "Apply heavy dose of nitrogen and potassium fertilizers",
            "Provide frequent irrigations throughout the growth period",
            "Monitor for borers and apply control measures",
            "Apply trash mulching for moisture conservation",
            "Harvest when sugar content is optimum (18-20 months)"
        ],
        "youtube": "https://www.youtube.com/watch?v=example_sugarcane"
    },

    "Watermelon": {
        "sowing": "March–April",
        "seed": "Hybrid watermelon seeds",
        "land": "Sandy loam soil with good drainage",
        "fertilizer": "Balanced NPK with micronutrients",
        "irrigation": "Regular irrigation, avoid waterlogging",
        "diseases": "Fusarium wilt, powdery mildew",
        "harvest": "75–90 days",
        "steps": [
            "Prepare raised beds for better drainage",
            "Sow 2-3 seeds per hill in rows 2-2.5 m apart",
            "Thin to one healthy seedling per hill after germination",
            "Apply well-decomposed organic manure in pits",
            "Provide trellis support for vine climbing",
            "Apply balanced fertilizers at sowing and vegetative stages",
            "Irrigate regularly but avoid waterlogging",
            "Monitor for fruit flies and apply insecticides",
            "Mulch around plants to conserve moisture",
            "Harvest when fruits are fully mature and rind is hard"
        ],
        "youtube": "https://www.youtube.com/watch?v=example_watermelon"
    }
}


# =============================
# 🌿 DISEASE MODEL
# =============================
disease_model = tf.keras.models.load_model("tomato_disease_model.h5")
DISEASE_CLASSES = ["Early Blight", "Healthy", "Late Blight", "Leaf Mold"] 

# =============================
# 🥔 POTATO DISEASE MODEL
# =============================
potato_disease_model = tf.keras.models.load_model("potato_disease_model.h5")

POTATO_DISEASE_CLASSES = [
    "Early Blight",   # index 0
    "Healthy",        # index 1
    "Late Blight"     # index 2
]

# =============================
# 🌶️ PEPPER DISEASE MODEL
# =============================
pepper_disease_model = tf.keras.models.load_model("pepper_disease_model.h5")

PEPPER_DISEASE_CLASSES = [
    "Bacterial Spot", # index 0
    "Healthy"         # index 1
]


UPLOAD_FOLDER = "static"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# =============================
# 🌱 CROP CLASSIFIER (Stage 1)
# =============================
crop_classifier = tf.keras.models.load_model("crop_classifier_model.h5")

# ⚠️ Order MUST match train_data.class_indices printed during training
CROP_CLASSES = [
    "Invalid",
    "Pepper",
    "Potato",
    "Tomato"
]

def predict_crop(img_array):
    preds = crop_classifier.predict(img_array)[0]
    return CROP_CLASSES[np.argmax(preds)]



# =============================
# 🚦 ROUTES
# =============================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/crop")
def crop_selection():
    season = request.args.get("season")
    soil = request.args.get("soil")
    water = request.args.get("water")

    predicted_crops = None
    if season and soil and water:
        predicted_crops = get_crop_suggestions(season, soil, water)

    return render_template("crop.html", season=season, soil=soil, water=water, predicted_crops=predicted_crops)

@app.route("/crop-plan/<crop>")
def crop_plan(crop):
    plan = CROP_PLANS.get(crop)
    return render_template("crop_plan.html", crop=crop, plan=plan)

@app.route("/disease")
def disease_page():
    return render_template("disease.html")

@app.route("/predict_disease", methods=["POST"])
def predict_disease():
    img_file = request.files.get("image")
    if not img_file:
        return render_template("disease.html")

    img_path = os.path.join(app.config["UPLOAD_FOLDER"], "uploaded_leaf.jpg")
    img_file.save(img_path)

    img = load_img(img_path, target_size=(224, 224))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # =============================
    # STAGE 1: CROP CLASSIFICATION
    # =============================
    crop = predict_crop(img_array)

    if crop == "Invalid":
        return render_template(
            "disease.html",
            prediction="Invalid Image",
            detected_crop=crop,
            invalid_image=True
        )

    # =============================
    # STAGE 2: DISEASE DETECTION
    # =============================
    confidence = 0
    predicted_class = None

    # -------- Tomato --------
    if crop == "Tomato":
        preds = disease_model.predict(img_array)[0]
        confidence = float(np.max(preds))
        predicted_class = DISEASE_CLASSES[np.argmax(preds)]

    # -------- Potato --------
    elif crop == "Potato":
        preds = potato_disease_model.predict(img_array)[0]
        confidence = float(np.max(preds))
        predicted_class = POTATO_DISEASE_CLASSES[np.argmax(preds)]

    # -------- Pepper --------
    elif crop == "Pepper":
        preds = pepper_disease_model.predict(img_array)[0]
        confidence = float(np.max(preds))
        predicted_class = PEPPER_DISEASE_CLASSES[np.argmax(preds)]

    # If crop not detected properly
    else:
        return render_template(
            "disease.html",
            invalid_image=True
        )

    # 🔹 Generate Treatment Plan
    treatment_data = generate_treatment_plan(
        crop,
        predicted_class,
        confidence
    )

    if treatment_data is None:
        treatment_data = {}

    return render_template(
        "disease.html",
        prediction=predicted_class,
        detected_crop=crop,
        invalid_image=False,
        treatment=treatment_data
    )

# ==========================================
# 🩺 MANUAL TREATMENT MODE (Session Based)
# ==========================================

@app.route("/manual-treatment", methods=["GET"])
def manual_treatment():

    if "manual" not in session:
        session["manual"] = {}

    manual = session["manual"]
    step = request.args.get("step", "crop")
    value = request.args.get("value")

    # -----------------------------
    # RESET SESSION
    # -----------------------------
    if step == "reset":
        session.pop("manual", None)
        return redirect(url_for("manual_treatment"))

    # -----------------------------
    # STEP 1: SELECT CROP
    # -----------------------------
    if step == "crop":
        crops = list(TREATMENT_KNOWLEDGE.keys())
        return render_template(
            "manual_treatment.html",
            step="crop",
            crops=crops
        )

    # -----------------------------
    # STEP 2: SELECT PROBLEM
    # -----------------------------
    if step == "problem":
        if value:
            manual["crop"] = value
            session["manual"] = manual

        crop = manual.get("crop")

        diseases = list(TREATMENT_KNOWLEDGE[crop].get("diseases", {}).keys())
        pests = list(TREATMENT_KNOWLEDGE[crop].get("pests", {}).keys())

        return render_template(
            "manual_treatment.html",
            step="problem",
            crop=crop,
            diseases=diseases,
            pests=pests
        )

    # -----------------------------
    # STEP 3: SELECT DISEASE / PEST
    # -----------------------------
    if step == "problem_select":
        manual["problem"] = value
        crop = manual.get("crop")

        if value in TREATMENT_KNOWLEDGE[crop]["diseases"]:
            manual["type"] = "disease"
            next_step = "disease_severity"
        else:
            manual["type"] = "pest"
            next_step = "pest_insects"

        session["manual"] = manual
        return redirect(url_for("manual_treatment", step=next_step))

    # =========================================================
    # 🔬 DISEASE FLOW
    # =========================================================

    # STEP 4: SEVERITY
    if step == "disease_severity":
        if value:
            manual["severity"] = value
            session["manual"] = manual
            return redirect(url_for("manual_treatment", step="disease_humidity"))

        return render_template(
            "manual_treatment.html",
            step="disease_severity",
            crop=manual["crop"],
            problem=manual["problem"]
        )

    # STEP 5: HUMIDITY
    if step == "disease_humidity":
        if value:
            manual["humidity"] = value
            session["manual"] = manual
            return redirect(url_for("manual_treatment", step="disease_spread"))

        return render_template(
            "manual_treatment.html",
            step="disease_humidity",
            crop=manual["crop"],
            problem=manual["problem"]
        )

    # STEP 6: SPREAD
    if step == "disease_spread":
        if value:
            manual["spread"] = value
            session["manual"] = manual
            return redirect(url_for("manual_treatment", step="generate_disease"))

        return render_template(
            "manual_treatment.html",
            step="disease_spread",
            crop=manual["crop"],
            problem=manual["problem"]
        )

    # FINAL: GENERATE DISEASE RESULT
    if step == "generate_disease":

        confidence = calculate_disease_confidence(
            manual["severity"],
            manual["humidity"],
            manual["spread"]
        )

        treatment = generate_treatment_plan(
            manual["crop"],
            manual["problem"],
            confidence
        )

        return render_template(
            "manual_treatment.html",
            step="result",
            treatment=treatment,
            crop=manual["crop"],
            problem=manual["problem"]
        )

    # =========================================================
    # 🐛 PEST FLOW
    # =========================================================

    # STEP 4: INSECTS
    if step == "pest_insects":
        if value:
            manual["insects"] = value
            session["manual"] = manual
            return redirect(url_for("manual_treatment", step="pest_damage"))

        return render_template(
            "manual_treatment.html",
            step="pest_insects",
            crop=manual["crop"],
            problem=manual["problem"]
        )

    # STEP 5: DAMAGE %
    if step == "pest_damage":
        if value:
            manual["damage"] = value
            session["manual"] = manual
            return redirect(url_for("manual_treatment", step="pest_spread"))

        return render_template(
            "manual_treatment.html",
            step="pest_damage",
            crop=manual["crop"],
            problem=manual["problem"]
        )

    # STEP 6: RAPID SPREAD
    if step == "pest_spread":
        if value:
            manual["rapid"] = value
            session["manual"] = manual
            return redirect(url_for("manual_treatment", step="generate_pest"))

        return render_template(
            "manual_treatment.html",
            step="pest_spread",
            crop=manual["crop"],
            problem=manual["problem"]
        )

    # FINAL: GENERATE PEST RESULT
    if step == "generate_pest":

        confidence = calculate_pest_confidence(
            manual["insects"],
            manual["damage"],
            manual["rapid"]
        )

        treatment = generate_treatment_plan(
            manual["crop"],
            manual["problem"],
            confidence
        )

        return render_template(
            "manual_treatment.html",
            step="result",
            treatment=treatment,
            crop=manual["crop"],
            problem=manual["problem"]
        )

    return redirect(url_for("manual_treatment"))
# =============================
# ▶ RUN
# =============================
if __name__ == "__main__":
    app.run(debug=True)
