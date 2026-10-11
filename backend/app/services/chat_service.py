"""
AI Agricultural Assistant Service
Multilingual English + Marathi
Uses OpenAI LLM with local agronomy knowledge-base fallback.
"""

import os
import re
from typing import Dict, Any, List, Optional
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# ENVIRONMENT
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(ROOT_DIR / ".env")

LLM_API_KEY = os.getenv("LLM_API_KEY", "").strip()

# You can change this model later if required.
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6")

openai_client: Optional[OpenAI] = None

if LLM_API_KEY and LLM_API_KEY != "your_llm_api_key_here":
    try:
        openai_client = OpenAI(api_key=LLM_API_KEY)
        print("OpenAI AI Assistant initialized successfully.")
    except Exception as e:
        print(f"OpenAI initialization failed: {e}")
        openai_client = None
else:
    print("OpenAI API key not configured. Expert agronomy fallback will be used.")


# ============================================================
# AGRICULTURAL KNOWLEDGE BASE - ENGLISH
# ============================================================

AGRI_KNOWLEDGE_BASE_EN = {

    "leaf_curl": {
        "keywords": [
            "curl", "virus", "whitefly", "wrinkled",
            "puckered", "stunted"
        ],
        "reply": """Chilli Leaf Curl (ChiLCV) is commonly transmitted by whiteflies (*Bemisia tabaci*).

**Recommended Action:**
1. Install 15–20 yellow sticky traps per acre to monitor and reduce whitefly populations.
2. Neem-based products such as azadirachtin can be used according to the product label.
3. Remove and safely destroy severely infected plants.
4. Avoid excessive nitrogen because it can encourage soft vegetative growth.
5. Control weeds and alternate hosts around the field.

Always follow the pesticide label and local agricultural recommendations.""",

        "suggestions": [
            "What are the symptoms of leaf curl?",
            "How can I control whiteflies?",
            "How to prepare neem oil spray?"
        ]
    },

    "bacterial_spot": {
        "keywords": [
            "bacterial", "spot", "dark spot",
            "water soaked", "xanthomonas"
        ],
        "reply": """Bacterial spot can cause dark, water-soaked or necrotic lesions on chilli leaves and fruits.

**Management:**
1. Avoid unnecessary overhead irrigation.
2. Keep foliage as dry as practical.
3. Remove badly infected plant material.
4. Improve field sanitation and drainage.
5. Use only locally approved bactericides/fungicides according to the product label.

Crop rotation and clean planting material can help reduce disease pressure.""",

        "suggestions": [
            "How can I prevent bacterial spot?",
            "Can bacterial spot affect chilli fruits?",
            "What causes bacterial leaf spots?"
        ]
    },

    "powdery_mildew": {
        "keywords": [
            "powdery", "mildew",
            "white powder", "white patch", "fungal"
        ],
        "reply": """Powdery mildew produces white fungal growth, often visible on leaf surfaces or undersides.

**Management:**
1. Maintain good plant spacing and air circulation.
2. Avoid excessive nitrogen fertilization.
3. Remove severely affected leaves where practical.
4. Use an approved fungicide according to its label and local recommendations.
5. Monitor the crop regularly because early treatment is generally more effective.""",

        "suggestions": [
            "How can I control powdery mildew organically?",
            "Why does powdery mildew occur?",
            "How does humidity affect powdery mildew?"
        ]
    },

    "cercospora": {
        "keywords": [
            "cercospora", "frogeye",
            "circular spot", "grey center",
            "leaf spot"
        ],
        "reply": """Cercospora leaf spot can produce circular lesions with lighter centers and darker margins.

**Management:**
1. Remove heavily infected plant debris.
2. Improve field drainage and air circulation.
3. Avoid prolonged leaf wetness.
4. Use locally recommended fungicides according to the product label.
5. Rotate crops where practical.""",

        "suggestions": [
            "How do I identify Cercospora?",
            "How can I prevent leaf spot?",
            "What is the difference between Cercospora and bacterial spot?"
        ]
    },

    "soil_npk": {
        "keywords": [
            "soil", "ph", "npk",
            "fertilizer", "urea", "dap",
            "potash", "nutrient",
            "deficiency", "yellow"
        ],
        "reply": """For chilli (*Capsicum annuum*), soil fertility should ideally be managed using a soil test.

**General guidance:**
- Maintain a suitable soil pH, commonly around 6.0–7.0.
- Nitrogen, phosphorus and potassium requirements depend on soil fertility, variety, yield target and production system.
- Avoid applying fertilizer only based on visual symptoms when a soil test is available.

**Common deficiency clues:**
- Older leaves becoming pale/yellow: may indicate nitrogen deficiency.
- Purplish coloration: may be associated with phosphorus deficiency, but other stresses can cause similar symptoms.
- Marginal leaf scorching: may be associated with potassium deficiency.
- Interveinal yellowing: may indicate magnesium or micronutrient problems.

A soil test is the best basis for fertilizer recommendations.""",

        "suggestions": [
            "How can I test soil pH?",
            "What fertilizer is suitable for chilli?",
            "What are the symptoms of nitrogen deficiency?"
        ]
    },

    "irrigation": {
        "keywords": [
            "irrigation", "water",
            "drip", "watering",
            "how often", "moisture"
        ],
        "reply": """Chilli needs balanced irrigation. Both water stress and excessive moisture can reduce plant performance.

**Best practices:**
1. Prefer drip irrigation where suitable.
2. Keep soil moisture relatively stable rather than allowing severe wet-dry cycles.
3. Pay particular attention to irrigation during flowering and fruit development.
4. Adjust irrigation according to soil type, weather, plant size and rainfall.
5. Avoid prolonged waterlogging because it can damage roots.""",

        "suggestions": [
            "Why are chilli flowers dropping?",
            "How often should I irrigate chilli?",
            "What are symptoms of overwatering?"
        ]
    },

    "flowering": {
        "keywords": [
            "flower", "flowers", "flowering",
            "no flower", "not flowering",
            "does not flower", "doesn't flower",
            "flower drop", "flowers dropping",
            "blossom", "fruit setting",
            "fruit set"
        ],
        "reply": """Poor flowering or flower drop in chilli can have several causes.

**Common causes:**
1. Excess nitrogen can produce excessive leaf growth instead of reproductive growth.
2. High or low temperatures can interfere with flowering and pollen viability.
3. Irregular irrigation or moisture stress can cause flower drop.
4. Poor sunlight can reduce flowering.
5. Nutrient imbalance, especially involving phosphorus or potassium, may contribute.
6. Pest or disease pressure can weaken the plant.
7. Excessively dense vegetation can reduce light and airflow.

**What to check:**
- Make sure plants receive adequate sunlight.
- Avoid excessive urea/nitrogen.
- Maintain consistent soil moisture.
- Check the plants for pests and diseases.
- Use soil testing before making major fertilizer changes.

If you tell me the plant's age, fertilizer used, irrigation method and current temperature, I can help narrow down the likely cause.""",

        "suggestions": [
            "Why are chilli flowers falling?",
            "Which fertilizer helps chilli flowering?",
            "Why does my chilli plant have leaves but no flowers?"
        ]
    }
}


# ============================================================
# AGRICULTURAL KNOWLEDGE BASE - MARATHI
# ============================================================

AGRI_KNOWLEDGE_BASE_MR = {

    "leaf_curl": {
        "keywords": [
            "बोकड्या", "चुरडा", "मुरडा",
            "पांढरी माशी", "पान वळणे",
            "व्हायरस", "curl", "virus"
        ],

        "reply": """मिरचीवरील चुरडा-मुरडा (बोकड्या) रोग प्रामुख्याने पांढऱ्या माशीमार्फत पसरतो.

**उपाययोजना:**
१. एकरी १५–२० पिवळे चिकट सापळे लावा.
२. कडुनिंबावर आधारित कीटकनियंत्रक उत्पादने लेबलवरील मात्रेनुसार वापरा.
३. जास्त बाधित झाडे काढून शेताबाहेर नष्ट करा.
४. युरियाचा अतिवापर टाळा.
५. शेतातील तण आणि रोगाचा पर्यायी आश्रय देणारी झाडे नियंत्रित करा.

कीटकनाशक वापरताना स्थानिक कृषी विभागाच्या शिफारशी आणि उत्पादनाचे लेबल पाळा.""",

        "suggestions": [
            "पांढऱ्या माशीचे नियंत्रण कसे करावे?",
            "बोकड्या रोगाची लक्षणे कोणती?",
            "कडुलिंबावर आधारित फवारणी कशी करावी?"
        ]
    },

    "bacterial_spot": {
        "keywords": [
            "जिवाणू", "ठिपके",
            "काळे डाग", "bacterial",
            "spot", "डाग"
        ],

        "reply": """जिवाणूजन्य ठिपके रोगामुळे मिरचीच्या पानांवर काळपट किंवा पाणथळ डाग दिसू शकतात.

**उपाययोजना:**
१. अनावश्यक तुषार सिंचन टाळा.
२. पाने जास्त वेळ ओली राहणार नाहीत याची काळजी घ्या.
३. जास्त बाधित पाने व अवशेष काढून टाका.
४. शेतात पाण्याचा योग्य निचरा ठेवा.
५. स्थानिक शिफारशीनुसारच औषधांचा वापर करा.""",

        "suggestions": [
            "जिवाणूजन्य ठिपके रोग कसा टाळावा?",
            "पावसाळ्यात मिरचीची काळजी कशी घ्यावी?",
            "पानांवर काळे डाग का येतात?"
        ]
    },

    "powdery_mildew": {
        "keywords": [
            "भुरी", "पांढरी बुरशी",
            "पांढरी भुकटी",
            "mildew", "powdery"
        ],

        "reply": """भुरी रोगामध्ये मिरचीच्या पानांवर पांढऱ्या रंगाची बुरशी दिसते.

**उपाययोजना:**
१. झाडांमध्ये हवा खेळती राहील असे अंतर ठेवा.
२. नत्रयुक्त खतांचा अतिरेक टाळा.
३. जास्त बाधित पाने काढून टाका.
४. रोगाच्या सुरुवातीच्या अवस्थेत नियमित निरीक्षण करा.
५. स्थानिक कृषी शिफारशीनुसार मान्यताप्राप्त बुरशीनाशक वापरा.""",

        "suggestions": [
            "भुरी रोग का होतो?",
            "भुरी रोगावर सेंद्रिय उपाय कोणते?",
            "भुरी रोग कसा ओळखावा?"
        ]
    },

    "soil_npk": {
        "keywords": [
            "माती", "सामू", "खत",
            "युरिया", "पोटॅश",
            "अन्नद्रव्य", "पिवळे",
            "npk", "fertilizer"
        ],

        "reply": """मिरचीसाठी जमिनीची सुपीकता आणि सामू योग्य असणे महत्त्वाचे आहे.

**सामान्य मार्गदर्शन:**
- जमिनीचा pH साधारण ६.०–७.० योग्य मानला जातो.
- नत्र, स्फुरद आणि पालाशाची मात्रा जमिनीच्या परीक्षणानुसार ठरवणे योग्य आहे.
- फक्त पानांच्या लक्षणांवर आधारित मोठ्या प्रमाणात खत देणे टाळा.

**कमतरतेची काही सामान्य लक्षणे:**
- जुनी पाने पिवळी पडणे → नत्राची कमतरता असू शकते.
- पाने जांभळट होणे → स्फुरदाची कमतरता असू शकते.
- पानांच्या कडा करपणे → पालाशाची कमतरता असू शकते.
- शिरांमधील पिवळेपणा → मॅग्नेशियम किंवा सूक्ष्म अन्नद्रव्यांची समस्या असू शकते.

शक्य असल्यास माती परीक्षण करून खत व्यवस्थापन करा.""",

        "suggestions": [
            "मातीचा pH कसा तपासावा?",
            "मिरचीसाठी कोणते खत चांगले आहे?",
            "नत्राच्या कमतरतेची लक्षणे कोणती?"
        ]
    },

    "irrigation": {
        "keywords": [
            "पाणी", "सिंचन",
            "ठिबक", "ओलावा",
            "water", "irrigation"
        ],

        "reply": """मिरची पिकासाठी योग्य आणि नियमित पाणी व्यवस्थापन महत्त्वाचे आहे.

**महत्त्वाच्या सूचना:**
१. शक्य असल्यास ठिबक सिंचनाचा वापर करा.
२. जमिनीमध्ये जास्त ओलावा किंवा जास्त कोरडेपणा होऊ देऊ नका.
३. फुलोरा आणि फळधारणेच्या काळात पाण्याचा ताण पडू देऊ नका.
४. पाणी देण्याचे प्रमाण मातीचा प्रकार, हवामान, पावसाचे प्रमाण आणि झाडांची अवस्था यानुसार बदला.
५. पाणी साचून राहणार नाही याची काळजी घ्या.""",

        "suggestions": [
            "मिरचीची फुले का गळतात?",
            "मिरचीला किती दिवसांनी पाणी द्यावे?",
            "जास्त पाणी दिल्याची लक्षणे कोणती?"
        ]
    },

    "flowering": {
        "keywords": [
            "फुले", "फूल", "फुलोरा",
            "फुले येत नाहीत",
            "फुलं येत नाहीत",
            "फुले गळतात",
            "फुलगळ",
            "फळधारणा",
            "फळे लागत नाहीत"
        ],

        "reply": """मिरचीला फुले न येण्याची किंवा फुले गळण्याची अनेक कारणे असू शकतात.

**संभाव्य कारणे:**
१. युरिया किंवा नत्राचा अतिरेक झाल्यास पानांची वाढ जास्त होऊन फुलोरा कमी होऊ शकतो.
२. जास्त किंवा कमी तापमानामुळे फुलोऱ्यावर परिणाम होऊ शकतो.
३. पाण्याचा ताण किंवा अनियमित सिंचनामुळे फुले गळू शकतात.
४. पुरेसा सूर्यप्रकाश न मिळाल्यास फुलोरा कमी होऊ शकतो.
५. अन्नद्रव्यांचे असंतुलन कारणीभूत असू शकते.
६. किडी किंवा रोगामुळे झाड कमजोर होऊ शकते.

**काय तपासावे:**
- झाडाला पुरेसा सूर्यप्रकाश मिळतो का ते पाहा.
- युरिया/नत्राचा अतिरेक टाळा.
- जमिनीतील ओलावा नियमित ठेवा.
- झाडांवर किडी किंवा रोग आहेत का ते तपासा.
- शक्य असल्यास माती परीक्षण करा.

तुम्ही झाडाचे वय, कोणते खत दिले आहे, किती पाणी देता आणि सध्याचे तापमान सांगितल्यास कारण अधिक अचूकपणे शोधता येईल.""",

        "suggestions": [
            "मिरचीची फुले का गळतात?",
            "फुलोऱ्यासाठी कोणते खत द्यावे?",
            "मिरचीला पाने येतात पण फुले का येत नाहीत?"
        ]
    }
}


# ============================================================
# OPENAI SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT_EN = """
You are AgriSmart AI, an agricultural assistant for farmers.

Your job is to provide practical, understandable and responsible agricultural
guidance.

Focus especially on:
- Chilli cultivation
- Chilli diseases
- Pest management
- Flowering and fruit setting
- Soil health
- Fertilizers and nutrients
- Irrigation
- Crop recommendations
- Weather-related agricultural advice
- General farming questions

Rules:
1. Answer the user's actual question directly.
2. Do not restrict answers to a fixed list of predefined questions.
3. If the question is about agriculture, provide useful practical guidance.
4. If exact fertilizer/pesticide dosage depends on product formulation, soil test,
   crop stage or local regulations, say so rather than inventing certainty.
5. Do not recommend unsafe pesticide mixing.
6. Encourage following the product label and local agricultural recommendations.
7. If the user asks about a plant problem, explain likely causes and what to check.
8. Use simple language suitable for farmers.
9. If the user asks in Marathi, answer in Marathi.
10. If the user asks in English, answer in English.
11. You may use bullet points and numbered steps.
12. Do not say that you can only answer predefined questions.
"""


SYSTEM_PROMPT_MR = """
तुम्ही AgriSmart AI कृषी सहाय्यक आहात.

शेतकऱ्यांना सोप्या, स्पष्ट आणि उपयुक्त पद्धतीने कृषीविषयक मार्गदर्शन देणे हे तुमचे काम आहे.

विशेषतः खालील विषयांवर मदत करा:
- मिरची लागवड
- मिरचीवरील रोग
- किडींचे व्यवस्थापन
- फुलोरा आणि फळधारणा
- माती परीक्षण व माती आरोग्य
- खते आणि अन्नद्रव्ये
- सिंचन
- पीक शिफारस
- हवामानाशी संबंधित कृषी सल्ला
- इतर शेतीविषयक प्रश्न

नियम:
१. वापरकर्त्याच्या प्रश्नाचे थेट उत्तर द्या.
२. फक्त पूर्वनिश्चित प्रश्नांपुरते उत्तर मर्यादित ठेवू नका.
३. कृषीविषयक प्रश्न असल्यास शक्य तितके व्यावहारिक मार्गदर्शन द्या.
४. खत किंवा कीटकनाशकाची अचूक मात्रा उत्पादनाची formulation,
   माती परीक्षण, पिकाची अवस्था आणि स्थानिक नियमांवर अवलंबून असल्यास
   ते स्पष्ट सांगा.
५. असुरक्षित कीटकनाशक मिश्रणे सुचवू नका.
६. औषध वापरताना उत्पादनाचे लेबल आणि स्थानिक कृषी शिफारशी पाळण्यास सांगा.
७. झाडाच्या समस्येबाबत संभाव्य कारणे आणि काय तपासावे हे सांगा.
८. सोपी शेतकरी-अनुकूल भाषा वापरा.
९. प्रश्न मराठीत असल्यास मराठीत उत्तर द्या.
१०. प्रश्न इंग्रजीत असल्यास इंग्रजीत उत्तर द्या.
११. आवश्यक असल्यास मुद्दे आणि क्रमांक वापरा.
१२. फक्त predefined प्रश्नांचीच उत्तरे देता येतात असे सांगू नका.
"""


# ============================================================
# HELPER: LOCAL KNOWLEDGE BASE
# ============================================================

def get_knowledge_base_response(
    message: str,
    is_marathi: bool
) -> Optional[Dict[str, Any]]:

    msg_lower = message.lower().strip()

    kb = AGRI_KNOWLEDGE_BASE_MR if is_marathi else AGRI_KNOWLEDGE_BASE_EN

    for topic_key, topic_data in kb.items():

        for keyword in topic_data["keywords"]:

            if keyword.lower() in msg_lower:

                return {
                    "reply": topic_data["reply"],
                    "language": "mr" if is_marathi else "en",
                    "suggested_questions": topic_data["suggestions"],
                    "source": "expert_agronomy_system",
                    "topic": topic_key
                }

    return None


# ============================================================
# HELPER: OPENAI RESPONSE
# ============================================================

def get_openai_response(
    message: str,
    is_marathi: bool,
    conversation_history: Optional[List[Dict[str, str]]] = None
) -> Optional[str]:

    if openai_client is None:
        return None

    try:

        system_prompt = (
            SYSTEM_PROMPT_MR
            if is_marathi
            else SYSTEM_PROMPT_EN
        )

        # Build conversation context
        input_messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        # Add previous conversation if available
        if conversation_history:

            for item in conversation_history[-10:]:

                role = item.get("role", "user")
                content = item.get("content", "")

                if role not in ["user", "assistant"]:
                    continue

                if not content:
                    continue

                input_messages.append({
                    "role": role,
                    "content": content
                })

        # Current user question
        input_messages.append({
            "role": "user",
            "content": message
        })

        response = openai_client.responses.create(
            model=OPENAI_MODEL,
            input=input_messages
        )

        answer = response.output_text.strip()

        if answer:
            return answer

        return None

    except Exception as e:

        print(f"OpenAI API call error: {e}")

        return None


# ============================================================
# MAIN CHAT SERVICE
# ============================================================

class ChatService:

    @classmethod
    def get_response(
        cls,
        message: str,
        language: str = "en",
        conversation_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:

        if not message or not message.strip():

            return {
                "reply": (
                    "Please enter your agricultural question."
                    if language != "mr"
                    else "कृपया तुमचा कृषीविषयक प्रश्न विचारा."
                ),
                "language": language,
                "suggested_questions": [],
                "source": "validation"
            }

        message = message.strip()

        # Detect Marathi automatically
        is_marathi = (
            language == "mr"
            or bool(re.search(r'[\u0900-\u097F]', message))
        )

        # ====================================================
        # 1. Try OpenAI first
        # ====================================================

        if openai_client is not None:

            ai_answer = get_openai_response(
                message=message,
                is_marathi=is_marathi,
                conversation_history=conversation_history
            )

            if ai_answer:

                return {
                    "reply": ai_answer,
                    "language": "mr" if is_marathi else "en",
                    "suggested_questions": [],
                    "source": "openai",
                }

        # ====================================================
        # 2. Local expert knowledge fallback
        # ====================================================

        local_response = get_knowledge_base_response(
            message=message,
            is_marathi=is_marathi
        )

        if local_response:
            return local_response

        # ====================================================
        # 3. General fallback
        # ====================================================

        if is_marathi:

            general_reply = (
                "मी **AgriSmart AI कृषी सहाय्यक** आहे.\n\n"
                "तुम्ही मिरची, पिकांचे रोग, किडी, खते, "
                "माती, सिंचन, फुलोरा, फळधारणा, हवामान "
                "किंवा इतर शेतीविषयक कोणताही प्रश्न विचारू शकता."
            )

            general_suggestions = [
                "मिरचीला फुले का येत नाहीत?",
                "मिरचीची फुले का गळतात?",
                "मिरचीसाठी कोणते खत वापरावे?",
                "मिरचीवर किडींचे नियंत्रण कसे करावे?"
            ]

        else:

            general_reply = (
                "I am **AgriSmart AI**, your agricultural assistant.\n\n"
                "You can ask me about chilli cultivation, diseases, "
                "pests, fertilizers, soil, irrigation, flowering, "
                "fruit setting, weather-related farming decisions, "
                "or other agricultural questions."
            )

            general_suggestions = [
                "Why does my chilli plant not produce flowers?",
                "Why are chilli flowers dropping?",
                "Which fertilizer is suitable for chilli?",
                "How can I control pests in chilli?"
            ]

        return {
            "reply": general_reply,
            "language": "mr" if is_marathi else "en",
            "suggested_questions": general_suggestions,
            "source": "expert_agronomy_system"
        }