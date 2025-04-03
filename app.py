import streamlit as st
import pandas as pd


# Load model and data
df = pd.read_csv("20 patients final final.csv")

import cloudpickle
with open("trained_rf_model_py312.pkl", "rb") as f:
    model = cloudpickle.load(f)

# Health score calculation function
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

# Sidebar login
st.sidebar.title("Patient Login")
patient_ids = df["Short_Patient_ID"].unique()
selected_id = st.sidebar.selectbox("Select Short Patient ID", patient_ids)

# Main dashboard
st.title("🏥 Patient Health Dashboard")

patient_data = df[df["Short_Patient_ID"] == selected_id].iloc[0]
calculated_score = calculate_health_score(patient_data)

features = ['Height_cm', 'BMI', 'Weight_kg', 'Diastolic_BP', 'Heart_Rate',
            'Systolic_BP', 'Smoking_Status', 'Diabetes', 'Hyperlipidemia', 'Heart_Disease']
input_data = patient_data[features].values.reshape(1, -1)
predicted_score = model.predict(input_data)[0]


# Show vitals
st.subheader("📋 Patient Vitals")
st.dataframe(patient_data[features].to_frame().T)

# Health scores
st.subheader("💡 Health Score Summary")
st.metric(label="Calculated Score", value=round(calculated_score, 2))
st.metric(label="Predicted Score", value=round(predicted_score, 2))

# Score progress
st.progress(min(1.0, calculated_score / 100))
st.write("Above is your calculated health score (max: 100).")

# Simple risk flag
if calculated_score < 70 or predicted_score < 70:
    st.warning("⚠️ Health risk detected. Consider lifestyle changes and medical consultation.")
