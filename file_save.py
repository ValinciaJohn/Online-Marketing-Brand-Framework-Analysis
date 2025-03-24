import pandas as pd
df = pd.read_csv("export.csv")
# Select the single column you want to copy (replace 'column_name' with your actual column name)
single_column = df[['URL']]

# Write the selected column to a new CSV file
single_column.to_csv('links.csv', index=False)