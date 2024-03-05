import os
import glob
import pandas as pd

current_directory = os.path.dirname(os.path.abspath(__file__))

directory = os.path.join(current_directory, '../Data/')

abs_directory = os.path.abspath(directory)

# Create the directory if it doesn't exist
if not os.path.exists(abs_directory):
    os.makedirs(abs_directory)
    print(f"Directory '{abs_directory}' created.")

csv_files = glob.glob(os.path.join(abs_directory, '*.csv'))
# Read the CSV files into a list of DataFrames
data_frames = []

for csv_file in csv_files:
    data = pd.read_csv(csv_file)
    data_frames.append(data)
    
# Concatenate the DataFrames into a single DataFrame
merged_data = pd.concat(data_frames, ignore_index=True)

# Formatting date and time columns
merged_data['acq_date'] = pd.to_datetime(merged_data['acq_date'], format='%Y-%m-%d')
merged_data['acq_time'] = merged_data['acq_time'].astype(str).str.zfill(4)
merged_data['acq_time'] = pd.to_datetime(merged_data['acq_time'], format='%H%M', errors='coerce')
merged_data['acq_time'] = merged_data['acq_time'].dt.time

# Sorting by date and time
merged_data = merged_data.sort_values(by=['acq_date', 'acq_time'])
merged_data = merged_data.reset_index(drop=True)

# Converting category columns
merged_data['version'] = merged_data['version'].astype(str)
cat_cols = ['satellite', 'instrument','daynight']
merged_data[cat_cols] = merged_data[cat_cols].astype('category')

# Saving the merged data to a Parquet file
parquet_file = os.path.join(directory, 'col_2000-2024.parquet')

merged_data.to_parquet(parquet_file)

# # # Saving the merged data to a CSV file
# csv_file = os.path.join(directory, 'modis_2024_Colombia.csv')
# merged_data.to_csv(csv_file, index=False)