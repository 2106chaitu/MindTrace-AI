# ==========================================================
# Suicide Risk Assessment Agent
# AI Powered Mental Health Text Analyzer
# ==========================================================

from pathlib import Path
import re
import string

import joblib
import numpy as np
import streamlit as st


# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent

MODEL_DIR = BASE_DIR / "models"
CSS_FILE = ROOT_DIR / "style.css"


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Suicide Risk Assessment Agent",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# LOAD CSS
# ==========================================================

if CSS_FILE.exists():

    with open(CSS_FILE, "r", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


# ==========================================================
# MODEL FILE PATHS
# ==========================================================

MODEL_PATH = MODEL_DIR / "suicide_risk_model.pkl"
VECTORIZER_PATH = MODEL_DIR / "tfidf_vectorizer.pkl"
LABEL_ENCODER_PATH = MODEL_DIR / "label_encoder.pkl"


# ==========================================================
# LOAD MACHINE LEARNING MODEL
# ==========================================================

try:

    model = joblib.load(MODEL_PATH)

    vectorizer = joblib.load(VECTORIZER_PATH)

    label_encoder = joblib.load(LABEL_ENCODER_PATH)

except FileNotFoundError as e:

    st.error("❌ Model files could not be found.")

    st.code(str(e))

    st.info(
        "Please make sure the following files exist inside "
        "backend/models/:\n\n"
        "• suicide_risk_model.pkl\n"
        "• tfidf_vectorizer.pkl\n"
        "• label_encoder.pkl"
    )

    st.stop()

except Exception as e:

    st.error("❌ Unable to load the machine learning model.")

    st.code(str(e))

    st.stop()


# ==========================================================
# TEXT CLEANING FUNCTION
# ==========================================================

def clean_text(text: str) -> str:

    text = text.lower()

    # Remove URLs
    text = re.sub(
        r"http\S+|www\S+|https\S+",
        "",
        text
    )

    # Remove HTML tags
    text = re.sub(
        r"<.*?>",
        "",
        text
    )

    # Remove punctuation
    text = text.translate(
        str.maketrans(
            "",
            "",
            string.punctuation
        )
    )

    # Remove numbers
    text = re.sub(
        r"\d+",
        "",
        text
    )

    # Remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


# ==========================================================
# SESSION STATE
# ==========================================================

if "history" not in st.session_state:

    st.session_state.history = []


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:10px 0 15px 0;
        ">
            <div style="
                font-size:28px;
                font-weight:700;
            ">
                🛡️ MindTrace AI
            </div>

            <div style="
                font-size:13px;
                opacity:0.75;
                margin-top:4px;
            ">
                Mental Wellness Screening
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.subheader("📌 About")

    st.write(
        """
        MindTrace AI analyzes written text using
        Natural Language Processing and Machine Learning
        to identify language patterns that may be associated
        with suicide risk.
        """
    )

    st.markdown("---")

    st.subheader("🤖 Model")

    st.success("Linear SVM")

    st.markdown("---")

    st.subheader("📊 Features")

    st.write("✅ Text Analysis")
    st.write("✅ TF-IDF Vectorization")
    st.write("✅ Machine Learning")
    st.write("✅ Confidence Score")
    st.write("✅ Prediction History")

    st.markdown("---")

    st.info(
        """
        ⚠️ This application is intended for
        educational screening purposes only.

        It is not a medical diagnosis and should
        not replace professional mental-health care.
        """
    )


# ==========================================================
# MAIN HEADER
# ==========================================================

st.markdown(
    """
    <div class="header">

        <h1>
            🛡️ Suicide Risk Assessment Agent
        </h1>

        <h4>
            AI Powered Mental Health Text Analyzer
        </h4>

        <p>
            Analyze written text using Natural Language Processing
            and Machine Learning to identify potential indicators
            of emotional distress.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


st.write("")


# ==========================================================
# INFORMATION CARD
# ==========================================================

st.markdown(
    """
    <div class="info-box">

        <h3>📝 Enter your thoughts</h3>

        <p>
            Write a sentence or short message below.
            The trained machine learning model will analyze
            the text and estimate whether it contains language
            associated with suicide risk.
        </p>

        <p>
            Your result is an automated screening prediction,
            not a clinical diagnosis.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


st.write("")


# ==========================================================
# TEXT INPUT
# ==========================================================

user_input = st.text_area(
    "Enter your text",

    height=250,

    placeholder="""
Example:

I don't know what to do anymore.
Everything feels hopeless and I feel alone...
"""
)


st.write("")


# ==========================================================
# ANALYZE BUTTON
# ==========================================================

predict = st.button(
    "🔍 Analyze Text",
    use_container_width=True
)


# ==========================================================
# PREDICTION LOGIC
# ==========================================================

if predict:

    if not user_input.strip():

        st.warning(
            "⚠️ Please enter some text before analyzing."
        )

    else:

        cleaned_text = clean_text(user_input)

        if not cleaned_text:

            st.warning(
                "⚠️ Please enter meaningful text."
            )

        else:

            with st.spinner(
                "🔄 Analyzing text..."
            ):

                try:

                    # ======================================
                    # TF-IDF TRANSFORMATION
                    # ======================================

                    transformed_text = vectorizer.transform(
                        [cleaned_text]
                    )


                    # ======================================
                    # MODEL PREDICTION
                    # ======================================

                    prediction = model.predict(
                        transformed_text
                    )[0]


                    # ======================================
                    # CONVERT PREDICTION TO LABEL
                    # ======================================

                    predicted_label = (
                        label_encoder
                        .inverse_transform([prediction])[0]
                    )

                    predicted_label = str(
                        predicted_label
                    )


                    # ======================================
                    # CONFIDENCE SCORE
                    # ======================================

                    try:

                        decision_score = (
                            model
                            .decision_function(
                                transformed_text
                            )[0]
                        )

                        confidence = (
                            1 /
                            (
                                1 +
                                np.exp(
                                    -abs(
                                        decision_score
                                    )
                                )
                            )
                        ) * 100

                        confidence = round(
                            float(confidence),
                            2
                        )

                    except Exception:

                        confidence = 0.0


                    # ======================================
                    # SAVE HISTORY
                    # ======================================

                    st.session_state.history.insert(
                        0,
                        {
                            "text": user_input,
                            "prediction": predicted_label,
                            "confidence": confidence
                        }
                    )


                except Exception as e:

                    st.error(
                        "❌ An error occurred while analyzing the text."
                    )

                    st.code(str(e))

                    st.stop()


            # ==================================================
            # RESULT SECTION
            # ==================================================

            st.write("")

            st.markdown("---")

            st.subheader("📊 Assessment Result")


            # ==================================================
            # LOW RISK
            # ==================================================

            if predicted_label.lower() == "non-suicide":

                st.success(
                    "🟢 Low Risk Detected"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Confidence Score",
                        f"{confidence}%"
                    )

                with col2:

                    st.metric(
                        "Assessment",
                        "Low Risk"
                    )


                st.progress(
                    min(
                        confidence / 100,
                        1.0
                    )
                )


                st.markdown(
                    """
                    ### ✅ AI Assessment

                    The entered text **does not contain strong
                    indicators associated with suicide risk**
                    according to the trained machine learning model.

                    **Remember:** This is an automated prediction
                    and not a medical diagnosis.
                    """
                )


                st.markdown(
                    "### 💡 Positive Suggestions"
                )


                st.info(
                    """
                    🌿 **Stay connected**
                    with friends and family.

                    🥗 **Maintain healthy eating habits**
                    and stay hydrated.

                    😴 **Maintain a regular sleep routine.**

                    🚶 **Take a short walk or exercise**
                    when possible.

                    🧘 **Practice mindfulness and relaxation**
                    activities.

                    🎨 **Spend time on hobbies**
                    and activities you enjoy.

                    💬 **Talk with someone you trust**
                    when you feel overwhelmed.
                    """
                )


            # ==================================================
            # HIGHER RISK
            # ==================================================

            else:

                st.error(
                    "🔴 Higher Risk Detected"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Confidence Score",
                        f"{confidence}%"
                    )

                with col2:

                    st.metric(
                        "Assessment",
                        "Elevated Risk"
                    )


                st.progress(
                    min(
                        confidence / 100,
                        1.0
                    )
                )


                st.markdown(
                    """
                    ### ⚠️ AI Assessment

                    The entered text contains language that
                    **may indicate elevated suicide risk**.

                    This result is generated by a machine learning
                    model and **is not a clinical diagnosis**.
                    """
                )


                st.markdown(
                    "### 💙 Supportive Suggestions"
                )


                st.warning(
                    """
                    💬 **Talk to someone you trust**
                    and avoid staying alone if you feel unsafe.

                    🧑‍⚕️ **Consider reaching out to a qualified
                    mental-health professional.**

                    🤝 **Stay connected with supportive people**
                    around you.

                    🌿 **Move to a safe and supportive environment**
                    if possible.

                    🆘 **If you or someone else is in immediate
                    danger, contact local emergency services
                    or an appropriate crisis resource immediately.**

                    ❤️ **You do not have to face difficult moments alone.**
                    """
                )


            st.markdown("---")


# ==========================================================
# PREDICTION HISTORY
# ==========================================================

if len(st.session_state.history) > 0:

    st.subheader("📜 Recent Prediction History")

    for item in st.session_state.history[:5]:

        prediction_text = str(
            item["prediction"]
        )

        confidence_value = item["confidence"]


        if prediction_text.lower() == "suicide":

            st.error(
                f"🔴 {prediction_text} | "
                f"Confidence: {confidence_value}%"
            )

        else:

            st.success(
                f"🟢 {prediction_text} | "
                f"Confidence: {confidence_value}%"
            )


# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        padding:20px 10px;
        opacity:0.85;
    ">

        <p style="
            font-size:16px;
            font-weight:600;
        ">
            💙 You are not alone. Reaching out for support
            can be the first step toward a better moment.
        </p>

        <p style="font-size:13px;">
            MindTrace AI is an educational screening tool,
            not a medical diagnosis or substitute for
            professional care.
        </p>

        <p style="font-size:12px;">
            Built with ❤️ using Python • Streamlit •
            Scikit-Learn • Machine Learning
        </p>

    </div>
    """,
    unsafe_allow_html=True
)