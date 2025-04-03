
import streamlit as st
import pandas as pd

def show_login_page():
    st.title("Welcome to HealthPredict")
    st.subheader("Login with Patient ID")
    
    patient_id = st.text_input("Enter Patient ID")

    if st.button("Login"):
        df = pd.read_csv("data/selected_20_final_patients.csv")
        if patient_id in df["patient_id"].values:
            st.session_state.logged_in = True
            st.session_state.patient_id = patient_id
            st.experimental_rerun()
        else:
            st.error("Invalid Patient ID")
