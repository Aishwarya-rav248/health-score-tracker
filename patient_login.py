
import streamlit as st
import pandas as pd
import os

def show_login_page():
    st.title("Welcome to HealthPredict")
    st.subheader("Login with Patient ID")

    patient_id = st.text_input("Enter Patient ID")

    if st.button("Login"):
        data_path = "data/selected_20_final_patients.csv"

        # Check if file exists before attempting to read it
        if not os.path.isfile(data_path):
            st.error("❌ Data file not found: 'data/selected_20_final_patients.csv'. Please upload it.")
            return

        try:
            df = pd.read_csv(data_path)
        except Exception as e:
            st.error(f"Failed to read data file. Error: {str(e)}")
            return

        if patient_id in df["patient_id"].values:
            st.session_state.logged_in = True
            st.session_state.patient_id = patient_id
            st.experimental_rerun()
        else:
            st.error("Invalid Patient ID")
