import streamlit as st
import pandas as pd
import cloudpickle

# -----------------------------
# ✅ Load the model and scaler
# -----------------------------
try:
    with open("heart_disease_classifier.pkl", "rb") as f:
        model_bundle = cloudpickle.load(f)
        model = model_bundle["model"]
        scaler = model_bundle["scaler"]
        features = model_bundle["features"]
except Exception as e:
    model = None
    st.error(f"❌ Model loading failed: {e}")

# -----------------------------
# ✅ Load the dataset
# -----------------------------
df = pd.read_csv("20 patients final final.csv")

# -----------------------------
# ✅ Define health score function
# -----------------------------
def calculate_health_score(row):
    score = 100
    score -= row['BMI'] * 0.3
    score -= row['Systolic_BP'] * 0.2
    score -= row['Diastolic_BP'] * 0.1
    score -= row['Heart_Rate'] * 0.1
    score -= row['Smoking_Status'] * 5
    if row['Heart_Disease'] == 1:
        score -= 15
    if row['Diabetes'] == 1:
        score -= 12
    if row['Weight_kg'] > 100:
        score -= 10
    if row['Hyperlipidemia'] == 1:
        score -= 12
    return score

# -----------------------------
# 🔐 Login Page
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if st.session_state.page == "login":
    st.title("🔐 Patient Login")
    patient_ids = df["Short_Patient_ID"].unique()
    selected_id = st.selectbox("Select Short Patient ID", patient_ids)
    if st.button("Login"):
        st.session_state.selected_id = selected_id
        st.session_state.page = "dashboard"
        st.experimental_rerun()

# -----------------------------
# 📊 Dashboard Page
# -----------------------------
elif st.session_state.page == "dashboard":
    st.title("🏥 Patient Health Dashboard")
    patient_id = st.session_state.selected_id
    patient_data = df[df["Short_Patient_ID"] == patient_id].iloc[0]

    st.subheader("📋 Patient Health Metrics")
    st.dataframe(patient_data.to_frame().T)

    # Health Score
    calculated_score = calculate_health_score(patient_data)
    st.subheader("💡 Calculated Health Score")
    st.metric("Health Score", round(calculated_score, 2))
    st.progress(min(1.0, calculated_score / 100))

    # Predict Heart Disease Risk
    if model is not None:
        input_data = patient_data[features].values.reshape(1, -1)
        input_scaled = scaler.transform(input_data)
        predicted_risk = model.predict(input_scaled)[0]

        st.subheader("❤️ Heart Disease Risk Prediction")
        if predicted_risk == 1:
            st.error("⚠️ High Risk of Heart Disease Detected!")
        else:
            st.success("✅ No Heart Disease Risk Detected.")

    # Back button
    if st.button("Logout"):
        st.session_state.page = "login"
        st.experimental_rerun()
