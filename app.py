# Update app.py to read CSV from the current directory instead of a subfolder

single_app_inline_csv = """
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
            st.error("❌ Data file not found: 'selected_20_final_patients.csv'. Please upload it to the root directory.")
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


# ----------- DASHBOARD PAGE -----------
def show_dashboard_page(patient_id):
    data_path = "selected_20_final_patients.csv"
    if not os.path.isfile(data_path):
        st.warning("Patient data file not found. Please upload 'selected_20_final_patients.csv' to the root directory.")
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
        st.markdown(f"**Age:** {latest['age']}  \\n**Gender:** {latest['gender']}")
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


# ----------- MAIN -----------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.patient_id = ""

if st.session_state.logged_in:
    show_dashboard_page(st.session_state.patient_id)
else:
    show_login_page()
"""

# Save updated app.py (root CSV path)
inline_dir = "/mnt/data/health_score_single_file_inline"
os.makedirs(inline_dir, exist_ok=True)

with open(f"{inline_dir}/app.py", "w") as f:
    f.write(single_app_inline_csv)

with open(f"{inline_dir}/requirements.txt", "w") as f:
    f.write("streamlit\npandas\nplotly")

# Zip it
zip_inline_path = "/mnt/data/health_score_single_file_inline_csv.zip"
with zipfile.ZipFile(zip_inline_path, 'w') as zipf:
    for root, dirs, files in os.walk(inline_dir):
        for file in files:
            zipf.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file), os.path.join(inline_dir, '..')))

zip_inline_path
