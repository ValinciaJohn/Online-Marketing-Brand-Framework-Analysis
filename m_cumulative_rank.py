import pandas as pd
pr_sg_df = pd.read_csv('export_m.csv')    
pr_te_df = pd.read_csv('url_scores_m.csv')     
pr_sa_df = pd.read_csv('prsa_rank_m.csv')  
print("Social Graph DataFrame head:\n", pr_sg_df.head())
print("Text Edge DataFrame head:\n", pr_te_df.head())
print("Sentiment Analysis DataFrame head:\n", pr_sa_df.head())
print("Social Graph DataFrame columns:", pr_sg_df.columns)
print("Text Edge DataFrame columns:", pr_te_df.columns)
print("Sentiment Analysis DataFrame columns:", pr_sa_df.columns)

# Assuming 'PageRank' is the column to be renamed to 'PRsg'
if 'PageRank' in pr_sg_df.columns:
    pr_sg_df.rename(columns={'PageRank': 'PRsg'}, inplace=True)
else:
    print("Column 'PageRank' not found in Social Graph DataFrame. Assigning default value.")
    pr_sg_df['PRsg'] = 0  # Set default value for missing 'PRsg'

pr_te_df.rename(columns={'Total Score': 'PRTE'}, inplace=True)  
pr_sa_df.rename(columns={'Rank': 'PRSA'}, inplace=True)
merged_df = pr_sg_df.merge(pr_te_df[['URL', 'PRTE']], on='URL', how='outer').merge(pr_sa_df[['URL', 'PRSA']], on='URL', how='outer')
print("Merged DataFrame columns:", merged_df.columns)
merged_df['PRsg'] = merged_df.get('PRsg', 0).fillna(0)
merged_df['PRTE'] = merged_df.get('PRTE', 0).fillna(0)
merged_df['PRSA'] = merged_df.get('PRSA', 0).fillna(0)

# Ensure the data types are correct
merged_df['PRsg'] = pd.to_numeric(merged_df['PRsg'], errors='coerce').fillna(0)
merged_df['PRTE'] = pd.to_numeric(merged_df['PRTE'], errors='coerce').fillna(0)
merged_df['PRSA'] = pd.to_numeric(merged_df['PRSA'], errors='coerce').fillna(0)

# Calculate the cumulative rank if all necessary columns are present
if 'PRsg' in merged_df.columns and 'PRTE' in merged_df.columns and 'PRSA' in merged_df.columns:
    # Calculate the cumulative rank
    merged_df['Cumulative_Rank'] = merged_df['PRsg'] + merged_df['PRTE'] + merged_df['PRSA']
else:
    print("One or more rank columns are missing in the merged DataFrame.")
    missing_columns = [col for col in ['PRsg', 'PRTE', 'PRSA'] if col not in merged_df.columns]
    print("Missing columns:", missing_columns)

# Select relevant columns for output if they exist
output_columns = ['URL', 'PRsg', 'PRTE', 'PRSA', 'Cumulative_Rank']
if all(col in merged_df.columns for col in output_columns):
    final_df = merged_df[output_columns]
    
    # Optionally, sort the results by cumulative rank
    final_df = final_df.sort_values(by='Cumulative_Rank', ascending=False).reset_index(drop=True)

    # Save the results to a new CSV file
    final_df.to_csv('cumulative_page_rank_m.csv', index=False)

    print("Cumulative page ranks calculated and saved to cumulative_page_rank_m.csv.")
else:
    print("Not all output columns are present in the merged DataFrame.")
