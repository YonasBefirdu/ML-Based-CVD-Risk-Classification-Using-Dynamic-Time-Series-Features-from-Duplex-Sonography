import os
import pandas as pd
from scipy.signal import butter, sosfiltfilt

# ==== Filter parameters ====
fs = 25         # Sampling frequency in Hz
cutoff = 8.0    # Low-pass cutoff frequency
order = 4       # Filter order

# ==== Low-pass filter function ====
def lowpass_filter(data, cutoff, fs, order=2):
    sos = butter(order, cutoff, btype='low', fs=fs, output='sos')
    return sosfiltfilt(sos, data)

# ==== Folder containing CSV files ====
folder_path = r'C:\Users\user\Desktop\A_serious_research\A_TIME_SERIES_DATA\LAST_Non.normalized - All 150 patients\Low_Risk_SPA--Raw_data'

# ==== Iterate over CSV files ====
for filename in os.listdir(folder_path):
    if filename.endswith(".xlsx"):
        file_path = os.path.join(folder_path, filename)

        try:
            # Read CSV
            df = pd.read_excel(file_path)

            # Ensure required column is present
            if 'Carotid Diameter' in df.columns:
                # Apply low-pass filter
                filtered = lowpass_filter(
                    df['Carotid Diameter'].values,
                    cutoff, fs, order
                )

                # Add new column
                df['Filtered_Diameter (8 Hz)'] = filtered

                # Save to same file (overwrite)
                df.to_excel(file_path, index=False)
                print(f"Filtered and updated: {filename}")
            else:
                print(f"Skipped (missing target column): {filename}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")
