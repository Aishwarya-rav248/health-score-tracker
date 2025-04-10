import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="HealthPredict Dashboard", layout="wide")

# ---------- CUSTOM CSS ----------
st.markdown("""
    <style>
        html, body, .main {
            background-color: #f4f7ff;
        }
        [data-testid="stSidebar"] {
            background-color: #ffffff;
            padding-top: 2rem;
            border-right: 1px solid #e1e4ed;
        }
        .title-section {
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 2rem;
            color: #1e1e1e;
        }
        .card {
            padding: 1.5rem;
            border-radius: 16px;
            background-color: #ffffff;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            margin-bottom: 1.5rem;
        }
        .card h4 {
            font-size: 20px;
            color: #333;
            margin-bottom: 1rem;
        }
        .card p {
            margin: 0.5rem 0;
            color: #444;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- LOGIN PAGE ----------
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
            st.experimental_rerun()
        else:
            st.error("Invalid Patient ID")

# ---------- DASHBOARD PAGE ----------
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
    risk_level = str(latest.get("Risk_Level", "")).lower()

    st.sidebar.title("HealthPredict")
    st.sidebar.success(f"Patient ID: {patient_id}")

    page_option = st.sidebar.radio("Select Section", ["Overview", "Visit History"])

    if page_option == "Overview":
        st.markdown("<div class='title-section'>Overview</div>", unsafe_allow_html=True)

        # ---------- ROW 1: Info + Metrics ----------
        row1_col1, row1_col2 = st.columns(2)

        with row1_col1:
            st.markdown(f"""
                <div class='card'>
                    <h4>🧍 Patient Info</h4>
                    <p><strong>Patient ID:</strong> {patient_id}</p>
                    <p><strong>Height:</strong> {latest.get("Height_cm", "N/A")} cm</p>
                    <p><strong>Weight:</strong> {latest.get("Weight_kg", "N/A")} kg</p>
                    <p><strong>Smoking Status:</strong> {latest.get("Smoking_Status", "N/A")}</p>
                </div>
            """, unsafe_allow_html=True)

        with row1_col2:
            st.markdown(f"""
                <div class='card'>
                    <h4>🧾 Health Metrics</h4>
                </div>
            """, unsafe_allow_html=True)
            st.metric("BMI", latest.get("BMI", "N/A"))
            st.metric("Blood Pressure", f"{latest.get('Systolic_BP', 'N/A')}/{latest.get('Diastolic_BP', 'N/A')}")
            st.metric("Heart Rate", latest.get("Heart_Rate", "N/A"))
            st.metric("Risk Level", latest.get("Risk_Level", "N/A"))

        # ---------- ROW 2: Gauge Chart ----------
        st.markdown("<div class='card'><h4>📊 Health Score</h4>", unsafe_allow_html=True)

        # Determine gauge color based on score or risk
        if health_score >= 85 or "low" in risk_level:
            gauge_color = "green"
        elif health_score >= 75 or "medium" in risk_level:
            gauge_color = "orange"
        else:
            gauge_color = "red"

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=health_score,
            title={'text': "Health Score", 'font': {'size': 20}},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': gauge_color},
                'bgcolor': "white",
                'steps': [
                    {'range': [0, 100], 'color': gauge_color}
                ]
            }
        ))

        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # ---------- ROW 3: Preventive Measures ----------
        with st.container():
            st.markdown(f"""
                <div class='card'>
                    <h4>🛡️ Preventive Measures</h4>
            """, unsafe_allow_html=True)

            bmi = latest.get("BMI", None)
            heart_rate = latest.get("Heart_Rate", None)
            systolic_bp = latest.get("Systolic_BP", None)

            if pd.notna(bmi):
                st.write(f"1. BMI Optimization (BMI: {bmi}) – Focus on balanced diet & exercise.")
            if pd.notna(heart_rate) and heart_rate > 80:
                st.write(f"2. Heart Rate Management ({heart_rate} bpm) – Practice stress reduction techniques.")
            if pd.notna(systolic_bp) and systolic_bp > 130:
                st.write(f"3. Blood Pressure Monitoring ({systolic_bp} mm Hg) – Limit salt intake, regular workouts.")
            st.write("4. Regular Checkups – Monitor sugar, cholesterol, maintain healthy habits.")

            st.markdown("</div>", unsafe_allow_html=True)

    elif page_option == "Visit History":
        st.title("📖 Visit History")
        trend_df = patient_df[["date", "Health_Score"]].dropna()
        trend_df["date"] = pd.to_datetime(trend_df["date"])

        if not trend_df.empty:
            st.subheader("📈 Health Score Over Time")
            st.line_chart(trend_df.set_index("date"))
        else:
            st.warning("No Health Score data available.")

        st.markdown("---")
        st.subheader("🕒 Health History Timeline")

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

    st.markdown("---")
    if st.button("🔙 Back to Login"):
        st.session_state.logged_in = False
        st.session_state.patient_id = ""
        st.rerun()

# ---------- MAIN ----------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.patient_id = ""

if st.session_state.logged_in:
    show_dashboard_page(st.session_state.patient_id)
else:
    show_login_page()
