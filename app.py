
import streamlit as st
import pandas as pd
import os

# ----------- LOGIN PAGE -----------
def show_login_page():
    st.title("Welcome to HealthPredict")
    st.subheader("Login with Patient ID")

    patient_id = st.text_input("Enter Patient ID")

    if st.button("Login"):
        data_path = "selected_20_final_patients.csv"

        if not os.path.isfile(data_path):
            st.error("❌ Data file not found: 'selected_20_final_patients.csv'. Please upload it.")
            return

        try:
            df = pd.read_csv(data_path)
        except Exception as e:
            st.error(f"Failed to read data file. Error: {str(e)}")
            return

        if patient_id in df["patient"].astype(str).values:
            st.session_state.logged_in = True
            st.session_state.patient_id = patient_id
            st.session_state.rerun = True
        else:
            st.error("Invalid Patient ID")


# ----------- DASHBOARD PAGE -----------
def show_dashboard_page(patient_id):
    data_path = "selected_20_final_patients.csv"
    if not os.path.isfile(data_path):
        st.warning("Patient data file not found. Please upload 'selected_20_final_patients.csv' to the root directory.")
        return

    df = pd.read_csv(data_path)
    st.write("Columns in your CSV:", df.columns.tolist())
    
    patient_df = df[df["patient"].astype(str) == patient_id].sort_values("date")

    if patient_df.empty:
        st.warning("No data found for the selected Patient ID.")
        return

    latest = patient_df.iloc[-1]

    st.sidebar.title("HealthPredict")
    st.sidebar.success(f"Patient ID: {patient_id}")

    st.title("Patient Details")
    col1, col2 = st.columns(2)
    col1, col2 = st.columns(2)
with col1:
    st.subheader(f"Patient: {latest.get('patient', 'N/A')}")
    st.markdown(f"**Smoking Status:** {latest.get('Smoking_Status', 'N/A')}")
    st.markdown(f"**Health Score:** {latest.get('Health_Score', 'N/A')} / 100")

with col2:
    st.metric("BMI", latest.get("BMI", "N/A"))
    st.metric("Blood Pressure", f"{latest.get('Systolic_BP', 'N/A')}/{latest.get('Diastolic_BP', 'N/A')}")
    st.metric("Heart Rate", latest.get("Heart_Rate", "N/A"))
    st.metric("Risk Level", latest.get("Risk_Level", "N/A"))


    st.markdown("---")
    st.subheader("Health History Timeline")

    for _, row in patient_df.iterrows():
        with st.expander(f"Visit on {row['date']}"):
            st.write(f"**Weight:** {row.get('weight', 'N/A')} kg")
            st.write(f"**BMI:** {row.get('bmi', 'N/A')}")
            st.write(f"**Blood Pressure:** {row.get('bp', 'N/A')}")
            st.write(f"**Heart Rate:** {row.get('heart_rate', 'N/A')}")
            st.write(f"**Health Score:** {row.get('health_score', 'N/A')}")


# ----------- MAIN -----------

# Handle rerun workaround
if st.session_state.get("rerun"):
    st.session_state.rerun = False
    st.experimental_rerun()

# Initialize login state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.patient_id = ""

# Route to the correct page
if st.session_state.logged_in:
    show_dashboard_page(st.session_state.patient_id)
else:
    show_login_page()

