import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Health Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("selected_20_final_patients.csv")

df = load_data()

# ------------------ SESSION SETUP ------------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.patient_id = ""

# ------------------ LOGIN PAGE ------------------
def show_login():
    st.title("Welcome to HealthPredict 🩺")
    st.subheader("Login with your Patient ID")
    patient_id = st.text_input("Enter Patient ID")

    if st.button("Login"):
        if patient_id in df["patient"].astype(str).values:
            st.session_state.logged_in = True
            st.session_state.patient_id = patient_id
            st.rerun()
        else:
            st.error("Invalid Patient ID. Please try again.")

# ------------------ DASHBOARD PAGE ------------------
def show_dashboard(patient_id):
    patient_df = df[df["patient"].astype(str) == patient_id].sort_values("date")
    
    if patient_df.empty:
        st.error("No data available for this patient.")
        return

    latest = patient_df.iloc[-1]

    # ---------- Top Section ----------
    col1, col2, col3 = st.columns([1.5, 1.5, 2])

    # --- Patient Info Card ---
    with col1:
        st.markdown("### 👤 Patient Info")
        st.markdown(f"**Patient ID:** {patient_id}")
        st.markdown(f"**Date:** {latest['date']}")
        st.markdown(f"**Height:** {latest['Height_cm']} cm")
        st.markdown(f"**Weight:** {latest['Weight_kg']} kg")
        st.markdown(f"**Smoking Status:** {latest['Smoking_Status']}")

    # --- Health Metrics Card ---
    with col2:
        st.markdown("### 📊 Health Metrics")
        st.metric("BMI", latest["BMI"])
        st.metric("Blood Pressure", f"{latest['Systolic_BP']}/{latest['Diastolic_BP']}")
        st.metric("Heart Rate", latest["Heart_Rate"])
        st.metric("Risk Level", latest["Risk_Level"])

    # --- Health Score Donut Chart ---
    with col3:
        st.markdown("### 🧭 Health Score")
        health_score = latest["Health_Score"]
        risk_level = latest["Risk_Level"].lower()
        color = "#4caf50" if "low" in risk_level else "#ffa94d" if "medium" in risk_level else "#ff4d4d"

        fig = go.Figure(data=[go.Pie(
            values=[health_score, 100 - health_score],
            hole=0.65,
            marker_colors=[color, "#f0f2f6"],
            textinfo='none'
        )])
        fig.update_layout(
            showlegend=False,
            height=260,
            annotations=[dict(
                text=f"<b>{health_score}</b><br>Score",
                font_size=18,
                showarrow=False
            )],
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    # ---------- Health Trend ----------
    st.markdown("### 📈 Health Score Over Time")
    trend_df = patient_df[["date", "Health_Score"]].copy()
    trend_df["date"] = pd.to_datetime(trend_df["date"])
    st.line_chart(trend_df.set_index("date"))

    # ---------- Visit History ----------
    st.markdown("### 📅 Visit History")
    for _, row in patient_df.iterrows():
        with st.expander(f"Visit on {row['date']}"):
            st.write(f"**Height:** {row['Height_cm']} cm")
            st.write(f"**Weight:** {row['Weight_kg']} kg")
            st.write(f"**BMI:** {row['BMI']}")
            st.write(f"**Blood Pressure:** {row['Systolic_BP']}/{row['Diastolic_BP']}")
            st.write(f"**Heart Rate:** {row['Heart_Rate']}")
            st.write(f"**Smoking Status:** {row['Smoking_Status']}")
            st.write(f"**Health Score:** {row['Health_Score']}")
            st.write(f"**Risk Level:** {row['Risk_Level']}")

    # ---------- BACK BUTTON ----------
    st.markdown("---")
    if st.button("🔙 Back to Login"):
        st.session_state.logged_in = False
        st.session_state.patient_id = ""
        st.rerun()

# ------------------ MAIN ------------------
if st.session_state.logged_in:
    show_dashboard(st.session_state.patient_id)
else:
    show_login()
