# 🌊 Water Quality Prediction Using Machine Learning

This project focuses on predicting key water quality indicators using historical monitoring data from 2000 to 2021. The analysis leverages machine learning to assess environmental parameters critical to aquatic health.

---

## 🎯 Project Goals

- Forecast pollutant levels at monitoring stations using historical data
- Classify water safety based on predicted pollutant concentrations
- Support decisions on environmental action and regulation

---

## 📁 Project Structure

```
WaterQualityPrediction/
│
├── 📊 Data
│   ├── PB_All_2000_2021.csv                  # Water quality dataset
│   ├── predicted_water_quality_essential.csv # Predicted pollutant levels
│   └── unsafe_samples_essential.csv          # Samples classified as unsafe
│
├── 📔 Notebooks
│   └── WaterQualityPrediction.ipynb          # Original notebook
│ 
│
├── 📁 Models
│   ├── pollution_model.pkl                   # Trained Random Forest model
│   └── model_columns.pkl                     # Feature alignment reference
│
├── 📁 Docs
│   └── Parameters_WQM_RMS.pdf                # Pollutant descriptions and environmental limits
│
├── .gitignore                                # Ignore patterns for git
├── requirements.txt                          # Python library dependencies
├── README.md                                 # Full project documentation
└── LICENSE                                    # License file (MIT, to be added if not present)

```

---

## 📊 Dataset Description

The dataset includes physicochemical parameters:

- **NH₄ (Ammonium)** – Wastewater contamination indicator
- **NO₃ (Nitrate), NO₂ (Nitrite)** – Agricultural and industrial runoff
- **BSK5 (BOD₅)** – Organic pollution load
- **O₂ (Dissolved Oxygen)** – Water quality and life support
- **PO₄ (Phosphate), SO₄ (Sulfate), CL (Chloride)** – Nutrients and industrial traces
- **Suspended Solids** – Turbidity and sediment impact

📄 See `Parameters_WQM_RMS.pdf` for environmental context and permissible limits.

---

## 🧼 Data Preprocessing

- Converted `date` column to datetime
- Extracted year, month, and day features
- Imputed missing values using column means
- Dropped redundant columns (`id`, `date`)

---

## 🤖 Modeling

- Algorithm: **Random Forest Regressor** using **MultiOutputRegressor** 
- Evaluation metrics: **Mean Absolute Error**, **Mean Squared Error**, **R² Score**
- Trained on extracted and cleaned numerical features
- Visual comparisons between actual vs predicted values 

---

## 🧪 Water Safety Classification

Predicted pollutant levels are compared against national/WHO safety thresholds. Each record is labeled as:  
- ✅ Safe  
- ⚠️ Unsafe  

---

## 📈 Station-Year Forecasting

Forecast pollutant levels for any given year and monitoring station. Visualize pollutant variation over time.

---

## 🚀 Deployment (Optional)

A Streamlit app can be developed for interactive pollutant prediction and visualization.

Model Link: https://drive.google.com/file/d/13jy3JdxHrRtn9YfUxrg_rgCFnXpME8qb/view?usp=sharing

---

## 🚀 Getting Started

### 🔧 Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/WaterQualityPrediction.git
cd WaterQualityPrediction

# Install required packages
pip install -r requirements.txt
```

### 📓 Run the Notebook

```bash
jupyter notebook notebooks/WaterQualityPrediction.ipynb
```

---

## 📌 References

- 📑 Water parameter details: `docs/Parameters_WQM_RMS.pdf`
- 📈 Dataset Source: Local monitoring data (2000–2021)

---

## ⚖️ License

This project is open-source and available under the [MIT License](LICENSE).
