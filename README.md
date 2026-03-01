# ML-Based-CVD-Risk-Classification-Using-Dynamic-Time-Series-Features-from-Duplex-Sonography
This repository contains the workflows, code, and documentation for the study **“Machine Learning–Based Cardiovascular Risk Classification Using Multivariate Carotid Hemodynamic Time-Series Data.”**  
The project introduces a machine-learning framework that uses **dynamic arterial waveforms**—carotid diameter, Doppler flow velocity, and brachial pressure—to classify cardiovascular disease (CVD) risk.
## Overview

Traditional carotid ultrasound assessments rely mainly on static plaque measurements and peak Doppler velocities.  
In contrast, this project analyzes **dynamic, full-cycle arterial waveforms** to capture physiologically meaningful information related to vascular stiffness, plaque burden, and hemodynamic alterations.

The repository provides tools to process and analyze three synchronized time-series signals:

- **Carotid diameter waveform** extracted from B-mode cine images  
- **Doppler flow velocity waveform** derived from spectral Doppler envelopes  
- **Brachial pulse pressure waveform** recorded using plethysmography  

By combining advanced time-series feature extraction (TSFEL and shapelet transform) with machine learning classifiers, this framework enables accurate prediction of **cardiovascular disease (CVD) risk** from carotid duplex sonography.
## Key Features

- **Multimodal Time-Series Integration**  
  Combines carotid diameter, Doppler flow velocity, and brachial pressure waveforms for comprehensive hemodynamic analysis.

- **Hybrid Feature Extraction Pipeline**  
  Utilizes both **TSFEL signal-derived features** and **shapelet-based temporal subsequences** to capture detailed waveform characteristics.

- **Feature Selection with mRMR**  
  Reduces high-dimensional feature space to the most discriminative set, improving model performance and interpretability.

- **Benchmarking of Multiple ML Models**  
  Includes Random Forest, XGBoost, LightGBM, CatBoost, SVM, k-NN, AdaBoost, and Voting Classifiers.

- **High Predictive Performance**  
  Achieves up to **0.90 accuracy** and **0.95 AUC** using the combined feature set with a Random Forest classifier.

## Repository Structure

```plaintext
├── data/
│   ├── raw/                        # Raw ultrasound-derived waveform data
│   ├── processed/                  # Preprocessed, filtered, and synchronized signals
│
├── notebooks/
│   ├── 01_preprocessing.ipynb      # Signal cleaning and ECG-based alignment
│   ├── 02_feature_extraction.ipynb # TSFEL + shapelet feature generation
│   ├── 03_feature_selection.ipynb  # mRMR and MI-based ranking
│   ├── 04_model_training.ipynb     # Training ML classifiers with GridSearchCV
│   ├── 05_evaluation.ipynb         # Performance metrics and waveform analysis
│
├── src/
│   ├── preprocessing.py            # Preprocessing scripts
│   ├── tsfel_features.py           # TSFEL feature extraction utilities
│   ├── shapelet_features.py        # Shapelet transform implementation
│   ├── feature_selection.py        # mRMR feature selection
│   ├── train_models.py             # Model training pipeline
│   ├── evaluate.py                 # Evaluation and metrics computation
│
├── figures/                        # Figures used in documentation/manuscript
│   ├── pipeline.png
│   ├── feature_scores.png
│   ├── shapelets.png
│   ├── mi_scores.png
│
└── README.md                       # Project documentation
```
## Dataset Description

### Participants
- **150 patients**, aged 50 years or older  
- Clinical examinations performed at **Gangnam Severance Hospital**, Seoul, Korea  
- Carotid duplex ultrasound and brachial-to-ankle pulse wave velocity (PWV) measured on the same day

### Extracted Waveforms
The dataset includes three synchronized arterial time-series signals:

- **Carotid Diameter Waveform**  
  - Extracted from longitudinal B-mode cine images  
  - Tracked using the CAROLAB speckle-tracking algorithm  
  - Captures radial wall motion over a cardiac cycle  

- **Carotid Flow Velocity Waveform**  
  - Derived from spectral Doppler ultrasound  
  - Envelope extracted using gray-level thresholding  
  - Represents blood flow dynamics throughout systole and diastole  

- **Brachial Pressure Waveform**  
  - Recorded using a volume-plethysmography system  
  - Digitized and resampled for waveform alignment  

### Signal Processing
All three waveforms were:

- Detrended to remove slow drift  
- Low-pass filtered to remove noise (8–10 Hz cutoff)  
- Min–max normalized across subjects  
- Synchronized to the **ECG R-wave**  
- Resampled uniformly at **128 Hz**  
- Cropped to a single cardiac cycle for each subject  

### Risk Labels
Cardiovascular risk was defined based on **Total Plaque Area (TPA)**:

| Risk Group | Criterion |
|------------|-----------|
| **High Risk** | TPA ≥ 40 mm² |
| **Low Risk** | TPA < 40 mm² |

This threshold is supported by prior clinical studies indicating strong association between TPA and CVD risk.
## Methods

### 1. Feature Extraction

#### TSFEL Features
The **Time Series Feature Extraction Library (TSFEL)** was used to compute:
- Statistical features (mean, variance, skewness)
- Temporal features (zero-crossing rate, autocorrelation)
- Spectral features (dominant frequency, spectral entropy)

A total of **201 TSFEL features** were extracted from the three waveforms and later reduced to **11** using the mRMR algorithm.

#### Shapelet Transform Features
The **Shapelet Transform** was used to identify short, discriminative subsequences from the multivariate time series.  
- Shapelets capture morphological differences between high- and low-risk groups  
- 10 shapelet-based features were extracted  
- Distances to each shapelet were used as feature values

#### Final Feature Set
TSFEL + shapelet features were combined and further reduced via **mRMR**, resulting in a final set of **15 optimal features** for model training.

---

### 2. Machine Learning Models

Eight traditional ML classifiers were evaluated:

- **Random Forest**
- **XGBoost**
- **LightGBM**
- **CatBoost**
- **AdaBoost**
- **Support Vector Machine (SVM)**
- **k-Nearest Neighbor (k-NN)**
- **Voting Classifier**

Hyperparameters were tuned using **GridSearchCV** with **5-fold stratified cross-validation**.

---

### 3. Model Performance

The combined feature set (TSFEL + shapelets) achieved the strongest results.

| Model | Accuracy | AUC | F1-score |
|--------|----------|------|----------|
| **Random Forest** | **0.90** | **0.95** | **0.80** |
| LightGBM | 0.87 | 0.80 | 0.79 |
| XGBoost | 0.83 | 0.76 | 0.75 |
| AdaBoost | 0.86 | 0.82 | 0.79 |
| CatBoost | 0.80 | 0.80 | 0.64 |
| SVM | 0.66 | 0.61 | 0.54 |
| k-NN | 0.80 | 0.61 | 0.57 |

**Random Forest demonstrated the best overall performance.**

---

### 4. Waveform Contribution Analysis

To evaluate the role of each waveform, models were trained using individual and combined signals:

| Waveforms Used | Accuracy | AUC | F1-score |
|----------------|----------|------|----------|
| Pressure only | 0.77 | 0.67 | 0.61 |
| Diameter only | 0.83 | 0.87 | 0.79 |
| Velocity only | 0.77 | 0.57 | 0.54 |
| **All three combined** | **0.90** | **0.95** | **0.80** |

**The multivariate model yielded the highest predictive performance**, demonstrating that pressure, diameter, and velocity waveforms carry complementary information about arterial mechanics and CVD risk.

