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
    layout="wide",
    page_icon="💧"
)

# === Custom Styling ===
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #f0f4ff, #e6f7ff);
    font-family: 'Segoe UI', sans-serif;
}
h1, h2, h3 {
    color: #002b5c;
}
.stApp {
    background-color: #f6fbff;
}
table {
    font-size: 14px;
    border-collapse: collapse;
}
.sidebar-table th, .sidebar-table td {
    padding: 6px 8px;
    text-align: left;
}
.sidebar-table tr:nth-child(even) {background-color: #f2f2f2;}
.stButton>button {
    background-color: #0077cc;
    color: white;
    font-weight: bold;
    border-radius: 8px;
}
.stButton>button:hover {
    background-color: #005fa3;
}
</style>
""", unsafe_allow_html=True)

# === Styled Header Section ===
st.markdown("""
<div style='text-align: center; padding: 1rem; background: #eaf4ff; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);'>
    <h1 style='color: navy; font-weight: bold;'>💧 Water Pollutants Predictor</h1>
    <p style='font-size: 17px; color: #003366;'>Predict water pollutant levels and classify safety based on environmental standards.</p>
</div>
""", unsafe_allow_html=True)

# === Sidebar Threshold Table ===
st.sidebar.title("📘 Info Panel")
st.sidebar.markdown("### 🧾 Pollutant Safety Thresholds")
st.sidebar.markdown("""
<table class="sidebar-table">
<tr><th>Pollutant</th><th>Limit</th></tr>
<tr><td>NH₄</td><td>&lt; 1.5 mg/L</td></tr>
<tr><td>BSK5</td><td>&lt; 5.0 mg/L</td></tr>
<tr><td>Suspended</td><td>&lt; 10 mg/L</td></tr>
<tr><td>O₂</td><td>&gt; 4.0 mg/L</td></tr>
<tr><td>NO₃</td><td>&lt; 45 mg/L</td></tr>
<tr><td>NO₂</td><td>&lt; 3 mg/L</td></tr>
<tr><td>SO₄</td><td>&lt; 250 mg/L</td></tr>
<tr><td>PO₄</td><td>&lt; 0.5 mg/L</td></tr>
<tr><td>Cl⁻</td><td>&lt; 250 mg/L</td></tr>
</table>
""", unsafe_allow_html=True)

# === Load Model and Columns ===
model = joblib.load("pollution_model.pkl")
model_cols = joblib.load("model_columns.pkl")

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
        input_df = pd.DataFrame({'year': [year_input], 'id': [station_id]})
        input_encoded = pd.get_dummies(input_df, columns=['id'])
        for col in model_cols:
            if col not in input_encoded.columns:
                input_encoded[col] = 0
        input_encoded = input_encoded[model_cols]

        predicted_pollutants = model.predict(input_encoded)[0]
        pollutants = ['NH4', 'BSK5', 'Suspended', 'O2', 'NO3', 'NO2', 'SO4', 'PO4', 'CL']
        units = ['mg/L'] * len(pollutants)

        thresholds = {
            'NH4': 1.5, 'BSK5': 5.0, 'Suspended': 10,
            'O2': 4.0, 'NO3': 45, 'NO2': 3,
            'SO4': 250, 'PO4': 0.5, 'CL': 250
        }

        classification = []
        for pollutant, value in zip(pollutants, predicted_pollutants):
            limit = thresholds[pollutant]
            if pollutant == 'O2':
                status = "Safe ✅" if value >= limit else "Unsafe ❌"
            else:
                status = "Safe ✅" if value <= limit else "Unsafe ❌"
            classification.append(status)

        results_df = pd.DataFrame({
            "Pollutant": pollutants,
            "Predicted Value (mg/L)": [round(val, 2) for val in predicted_pollutants],
            "Unit": units,
            "Water Safety Status": classification
        })

        st.success(f"✅ Prediction completed for Station ID: **{station_id}**, Year: **{year_input}**")

        # Summary
        safe_count = classification.count("Safe ✅")
        unsafe_count = classification.count("Unsafe ❌")
        col1, col2 = st.columns(2)
        col1.success(f"✅ Safe Parameters: {safe_count}")
        col2.error(f"❌ Unsafe Parameters: {unsafe_count}")

        # Table
        st.markdown("### 🧪 Predicted Pollutant Levels")
        st.dataframe(results_df.style.format({"Predicted Value (mg/L)": "{:.2f}"}), use_container_width=True)

        # Chart
        st.markdown("### 📊 Visual Summary")
        fig = px.bar(
            results_df,
            x="Pollutant",
            y="Predicted Value (mg/L)",
            color="Water Safety Status",
            text="Predicted Value (mg/L)",
            title=f"Pollutant Levels for Station '{station_id}' in {year_input}'",
            height=480
        )
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(
            yaxis_title="Concentration (mg/L)",
            xaxis_title="Pollutant",
            yaxis_range=[0, max(results_df["Predicted Value (mg/L)"]) * 1.25],
            plot_bgcolor='rgba(255,255,255,0.95)',
            paper_bgcolor='rgba(240,248,255,0.6)',
            font=dict(family="Segoe UI", size=14, color="#002b5c"),
            title_font=dict(size=22, color="#002b5c", family="Segoe UI"),
            title_x=0.5
        )
        st.plotly_chart(fig, use_container_width=True)

        # Download
        st.markdown("### 📥 Download Results")
        safe_station_id = re.sub(r'\W+', '_', station_id)
        csv = results_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download as CSV",
            data=csv,
            file_name=f"predicted_pollutants_{safe_station_id}_{year_input}.csv",
            mime="text/csv"
        )