import pandas as pd

# Load the existing CSV file
existing_csv = 'path_to_existing_file.csv'

# Read the CSV into a DataFrame
df = pd.read_csv("C:\Users\kalya\OneDrive\Documents\BOOKS\SEM 5\SNDA_package\env\export.csv")

# Select the desired column (replace 'column_name' with your column's name)
column_to_extract = df[['column_name']]  # Double brackets to keep it as a DataFrame

# Save the selected column to a new CSV file
new_csv = 'path_to_new_file.csv'
column_to_extract.to_csv(new_csv, index=False)

print(f"Column has been extracted and saved to {new_csv}")
