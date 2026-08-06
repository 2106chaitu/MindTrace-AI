# ==========================================================
# Suicide Risk Assessment Agent
# AI Powered Mental Health Text Analyzer
# ==========================================================

# -------------------------
# Import Libraries
# -------------------------

import streamlit as st
import joblib
import numpy as np
import re
import string

# -------------------------
# Page Configuration
# -------------------------

st.set_page_config(
    page_title="Suicide Risk Assessment Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------
# Load CSS
# -------------------------

def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# -------------------------
# Load Model Files
# -------------------------

model = joblib.load("suicide_risk_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# -------------------------
# Text Cleaning Function
# -------------------------

def clean_text(text):

    text = text.lower()

    text = re.sub(r"http\S+|www\S+|https\S+", "", text)

    text = re.sub(r"<.*?>", "", text)

    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    text = re.sub(r"\d+", "", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text

# -------------------------
# Sidebar
# -------------------------

with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/2785/2785819.png",
        width=120
    )

    st.title("Suicide Risk Assessment")

    st.markdown("---")

    st.subheader("📌 About")

    st.write(
        """
        This AI application analyzes text
        and predicts whether it contains
        language associated with suicide risk.
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

    st.markdown("---")

    st.info(
        "⚠ This application is intended "
        "for educational purposes only "
        "and should not replace "
        "professional mental health support."
    )

# -------------------------
# Header
# -------------------------

st.markdown(
    """
    <div class="header">
        <h1>🧠 Suicide Risk Assessment Agent</h1>
        <h4>AI Powered Mental Health Text Analyzer</h4>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# -------------------------
# Information Card
# -------------------------

st.markdown(
"""
<div class="info-box">

Enter any text below.

The trained Machine Learning model will analyze
the content and estimate whether it contains
language associated with suicide risk.

</div>
""",
unsafe_allow_html=True
)

st.write("")

# -------------------------
# Text Input
# -------------------------

user_input = st.text_area(

    "Enter your text",

    height=250,

    placeholder="""
Example:

I don't know what to do anymore.
Everything feels hopeless...
"""
)

st.write("")

# -------------------------
# Analyze Button
# -------------------------

predict = st.button(
    "🔍 Analyze Text",
    use_container_width=True
)
# ==========================================================
# Prediction Logic
# ==========================================================

if "history" not in st.session_state:
    st.session_state.history = []

if predict:

    if user_input.strip() == "":

        st.warning("⚠ Please enter some text before analyzing.")

    else:

        with st.spinner("Analyzing text..."):

            # Clean text
            cleaned_text = clean_text(user_input)

            # TF-IDF Transformation
            transformed_text = vectorizer.transform([cleaned_text])

            # Prediction
            prediction = model.predict(transformed_text)[0]

            # Convert numeric prediction to label
            predicted_label = label_encoder.inverse_transform([prediction])[0]

            # -----------------------------
            # Confidence Score (Linear SVM)
            # -----------------------------
            decision_score = model.decision_function(transformed_text)[0]

            confidence = (
                1 / (1 + np.exp(-abs(decision_score)))
            ) * 100

            confidence = round(confidence, 2)

            # Save History
            st.session_state.history.insert(
                0,
                {
                    "text": user_input,
                    "prediction": predicted_label,
                    "confidence": confidence
                }
            )

        st.write("")
        st.markdown("---")

        # =====================================
        # LOW RISK
        # =====================================

        if predicted_label == "non-suicide":

            st.success("🟢 Low Risk Detected")

            st.metric(
                "Confidence Score",
                f"{confidence}%"
            )

            st.progress(min(confidence / 100, 1.0))

            st.markdown("""
### ✅ AI Assessment

The entered text **does not contain strong indicators**
associated with suicide risk according to the trained model.

**Remember:** This is only an AI prediction and not a medical diagnosis.
""")

            st.markdown("### 💡 Positive Suggestions")

            st.info("""
✔ Stay connected with friends and family.

✔ Maintain healthy sleep and eating habits.

✔ Exercise regularly.

✔ Practice mindfulness and relaxation.

✔ Continue engaging in hobbies and activities you enjoy.
""")

        # =====================================
        # HIGHER RISK
        # =====================================

        else:

            st.error("🔴 Higher Risk Detected")

            st.metric(
                "Confidence Score",
                f"{confidence}%"
            )

            st.progress(min(confidence / 100, 1.0))

            st.markdown("""
### ⚠ AI Assessment

The entered text contains language that **may indicate elevated suicide risk**.

This prediction is generated by a machine learning model and **is not a clinical diagnosis**.
""")

            st.markdown("### 💙 Supportive Suggestions")

            st.warning("""
• Consider talking to someone you trust.

• Reach out to a mental health professional if you're struggling.

• If you or someone else is in immediate danger, contact your local emergency services or crisis resources right away.

• Remember that support is available and reaching out can make a difference.
""")

        st.markdown("---")

# ==========================================================
# Prediction History
# ==========================================================

if len(st.session_state.history) > 0:

    st.subheader("📜 Prediction History")

    for item in st.session_state.history[:5]:

        if item["prediction"] == "suicide":

            st.error(
                f"🔴 {item['prediction']} | Confidence: {item['confidence']}%"
            )

        else:

            st.success(
                f"🟢 {item['prediction']} | Confidence: {item['confidence']}%"
            )

# ==========================================================
# Footer
# ==========================================================

st.markdown("---")

st.markdown(
"""
<center>

Made with ❤️ using

<b>Python | Streamlit | Scikit-Learn | Machine Learning</b>

<br><br>

<i>For educational purposes only.</i>

</center>
""",
unsafe_allow_html=True
)