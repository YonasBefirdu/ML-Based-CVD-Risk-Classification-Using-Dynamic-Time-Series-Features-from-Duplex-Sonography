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
├── Raw and Processed data columns/ # Raw ultrasound-derived waveform data first 4 columns (time,Brachial Data, Carotid diameter and blood velocity)...Preprocessed and synchronized, low-pass filtered, and normalized signals('Normalized Brachial', 'NormalizedFiltered Diameter' and 'Normalized Velocity')
│   ├── High_Risk_SPA--Raw_data
│   ├── Low_Risk_SPA--Raw_data
│   ├── High_r_stacked_rc_8.npy
│   ├── Low_r_stacked_rc_8.npy
│   ├── best_feature2_last_df.csv
│   ├── combined_data_last.xlsx                       
│
├── Feature_extraction_TSFEL_and_Shapeletes/
│   ├── Multi_Variate_Shapelets/
│       ├── Multivariate_shapelets.ipynb
│   ├── TSFEL/
│       ├── batch_processing.py
│       ├── merger.py
│
├── Fusion_features_model_training
│   ├── FUSION_OF_FEATURES.ipynb
│
├── Preprocessing/                       
│   ├──Normalization_of_all.py
│   ├── low_pass.py
│   ├── stacking.py
│
└── README.md                       # Project documentation
```
**Note:** The tree above is a conceptual layout used in the manuscript workflow. In this repository, executable scripts are currently organized under `Preprocessing/` and `Feature_extraction_TSFEL_and_Shapeletes/`, with model training notebooks under `Fusion_features_model_training/`.

## Dependencies

The following dependencies were identified by scanning the Python scripts and notebooks in this repository.

### Core Python packages

- `numpy`
- `pandas`
- `scipy`
- `openpyxl` (Excel I/O engine used by pandas)
- `matplotlib`
- `seaborn`
- `scikit-learn`

### Feature extraction and modeling packages

- `tsfel`
- `aeon` (shapelet transform utilities in notebooks)
- `mrmr-selection` (imported as `mrmr`)
- `xgboost`
- `lightgbm`
- `catboost`

### Optional acceleration / environment-specific packages

- `numba`
- `cupy` (GPU-accelerated array operations in notebook experiments)

### Suggested setup

Use Python 3.10+ and install dependencies with:

```bash
pip install numpy pandas scipy openpyxl matplotlib seaborn scikit-learn tsfel aeon mrmr-selection xgboost lightgbm catboost numba
```

If you plan to run GPU experiments, install a CUDA-matching CuPy build separately from the official CuPy installation guide.

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
## Usage Workflow

The project can be run as a stepwise pipeline:

1. **Low-pass filter carotid diameter signal**
   - Script: `Preprocessing/low_pass.py`
2. **Normalize waveform columns per risk group**
   - Script: `Preprocessing/Normalization_of_all.py`
3. **Stack processed samples into `.npy` arrays**
   - Script: `Preprocessing/stacking.py`
4. **Extract TSFEL feature tables from each patient file**
   - Script: `Feature_extraction_TSFEL_and_Shapeletes/TSFEL/batch_processing.py`
5. **Merge high- and low-risk feature tables**
   - Script: `Feature_extraction_TSFEL_and_Shapeletes/TSFEL/merger.py`
6. **Train and evaluate fusion models**
   - Notebook: `Fusion_features_model_training/FUSION_OF_FEATURES.ipynb`

## Reproducibility Notes

- Many scripts currently contain hard-coded Windows paths (e.g., `C:\Users\...`). Update these paths before running locally.
- Input files are expected to be `.xlsx` format with canonical columns such as:
  - `Brachial Data`
  - `Carotid Diameter`
  - `Filtered_Diameter (8 Hz)`
  - `blood velocity`
  - normalized columns generated during preprocessing
- Some notebooks include exploratory blocks (including optional GPU code); results may vary depending on software versions and hardware.

## Limitations

- This repository includes research scripts and notebooks rather than a fully packaged Python module.
- Paths and I/O conventions are dataset-specific and may require adaptation for external cohorts.
- The raw clinical data are sensitive and not intended for unrestricted redistribution.

## Citation

If you use this repository or workflow in your research, please cite the associated study:

> Machine Learning-Based Cardiovascular Disease Risk Classification Using Dynamic Time-Series Features from Carotid Duplex Sonography

## License

No explicit license file is currently included in this repository. Please contact the repository owner before reuse beyond academic reference.


