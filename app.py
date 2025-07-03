# === Import Required Libraries ===
import pandas as pd
import numpy as np
import joblib
import streamlit as st
import plotly.express as px
import re

# === Page Config ===
st.set_page_config(
    page_title="💧 Water Pollutants Predictor",
    layout="centered",
    page_icon="💧"
)

# === Load Model and Feature Columns ===
model = joblib.load("pollution_model.pkl")
model_cols = joblib.load("model_columns.pkl")

# === Header ===
st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color: navy;'>💧 Water Pollutants Predictor</h1>
        <p style='font-size: 17px;'>Predict the concentration of major water pollutants using machine learning.</p>
    </div>
    <hr style='border: 1px solid #ddd;' />
""", unsafe_allow_html=True)

# === Input Form ===
with st.form("input_form"):
    st.subheader("📥 Enter Parameters Below")
    col1, col2 = st.columns(2)
    with col1:
        year_input = st.number_input("🌐 Year", min_value=2000, max_value=2100, value=2022, step=1)
    with col2:
        station_id = st.text_input("🏭 Station ID", value='1')
    submitted = st.form_submit_button("🔍 Predict Pollutants")

# === Prediction Logic ===
if submitted:
    if not station_id.strip():
        st.warning("⚠️ Please enter a valid Station ID.")
    else:
        # --- Input Preparation ---
        input_df = pd.DataFrame({'year': [year_input], 'id': [station_id]})
        input_encoded = pd.get_dummies(input_df, columns=['id'])

        for col in model_cols:
            if col not in input_encoded.columns:
                input_encoded[col] = 0
        input_encoded = input_encoded[model_cols]

        # --- Model Prediction ---
        predicted_pollutants = model.predict(input_encoded)[0]
        pollutants = ['NH4', 'BSK5', 'Suspended', 'O2', 'NO3', 'NO2', 'SO4', 'PO4', 'CL']
        units = ['mg/L'] * len(pollutants)

        # --- DataFrame for Output ---
        results_df = pd.DataFrame({
            "Pollutant": pollutants,
            "Predicted Value": [round(val, 2) for val in predicted_pollutants],
            "Unit": units
        })

        # --- Success Message ---
        st.success(f"✅ Prediction generated for Station ID: **{station_id}**, Year: **{year_input}**")

        # === Display Results Table ===
        st.markdown("### 🧪 Predicted Pollutant Levels")
        st.dataframe(results_df.style.format({"Predicted Value": "{:.2f}"}), use_container_width=True)

        # === Chart Visualization ===
        st.markdown("### 📊 Visual Comparison of Predicted Values")
        fig = px.bar(
            results_df,
            x="Pollutant",
            y="Predicted Value",
            text="Predicted Value",
            color="Pollutant",
            labels={"Predicted Value": "Concentration (mg/L)"},
            title=f"Pollutant Concentrations for Station '{station_id}' in {year_input}",
            height=500
        )
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(
            yaxis_range=[0, max(results_df["Predicted Value"]) * 1.25],
            xaxis_title="Pollutant",
            yaxis_title="Predicted Concentration (mg/L)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)

        # === Download Option ===
        st.markdown("### 📥 Download Predicted Results")
        safe_station_id = re.sub(r'\W+', '_', station_id)
        csv = results_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download as CSV",
            data=csv,
            file_name=f"predicted_pollutants_{safe_station_id}_{year_input}.csv",
            mime="text/csv"
        )


