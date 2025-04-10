import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Health Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("selected_20_final_patients.csv")

df = load_data()

# Sidebar
st.sidebar.title("🩺 Health Dashboard")
selected_patient = st.sidebar.selectbox("Choose Patient", df["patient"].unique())

# Filter data for selected patient
patient_df = df[df["patient"] == selected_patient].sort_values("date")
latest = patient_df.iloc[-1]

# ---------- Top Section ----------
col1, col2, col3 = st.columns([1.5, 1.5, 2])

# --- Patient Info Card ---
with col1:
    st.markdown("### 👤 Patient Info")
    st.markdown(f"**Patient ID:** {selected_patient}")
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

# --- Health Score Gauge ---
with col3:
    st.markdown("### 🧭 Health Score")

    health_score = latest["Health_Score"]
    risk_level = latest["Risk_Level"].lower()

    # Determine gauge color
    color = "green" if "low" in risk_level else "orange" if "medium" in risk_level else "red"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=health_score,
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': color},
            'bgcolor': "white",
            'steps': [
                {'range': [0, 60], 'color': '#ff4d4d'},
                {'range': [60, 80], 'color': '#ffa94d'},
                {'range': [80, 100], 'color': '#4caf50'}
            ]
        }
    ))
    fig.update_layout(height=250, margin=dict(t=10, b=10, l=20, r=20))
    st.plotly_chart(fig, use_container_width=True)

# ---------- Trend Line ----------
st.markdown("### 📈 Health Score Over Time")
trend_df = patient_df[["date", "Health_Score"]].copy()
trend_df["date"] = pd.to_datetime(trend_df["date"])
st.line_chart(trend_df.set_index("date"))

# ---------- Visit History Timeline ----------
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
