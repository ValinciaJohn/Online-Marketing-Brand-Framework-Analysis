import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the title
st.title('Data Visualization of the URls')

# Upload the CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Filter options
    st.sidebar.subheader("Filter Options")
    
    # Slider for Cumulative Rank
    cumulative_rank_min, cumulative_rank_max = st.sidebar.slider(
        'Select the range for Cumulative Rank', 
        int(df['Cumulative_Rank'].min()), 
        int(df['Cumulative_Rank'].max()), 
        (int(df['Cumulative_Rank'].min()), int(df['Cumulative_Rank'].max()))
    )
    
    # Selectbox for column to visualize
    metric = st.sidebar.selectbox(
        "Select Metric to Visualize",
        ['PRTE', 'PRSA', 'Cumulative_Rank']
    )
    
    # Apply filter
    filtered_df = df[(df['Cumulative_Rank'] >= cumulative_rank_min) & (df['Cumulative_Rank'] <= cumulative_rank_max)]
    
    # Statistical insights
    st.sidebar.subheader("Statistical Insights")
    st.sidebar.write("Mean of PRTE:", round(filtered_df['PRTE'].mean(), 2))
    st.sidebar.write("Median of PRTE:", round(filtered_df['PRTE'].median(), 2))
    st.sidebar.write("Mean of PRSA:", round(filtered_df['PRSA'].mean(), 2))
    st.sidebar.write("Mean of Cumulative Rank:", round(filtered_df['Cumulative_Rank'].mean(), 2))
    
    # Display filtered data
    st.subheader('Filtered Data')
    st.dataframe(filtered_df)

    # Set the aesthetic style of the plots
    sns.set(style="whitegrid")

    # Stacked Bar Chart for all three ranks
    st.subheader('Stacked Bar Chart: PRTE, PRSA, and Cumulative Rank by URL')
    fig, ax = plt.subplots(figsize=(12, 8))
    filtered_df.set_index('URL')[['PRTE', 'PRSA', 'Cumulative_Rank']].plot(
        kind='bar', stacked=True, colormap='Paired', ax=ax
    )
    ax.set_title('PRTE, PRSA, and Cumulative Rank for each URL', fontsize=16)
    ax.set_xlabel('URL', fontsize=14)
    ax.set_ylabel('Rank Value', fontsize=14)
    plt.xticks(rotation=90)
    st.pyplot(fig)

    # Additional bar and line plots for selected metric (optional as before)
    st.subheader(f'Bar Plot: {metric} Distribution for Filtered URLs')
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.barplot(x=metric, y='URL', data=filtered_df, palette='coolwarm', ax=ax2)
    ax2.set_title(f'{metric} Distribution of URLs', fontsize=16)
    ax2.set_xlabel(metric, fontsize=14)
    ax2.set_ylabel('URL', fontsize=14)
    st.pyplot(fig2)

    st.subheader(f'Line Plot: {metric} Trend for Filtered URLs')
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='URL', y=metric, data=filtered_df, marker='o', ax=ax3)
    ax3.set_title(f'{metric} Trend across Filtered URLs', fontsize=16)
    ax3.set_ylabel(metric, fontsize=14)
    ax3.set_xlabel('URL', fontsize=14)
    plt.xticks(rotation=90)
    st.pyplot(fig3)
    st.subheader('Top 10 URLs by Highest Cumulative Rank')
    top_10_df = df.nlargest(10, 'Cumulative_Rank')

    fig3, ax3 = plt.subplots(figsize=(12, 6))
    sns.barplot(x='Cumulative_Rank', y='URL', data=top_10_df, palette='viridis', ax=ax3)
    ax3.set_title('Top 10 URLs with Highest Cumulative Rank', fontsize=16)
    ax3.set_xlabel('Cumulative Rank', fontsize=14)
    ax3.set_ylabel('URL', fontsize=14)
    st.pyplot(fig3)