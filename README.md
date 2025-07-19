#  Water Quality Prediction Using Machine Learning

This project focuses on predicting key water quality indicators using historical monitoring data from 2000 to 2021. The analysis leverages machine learning to assess environmental parameters critical to aquatic health.

---

##  Project Goals

- Forecast pollutant levels at monitoring stations using historical data
- Classify water safety based on predicted pollutant concentrations
- Support decisions on environmental action and regulation

---

##  Project Structure

```
WaterQualityPrediction/
├── PB_All_2000_2021.csv                  # Raw water quality dataset (2000–2021)
├── predicted_water_quality_essential.csv # Model output: predicted pollutant levels
├── unsafe_samples_essential.csv          # Classified unsafe samples based on thresholds
├── Parameters_WQM_RMS.pdf                # Descriptions and permissible limits for each pollutant
├── WaterQualityPrediction.ipynb          # Jupyter Notebook: data cleaning, modeling, and evaluation
├── app.py                                # Streamlit app for interactive prediction and visualization
├── model_columns.pkl                     # Column structure used during model training
├── pollution_model.pkl                   # Trained Random Forest model (MultiOutput Regressor)
├── requirements.txt                      # pip dependency file for Python environment setup
├── .gitattributes                        # Git LFS tracking for large files (e.g., .pkl, .csv)
├── .gitignore                            # Git ignore rules to exclude unnecessary files
├── LICENSE                               # MIT license for open-source use
└── README.md                             # Full project overview and instructions

 Tips:
- Keep model_columns.pkl and pollution_model.pkl versioned if reproducibility matters.
- Use .gitattributes with Git LFS to manage .csv and .pkl efficiently.

```

---

##  Dataset Description

The dataset includes physicochemical parameters:

- **NH₄ (Ammonium)** – Wastewater contamination indicator
- **NO₃ (Nitrate), NO₂ (Nitrite)** – Agricultural and industrial runoff
- **BSK5 (BOD₅)** – Organic pollution load
- **O₂ (Dissolved Oxygen)** – Water quality and life support
- **PO₄ (Phosphate), SO₄ (Sulfate), CL (Chloride)** – Nutrients and industrial traces
- **Suspended Solids** – Turbidity and sediment impact

 See `Parameters_WQM_RMS.pdf` for environmental context and permissible limits.

---

##  Data Preprocessing

- Converted `date` column to datetime
- Extracted year, month, and day features
- Imputed missing values using column means
- Dropped redundant columns (`id`, `date`)

---

##  Modeling

- Algorithm: **Random Forest Regressor** and **XGBoost Regressor** using **MultiOutputRegressor** 
- Evaluation metrics: **Mean Absolute Error**, **Mean Squared Error**, **R² Score**
- Trained on extracted and cleaned numerical features
- Visual comparisons between actual vs predicted values 

---

##  Water Safety Classification

Predicted pollutant levels are compared against national/WHO safety thresholds. Each record is labeled as:  
-  Safe  
-  Unsafe  

---

##  Station-Year Forecasting

Forecast pollutant levels for any given year and monitoring station. Visualize pollutant variation over time.

---

##  Deployment (Optional)

A interactive **Streamlit web app** can be developed for interactive pollutant prediction, data exploration and visualization.

###  Prerequisites

Install dependencies using either of the following methods:

#### Option 1: pip

```bash
pip install -r requirements.txt
```
#### Option 2: conda

```bash
conda env create -f environment.yml
conda activate water_pollutants_env
```

###  Run the App

```bash
streamlit run app.py
```

###  Features

- Input any year and station ID to predict pollutant levels
- View visual results in interactive bar charts
- Download predicted values as CSV

###  Model File: pollution_model.pkl (Google Drive)
Model Link: https://drive.google.com/file/d/13jy3JdxHrRtn9YfUxrg_rgCFnXpME8qb/view?usp=sharing

---

##  Getting Started

###  Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/WaterQualityPrediction.git
cd WaterQualityPrediction

# Install required packages
pip install -r requirements.txt
```

###  Run the Notebook

```bash
jupyter notebook notebooks/WaterQualityPrediction.ipynb
```

---

##  References

-  Water parameter details: `docs/Parameters_WQM_RMS.pdf`
-  Dataset Source: Local monitoring data (2000–2021)

---

##  License

This project is open-source and available under the [MIT License](LICENSE).

