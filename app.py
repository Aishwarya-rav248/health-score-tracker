import streamlit as st
import pandas as pd
import cloudpickle

# -----------------------------
# ✅ Load the trained model safely
# -----------------------------
try:
    with open("trained_rf_model_py312.pkl", "rb") as f:
        model = cloudpickle.load(f)
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
# 🔐 Sidebar Login
# -----------------------------
st.sidebar.title("Patient Login")
patient_ids = df["Short_Patient_ID"].unique()
selected_id = st.sidebar.selectbox("Select Short Patient ID", patient_ids)

# -----------------------------
# 📊 Main Dashboard
# -----------------------------
st.title("🏥 Patient Health Dashboard")
features = ['Height_cm', 'BMI', 'Weight_kg', 'Diastolic_BP', 'Heart_Rate',
            'Systolic_BP', 'Smoking_Status', 'Diabetes', 'Hyperlipidemia', 'Heart_Disease']

patient_data = df[df["Short_Patient_ID"] == selected_id].iloc[0]
calculated_score = calculate_health_score(patient_data)

# Show Vitals
st.subheader("📋 Patient Vitals")
st.dataframe(patient_data[features].to_frame().T)

# Show Calculated Score
st.subheader("💡 Health Score Summary")
st.metric(label="Calculated Score", value=round(calculated_score, 2))

# Safe model prediction
missing = [col for col in features if col not in patient_data]
if missing:
    st.error(f"Missing columns in patient data: {missing}")
else:
    input_data = patient_data[features].values.reshape(1, -1)
    if model is not None:
        predicted_score = model.predict(input_data)[0]
        st.metric("Predicted Score", round(predicted_score, 2))
        st.progress(min(1.0, calculated_score / 100))
    else:
        st.error("❌ Model not loaded. Please recheck your .pkl file or environment.")
