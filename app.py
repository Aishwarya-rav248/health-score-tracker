
import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

@st.cache_data
def load_data():
    df = pd.read_csv("data/FINAL_20_PATIENTS.csv")
    model = joblib.load("model/heart_disease_model.pkl")
    return df, model

df, model = load_data()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("HealthPredict Login")
    patient_id = st.text_input("Enter your Patient ID:")
    if st.button("Login"):
        if patient_id in df["patient"].values:
            st.session_state.logged_in = True
            st.session_state.patient_id = patient_id
            st.experimental_rerun()
        else:
            st.error("Invalid Patient ID")
else:
    st.sidebar.title("HealthPredict")
    st.sidebar.markdown("Monitor your health metrics and risk predictions")

    st.title("Patient Dashboard")
    patient_df = df[df["patient"] == st.session_state.patient_id]

    if not patient_df.empty:
        personal_info = patient_df.iloc[0]
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Patient Information")
            st.markdown(f"**Name**: {personal_info['First Name']} {personal_info['Last Name']}")
            st.markdown(f"**Gender**: {personal_info['Gender']}")
            st.markdown(f"**DOB**: {personal_info['Date_of_Birth']}")
            st.markdown(f"**Smoking**: {personal_info['Smoking_Status']}")
        with col2:
            st.subheader("Health Score")
            score = int(personal_info['Health_Score'])
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "green" if score > 80 else "orange" if score > 60 else "red"},
                    'steps': [
                        {'range': [0, 60], 'color': "red"},
                        {'range': [60, 80], 'color': "orange"},
                        {'range': [80, 100], 'color': "green"},
                    ]
                }
            ))
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Visit-wise Health History")
        history = patient_df.sort_values(by="Date")
        for _, visit in history.iterrows():
            st.markdown(f"### {pd.to_datetime(visit['Date']).strftime('%B %d, %Y')}")
            st.markdown(f"- **Weight**: {visit['Weight']} kg")
            st.markdown(f"- **BMI**: {visit['BMI']}")
            st.markdown(f"- **Blood Pressure**: {visit['Systolic_BP']}/{visit['Diastolic_BP']} mmHg")
            st.markdown(f"- **Heart Rate**: {visit['Heart_Rate']} bpm")
            st.markdown(f"- **Health Score**: {int(visit['Health_Score'])}")

        st.subheader("Heart Disease Risk Prediction")
        features = ['BMI', 'Systolic_BP', 'Diastolic_BP', 'Heart_Rate']
        latest = patient_df.sort_values('Date').iloc[-1]
        input_features = latest[features].values.reshape(1, -1)
        prediction = model.predict(input_features)[0]
        st.success(f"Predicted Risk: **{'Yes' if prediction else 'No'}**")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()
