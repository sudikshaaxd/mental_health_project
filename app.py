import streamlit as st
import pandas as pd
import numpy as np
import joblib

# -----------------
# Load the model
# -----------------
model = joblib.load("model.pkl")

# -----------------
# Login credentials
# -----------------
USER_CREDENTIALS = {
    "admin": "password123",  # Change to your own
    "user": "1234"
}

# -----------------
# Login function
# -----------------
def login():
    st.title("🔐 Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["logged_in"] = True
            st.success("✅ Login Successful!")
        else:
            st.error("❌ Invalid Username or Password")

# -----------------
# Prediction function
# -----------------
def predict_risk(input_data):
    # Convert to DataFrame
    df = pd.DataFrame([input_data])
    probability = model.predict_proba(df)[0][1]  # Probability of positive class
    return round(probability * 100, 2)  # Convert to %

# -----------------
# Main app after login
# -----------------
def main_app():
    st.title("🧠 Mental Health Risk Prediction")

    # Example input fields (update according to your dataset features)
    age = st.number_input("Age", min_value=10, max_value=100, value=25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    work_interfere = st.selectbox("Work Interference", ["Never", "Rarely", "Sometimes", "Often"])

    if st.button("Predict"):
        input_data = {
            "Age": age,
            "Gender": gender,
            "work_interfere": work_interfere
        }
        risk_percent = predict_risk(input_data)
        st.info(f"📝 Predicted Risk: **{risk_percent}%**")
        if risk_percent >= 70:
            st.error("⚠ High Risk — Seek support and take care of your mental health.")
        elif risk_percent >= 40:
            st.warning("⚠ Moderate Risk — Monitor your mental health regularly.")
        else:
            st.success("✅ Low Risk — Keep maintaining good mental health.")

# -----------------
# Run app
# -----------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
else:
    main_app()
