import pandas as pd
import os
import re

# Folders
high_risk_folder = r"C:\Users\user\Desktop\A_serious_research\A_TIME_SERIES_DATA\Code\LABELING_CHANGE\features\High_Risk_SPA--Raw_data"
low_risk_folder  = r"C:\Users\user\Desktop\A_serious_research\A_TIME_SERIES_DATA\Code\LABELING_CHANGE\features\Low_Risk_SPA--Raw_data"

# Output file
output_file = r"C:\Users\user\Desktop\A_serious_research\A_TIME_SERIES_DATA\Code\LABELING_CHANGE\features\combined_data_last.xlsx"
def extract_id(file_name):
    """
    Extracts the numeric ID from the file name.
    For example, from 'features_1. 6249856R.xlsx' it will extract '6249856'.
    Adjust the regex if needed.
    """
    # Find all digits in the file name and join them together
    digits = re.findall(r'\.\s*([A-Za-z0-9]+)\.', file_name)
    if digits:
        return ''.join(digits)
    return file_name

def read_folder(folder_path, label):
    """
    Reads all Excel files in the given folder,
    appends them into a single DataFrame, 
    and adds 'filename' and 'risk_label' columns.
    """
    all_data = []
    for file_name in os.listdir(folder_path):
        # Only read Excel files
        if file_name.endswith(".xlsx") or file_name.endswith(".xls"):
            file_path = os.path.join(folder_path, file_name)
            
            # Read Excel assuming first row is header
            df = pd.read_excel(file_path, header=0)
            # Extract numeric ID from file name
            file_id = extract_id(file_name)
            
            # Add extra columns
            df["filename"] = file_id
            df["risk_label"] = label
            
            # Collect data
            all_data.append(df)
    
    # Combine all data for this folder into one DataFrame
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        # Return an empty DataFrame if no valid files found
        return pd.DataFrame()

# Read both folders
df_high_risk = read_folder(high_risk_folder, "high_risk")
df_low_risk  = read_folder(low_risk_folder,  "low_risk")

# Combine all data
df_combined = pd.concat([df_high_risk, df_low_risk], ignore_index=True)

# Write to Excel
df_combined.to_excel(output_file, index=False)

print(f"Combined file saved as: {output_file}")

