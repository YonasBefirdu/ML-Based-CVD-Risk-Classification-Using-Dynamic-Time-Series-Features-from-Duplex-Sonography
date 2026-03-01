import os
import pandas as pd
import numpy as np

# === Define your folders ===
base_folder = r"C:\Users\user\Desktop\A_serious_research\A_TIME_SERIES_DATA\LAST_Non.normalized - All 150 patients"  # change this
risk_folders = ['High_Risk_SPA--Raw_data', 'Low_Risk_SPA--Raw_data']

# === Columns to normalize ===
columns_to_normalize = {
    'Brachial Data': 'Normalized Brachial',
    'Filtered_Diameter (8 Hz)': 'Normalized Filtered Diameter',
    'blood velocity': 'Normalized Velocity'
}

def get_global_min_max(folder_path, columns):
    """Find global min and max for each column across all Excel files in a folder."""
    global_min = {col: np.inf for col in columns}
    global_max = {col: -np.inf for col in columns}
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.xlsx') and not file_name.startswith('~$'):
            file_path = os.path.join(folder_path, file_name)
            try:
                df = pd.read_excel(file_path)
                for col in columns:
                    if col in df.columns:
                        col_data = df[col].dropna()
                        if not col_data.empty:
                            global_min[col] = min(global_min[col], col_data.min())
                            global_max[col] = max(global_max[col], col_data.max())
            except Exception as e:
                print(f"Failed to read {file_name}: {e}")

    return global_min, global_max

def normalize_and_save(folder_path, min_vals, max_vals, columns_map):
    """Apply min-max normalization and save the files with new columns."""
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.xlsx') and not file_name.startswith('~$'):
            file_path = os.path.join(folder_path, file_name)
            try:
                df = pd.read_excel(file_path)
                for col, new_col in columns_map.items():
                    if col in df.columns:
                        min_val = min_vals[col]
                        max_val = max_vals[col]
                        if max_val != min_val:  # avoid division by zero
                            df[new_col] = (df[col] - min_val) / (max_val - min_val)
                        else:
                            df[new_col] = 0  # or np.nan
                df.to_excel(file_path, index=False)
                print(f"Updated: {file_name}")
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

# === Process each folder ===
for folder in risk_folders:
    folder_path = os.path.join(base_folder, folder)
    print(f"\nProcessing folder: {folder}")
    
    min_vals, max_vals = get_global_min_max(folder_path, columns_to_normalize.keys())
    print(f"Min values: {min_vals}")
    print(f"Max values: {max_vals}")
    
    normalize_and_save(folder_path, min_vals, max_vals, columns_to_normalize)
