
import streamlit as st
import pandas as pd
import os

def show_dashboard_page(patient_id):
    data_path = "data/selected_20_final_patients.csv"
    if not os.path.isfile(data_path):
        st.warning("Patient data file not found. Please upload 'selected_20_final_patients.csv' in the data/ folder.")
        return

    df = pd.read_csv(data_path)
    patient_df = df[df["patient_id"] == patient_id].sort_values("visit_date")

    if patient_df.empty:
        st.warning("No data found for the selected Patient ID.")
        return

    latest = patient_df.iloc[-1]

    st.sidebar.title("HealthPredict")
    st.sidebar.success(f"Patient ID: {patient_id}")

    st.title("Patient Details")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"{latest['first_name']} {latest['last_name']}")
        st.markdown(f"**Age:** {latest['age']}  \n**Gender:** {latest['gender']}")
        st.markdown(f"**Smoking Status:** {latest['smoking_status']}")
        st.markdown(f"**Health Score:** {latest['health_score']} / 100")

    with col2:
        st.metric("BMI", latest["bmi"])
        st.metric("Blood Pressure", latest["bp"])
        st.metric("Heart Rate", latest["heart_rate"])
        st.metric("Risk Score", latest["risk_score"])

    st.markdown("---")
    st.subheader("Health History Timeline")

    for _, row in patient_df.iterrows():
        with st.expander(f"Visit on {row['visit_date']}"):
            st.write(f"**Weight:** {row['weight']} kg")
            st.write(f"**BMI:** {row['bmi']}")
            st.write(f"**Blood Pressure:** {row['bp']}")
            st.write(f"**Heart Rate:** {row['heart_rate']}")
            st.write(f"**Health Score:** {row['health_score']}")
