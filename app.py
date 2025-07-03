# === Import Required Libraries ===
import pandas as pd
import numpy as np
import joblib
import streamlit as st
import plotly.express as px
import re

# === Page Configuration ===
st.set_page_config(
    page_title="💧 Water Pollutants Predictor",
    layout="centered",
    page_icon="💧"
)

# === Load Model and Feature Columns ===
model = joblib.load("pollution_model.pkl")
model_cols = joblib.load("model_columns.pkl")

# === Title and Description ===
st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color: navy;'>💧 Water Pollutants Predictor</h1>
        <p style='font-size: 17px;'>Predict water pollutant levels and classify safety based on environmental standards.</p>
    </div>
    <hr style='border: 1px solid #ddd;' />
""", unsafe_allow_html=True)

# === Input Form ===
with st.form("input_form"):
    st.subheader("📥 Enter Parameters")
    col1, col2 = st.columns(2)
    with col1:
        year_input = st.number_input("🌐 Year", min_value=2000, max_value=2100, value=2022, step=1)
    with col2:
        station_id = st.text_input("🏭 Station ID", value='1')
    submitted = st.form_submit_button("🔍 Predict")

# === Prediction Logic ===
if submitted:
    if not station_id.strip():
        st.warning("⚠️ Please enter a valid Station ID.")
    else:
        # --- Input Preprocessing ---
        input_df = pd.DataFrame({'year': [year_input], 'id': [station_id]})
        input_encoded = pd.get_dummies(input_df, columns=['id'])
        for col in model_cols:
            if col not in input_encoded.columns:
                input_encoded[col] = 0
        input_encoded = input_encoded[model_cols]

        # --- Predict Pollutant Levels ---
        predicted_pollutants = model.predict(input_encoded)[0]
        pollutants = ['NH4', 'BSK5', 'Suspended', 'O2', 'NO3', 'NO2', 'SO4', 'PO4', 'CL']
        units = ['mg/L'] * len(pollutants)

        # --- Define Safety Thresholds (WHO/CPCB) ---
        thresholds = {
            'NH4': 1.5,
            'BSK5': 5.0,
            'Suspended': 10,
            'O2': 4.0,
            'NO3': 45,
            'NO2': 3,
            'SO4': 250,
            'PO4': 0.5,
            'CL': 250
        }

        # --- Classify Safety ---
        classification = []
        for pollutant, value in zip(pollutants, predicted_pollutants):
            limit = thresholds[pollutant]
            if pollutant == 'O2':
                status = "Safe ✅" if value >= limit else "Unsafe ❌"
            else:
                status = "Safe ✅" if value <= limit else "Unsafe ❌"
            classification.append(status)

        # --- Create Results DataFrame ---
        results_df = pd.DataFrame({
            "Pollutant": pollutants,
            "Predicted Value (mg/L)": [round(val, 2) for val in predicted_pollutants],
            "Unit": units,
            "Water Safety Status": classification
        })

        # --- Success Info ---
        st.success(f"✅ Prediction completed for Station ID: **{station_id}**, Year: **{year_input}**")

        # === Results Table ===
        st.markdown("### 🧪 Predicted Pollutant Levels with Safety Classification")
        st.dataframe(results_df.style.format({"Predicted Value (mg/L)": "{:.2f}"}), use_container_width=True)

        # === Visualization ===
        st.markdown("### 📊 Visualization")
        fig = px.bar(
            results_df,
            x="Pollutant",
            y="Predicted Value (mg/L)",
            color="Water Safety Status",
            text="Predicted Value (mg/L)",
            title=f"Pollutant Levels for Station '{station_id}' in {year_input}",
            height=500
        )
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(
            yaxis_title="Concentration (mg/L)",
            xaxis_title="Pollutant",
            yaxis_range=[0, max(results_df["Predicted Value (mg/L)"]) * 1.25],
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)

        # === Download Button ===
        st.markdown("### 📥 Download Results")
        safe_station_id = re.sub(r'\W+', '_', station_id)
        csv = results_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download as CSV",
            data=csv,
            file_name=f"predicted_pollutants_{safe_station_id}_{year_input}.csv",
            mime="text/csv"
        )
