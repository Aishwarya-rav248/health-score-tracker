
import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go


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
        st.warning("Data file not found.")
        return

    df = pd.read_csv(data_path)
    patient_df = df[df["patient"].astype(str) == patient_id].sort_values("date")

    if patient_df.empty:
        st.warning("No data found for the selected Patient ID.")
        return

    latest = patient_df.iloc[-1]
    health_score = latest.get("Health_Score", None)

    # ---------- SIDEBAR ----------
    st.sidebar.title("HealthPredict")
    st.sidebar.success(f"Patient ID:\n{patient_id}")

    page_option = st.sidebar.radio(
        "Select Section",
        ["Overview", "Visit History"],
        key="dashboard_section"
    )

    # ---------- OVERVIEW PAGE ----------
    if page_option == "Overview":
        st.title("Patient Details")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
                <div style='padding: 1rem; background-color: #262730; border-radius: 10px; color: #ddd;'>
                    <h3 style='margin-bottom: 0;'>Patient:</h3>
                    <p style='margin-top: 0;'>{latest.get('patient', 'N/A')}</p>
                    <p><strong>Smoking Status:</strong> {latest.get('Smoking_Status', 'N/A')}</p>
                    <p><strong>Health Score:</strong> {health_score} / 100</p>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.metric("BMI", latest.get("BMI", "N/A"))
            st.metric("Blood Pressure", f"{latest.get('Systolic_BP', 'N/A')}/{latest.get('Diastolic_BP', 'N/A')}")
            st.metric("Heart Rate", latest.get("Heart_Rate", "N/A"))
            st.metric("Risk Level", latest.get("Risk_Level", "N/A"))

        if pd.notna(health_score):
            st.subheader("Health Score")
            gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=health_score,
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "green" if health_score >= 85 else "orange" if health_score >= 75 else "red"},
                    'steps': [
                        {'range': [0, 74], 'color': "red"},
                        {'range': [75, 84], 'color': "orange"},
                        {'range': [85, 100], 'color': "green"}
                    ]
                },
                domain={'x': [0, 1], 'y': [0, 1]}
            ))
            st.plotly_chart(gauge)

            if health_score >= 85:
                st.success("Excellent")
            elif health_score >= 75:
                st.warning("Needs Improvement")
            else:
                st.error("Unhealthy: Immediate Action Required!")

            st.subheader("Preventive Measures")
            bmi = latest.get("BMI", None)
            heart_rate = latest.get("Heart_Rate", None)
            systolic_bp = latest.get("Systolic_BP", None)

            if pd.notna(bmi):
                st.write(f"1. BMI Optimization (BMI: {bmi}) – Focus on balanced diet & exercise.")
            if pd.notna(heart_rate) and heart_rate > 80:
                st.write(f"2. Heart Rate Management ({heart_rate} bpm) – Practice stress reduction techniques.")
            if pd.notna(systolic_bp) and systolic_bp > 130:
                st.write(f"3. Blood Pressure Monitoring ({systolic_bp} mm Hg) – Limit salt intake, exercise regularly.")
            st.write("4. Regular Checkups – Monitor blood sugar, cholesterol, and maintain healthy routines.")

    # ---------- VISIT HISTORY PAGE ----------
    elif page_option == "Visit History":
        st.title("Visit History")

        st.subheader("Health Score Over Time")
        trend_df = patient_df[["date", "Health_Score"]].dropna()
        trend_df["date"] = pd.to_datetime(trend_df["date"])
        st.line_chart(trend_df.set_index("date"))

        st.markdown("---")
        st.subheader("Health History Timeline")
        for _, row in patient_df.iterrows():
            with st.expander(f"Visit on {row['date']}"):
                st.write(f"**Height:** {row.get('Height_cm', 'N/A')} cm")
                st.write(f"**Weight:** {row.get('Weight_kg', 'N/A')} kg")
                st.write(f"**BMI:** {row.get('BMI', 'N/A')}")
                st.write(f"**Blood Pressure:** {row.get('Systolic_BP', 'N/A')}/{row.get('Diastolic_BP', 'N/A')}")
                st.write(f"**Heart Rate:** {row.get('Heart_Rate', 'N/A')}")
                st.write(f"**Smoking Status:** {row.get('Smoking_Status', 'N/A')}")
                st.write(f"**Health Score:** {row.get('Health_Score', 'N/A')}")

                risk = str(row.get('Risk_Level', 'N/A')).lower()
                if 'high' in risk:
                    st.error(f"**Risk Level:** {risk.capitalize()}")
                elif 'medium' in risk:
                    st.warning(f"**Risk Level:** {risk.capitalize()}")
                elif 'low' in risk:
                    st.success(f"**Risk Level:** {risk.capitalize()}")
                else:
                    st.info(f"**Risk Level:** {risk.capitalize()}")

    # ---------- BACK TO LOGIN ----------
    st.markdown("---")
    if st.button("🔙 Back to Login"):
        st.session_state.logged_in = False
        st.session_state.patient_id = ""
        st.session_state.page = 'login'
        st.rerun()

# ----------- MAIN -----------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.patient_id = ""

if st.session_state.logged_in:
    show_dashboard_page(st.session_state.patient_id)
else:
    show_login_page()


