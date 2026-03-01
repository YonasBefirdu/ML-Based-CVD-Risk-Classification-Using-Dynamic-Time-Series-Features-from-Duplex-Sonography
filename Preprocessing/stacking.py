# This script processes Excel files in a folder:
# - Removes the first row (column names) and first column ('Time')
# - Transposes the remaining data
# - Stacks all processed arrays into a single 8D numpy array


import pandas as pd
import numpy as np
import os

# List of risk types to process
risk_levels = ["Low", "High"]

# Base path where both risk folders exist
base_path = r"C:\Users\user\Desktop\A_serious_research\A_TIME_SERIES_DATA\Code\LABELING_CHANGE"

for risk in risk_levels:
    print(f"\n===== Processing {risk} Risk =====")

    folder_path = os.path.join(base_path, f"{risk}_Risk_SPA--Raw_data")
    samples = []
    bad_files = []
    checked_files = 0

    # Loop through files for the current risk level
    for filename in os.listdir(folder_path):
        if filename.endswith(".xlsx") and not filename.startswith("~$"):
            file_path = os.path.join(folder_path, filename)

            try:
                df = pd.read_excel(file_path, engine='openpyxl', header=None)

                # Print shape only for the first Excel file
                if checked_files == 0:
                    print(df.head())
                    print(df.shape)

                # Process the data
                processed_data = df.iloc[1:, 1:].to_numpy().T  # shape → (8, 128)

                samples.append(processed_data)
                print(f"✅ {filename} - OK")

            except Exception as e:
                print(f"❌ {filename} - Error: {e}")
                bad_files.append(filename)

            checked_files += 1

    # Convert to 3D numpy array: (num_files, 8, 128)
    final_8d_array = np.array(samples)

    # Print final shape
    print(f"{risk} risk final array shape:", final_8d_array.shape)

    # Save output array
    output_path = os.path.join(base_path, f"{risk}_r_stacked.npy")
    np.save(output_path, final_8d_array)

    print(f"💾 Saved: {output_path}")

    # If bad files found
    if bad_files:
        print(f"\n⚠️ Bad files in {risk} Risk:")
        for bf in bad_files:
            print(" -", bf)



import numpy as np

# Load your .npy files (update the file paths accordingly)
array1 = np.load(r"C:\Users\user\Desktop\A_serious_research\A_TIME_SERIES_DATA\Code\LABELING_CHANGE\High_r_stacked.npy",allow_pickle=True)  # shape (37, 8, 128)
array2 = np.load(r"C:\Users\user\Desktop\A_serious_research\A_TIME_SERIES_DATA\Code\LABELING_CHANGE\Low_r_stacked.npy",allow_pickle=True)  # shape (113, 8, 128)

# Verify the shapes
print("array1 shape:", array1.shape)  # Should print (37, 8, 128)
print("array2 shape:", array2.shape)  # Should print (113, 8, 128)

# Concatenate along the first axis
stacked_array = np.concatenate((array1, array2), axis=0)

# The resulting shape is (37+113, 8, 128) i.e., (150, 8, 128)
print("Stacked array shape:", stacked_array.shape)

output_path = r"C:\Users\user\Desktop\A_serious_research\A_TIME_SERIES_DATA\Code\LABELING_CHANGE\Both_stacked.npy"
np.save(output_path, stacked_array)






