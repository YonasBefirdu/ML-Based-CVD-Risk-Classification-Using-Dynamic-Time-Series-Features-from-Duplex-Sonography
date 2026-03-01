import pandas as pd
import tsfel
import os
def check_duplicate_columns(df):
    """Check for columns with identical names"""
    duplicates = df.columns[df.columns.duplicated()].tolist()
    if duplicates:
        print("\n⚠️ Exact duplicate columns found:")
        for col in set(duplicates):
            count = list(df.columns).count(col)
            print(f"'{col}' appears {count} times")
    else:
        print("\n✅ All column names are unique")
    return duplicates

def process_signals(file_path, output_dir):
    # Load data
    df = pd.read_excel(file_path)#.set_index('Time')
    
    # Calculate sampling frequency from normalized time (0-1 range)
    fs = 25 #1 / (df.index[1] - df.index[0])  # Auto-calculate from 128 points
    
    # Feature storage
    all_features = pd.DataFrame()

    #Process Brachial Pressure
    brachial = (df['Normalized Brachial'].values)/(10**6)
    brachial_features_1 = tsfel.time_series_features_extractor(
         tsfel.get_features_by_domain("temporal"),
        brachial, fs=fs, window_size=128).add_prefix('Brachial_')
    
    #Process Carotid Diameter 
    carotid = df['Normalized Filtered Diameter'].values
    carotid_features_1 = tsfel.time_series_features_extractor(
        tsfel.get_features_by_domain("temporal"),
        carotid, fs=fs, window_size=128).add_prefix('Carotid_')

    brachial_features_2 = tsfel.time_series_features_extractor(
         tsfel.get_features_by_domain("statistical"),
        brachial, fs=fs, window_size=128).add_prefix('Brachial_')
    
    #Process Carotid Diameter 

    carotid_features_2 = tsfel.time_series_features_extractor(
        tsfel.get_features_by_domain("statistical"),
        carotid, fs=fs, window_size=128).add_prefix('Carotid_')
    
    # Process Blood Velocity
    velocity = df['Normalized Velocity'].values
    velocity_features = tsfel.time_series_features_extractor(
        tsfel.get_features_by_domain("spectral"),
        velocity, fs=fs, window_size=128
    ).add_prefix('Velocity_')
    
    # Combine features
    all_features = pd.concat([
        brachial_features_1,
        carotid_features_1,
        brachial_features_2,
        carotid_features_2,
        velocity_features
    ], axis=1)
    duplicate_cols = check_duplicate_columns(all_features)
    
    if duplicate_cols:
        print("\n❌ Warning: Duplicate columns will be dropped before saving")
        print(duplicate_cols[:-1])
    
    # Save results
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"features_{os.path.basename(file_path)}")
    #all_features.drop(columns=all_features.columns[0], axis=1,  inplace=True)
    all_features.to_excel(output_path)
    
    print(f"Extracted {all_features.shape[1]} features")
    return all_features

def batch_process(base_input_dir, base_output_dir):
    """Process all Excel files in risk category subfolders"""
    risk_categories = ['High_Risk_SPA--Raw_data', 'Low_Risk_SPA--Raw_data']  # Update with your actual folder names
    
    for risk_category in risk_categories:
        input_dir = os.path.join(base_input_dir, risk_category)
        output_dir = os.path.join(base_output_dir, risk_category)
        
        print(f"\n{'='*40}\nProcessing {risk_category}...\n{'='*40}")
        
        for file_name in os.listdir(input_dir):
            if file_name.endswith('.xlsx'):
                patient_id = os.path.splitext(file_name)[0]
                input_path = os.path.join(input_dir, file_name)
                output_path = os.path.join(output_dir, f"features_{file_name}")
                
                if os.path.exists(output_path):
                    print(f"⏩ Already processed: {patient_id}")
                    continue
                
                try:
                    print(f"\nProcessing {patient_id}...")
                    process_signals(input_path, output_dir)
                    print(f"✅ Success: {patient_id}")
                    
                except Exception as e:
                    print(f"❌ Failed {patient_id}: {str(e)}")
                    # Create error log
                    with open(os.path.join(output_dir, 'processing_errors.log'), 'a') as f:
                        f.write(f"{patient_id}\t{str(e)}\n")

if __name__ == "__main__":
    BASE_INPUT = r"C:\Users\user\Desktop\A_serious_research\A_TIME_SERIES_DATA\Code\LABELING_CHANGE"
    BASE_OUTPUT = r"C:\Users\user\Desktop\A_serious_research\A_TIME_SERIES_DATA\Code\LABELING_CHANGE\features"
    
    batch_process(BASE_INPUT, BASE_OUTPUT)