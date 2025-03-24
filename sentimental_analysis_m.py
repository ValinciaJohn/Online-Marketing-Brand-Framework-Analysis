import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
import re

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

positive_words = set([
    "good", "excellent", "happy", "positive", "amazing", "love", "great", "awesome", "fantastic", "wonderful", 
    "superb", "incredible", "impressive", "brilliant", "pleased", "joyful", "delighted", "successful", "satisfied", "glad"
])

negative_words = set([
    "bad", "poor", "sad", "negative", "terrible", "hate", "awful", "disappointing", "horrible", "worst", 
    "dreadful", "disgusting", "painful", "unhappy", "miserable", "regret", "fail", "sorrow", "angry", "frustrated"
])

neutral_words = set([
    "okay", "average", "fine", "normal", "sufficient", "typical", "fair", "acceptable", "ordinary", "standard",
    "mediocre", "moderate", "regular", "so-so", "unremarkable", "adequate", "routine", "unsure", "balanced", "equivalent"
])

# Function to preprocess text
def preprocess_text(content):
    # Check if content is a string
    if not isinstance(content, str):
        return []
    
    # Remove non-alphanumeric characters except spaces
    cleaned_text = re.sub(r'[^A-Za-z0-9\s]', '', content)
    
    # Tokenize sentences
    sentences = sent_tokenize(cleaned_text.lower())
    
    # Initialize Porter Stemmer and Stopwords
    ps = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    
    # Process each sentence
    processed_sentences = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        filtered_words = [ps.stem(word) for word in words if word not in stop_words and word.isalnum()]
        processed_sentences.append(filtered_words)
    
    return processed_sentences

# Function to classify sentences with negation handling
def classify_sentence_with_negation(sentence):
    is_negated = False
    sentiment_score = 0
    
    for i, word in enumerate(sentence):
        if word in neutral_words:
            is_negated = True
        elif word in positive_words:
            if is_negated:
                sentiment_score -= 1  # Negation flips the sentiment
                is_negated = False
            else:
                sentiment_score += 1
        elif word in negative_words:
            if is_negated:
                sentiment_score += 1  # Negation flips the sentiment
                is_negated = False
            else:
                sentiment_score -= 1
    
    if sentiment_score > 0:
        return "positive"
    elif sentiment_score < 0:
        return "negative"
    else:
        return "neutral"

# Function to calculate PRSA for a page
def calculate_prsa(sentences, a=1.0, b=0.5, c=0.3):
    positive_count = 0
    neutral_count = 0
    negative_count = 0
    
    # Classify each sentence
    for sentence in sentences:
        classification = classify_sentence_with_negation(sentence)
        if classification == "positive":
            positive_count += 1
        elif classification == "neutral":
            neutral_count += 1
        else:
            negative_count += 1
    
    total_sentences = len(sentences)
    
    # Calculate probabilities
    p_positive = positive_count / total_sentences if total_sentences > 0 else 0
    p_neutral = neutral_count / total_sentences if total_sentences > 0 else 0
    p_negative = negative_count / total_sentences if total_sentences > 0 else 0
    
    # Calculate PRSA
    prsa = (a * p_positive) + (b * p_neutral) - (c * p_negative)
    
    return prsa, {"positive": positive_count, "neutral": neutral_count, "negative": negative_count}


df = pd.read_csv('scraped_web_content_m.csv')
print(df.columns)
print(df.head())


if 'Content' in df.columns:
  
    df['processed_sentences'] = df['Content'].apply(preprocess_text)
    
    # Calculate PRSA for each row
    df['PRSA_Score'], df['Sentiment_Counts'] = zip(*df['processed_sentences'].apply(calculate_prsa))
    
    # Split the sentiment counts into separate columns
    df['Positive_Count'] = df['Sentiment_Counts'].apply(lambda x: x['positive'])
    df['Neutral_Count'] = df['Sentiment_Counts'].apply(lambda x: x['neutral'])
    df['Negative_Count'] = df['Sentiment_Counts'].apply(lambda x: x['negative'])
    
   
    df = df.drop(columns=['processed_sentences', 'Sentiment_Counts'])
    
   
    if 'URL' in df.columns:
        df['Total_Score'] = df[['Positive_Count', 'Neutral_Count', 'Negative_Count']].sum(axis=1)
        
        # Add a rank column based on PRSA scores
        df['Rank'] = df['PRSA_Score'].rank(method='min', ascending=False)
        
        
        final_df = df[['URL', 'Total_Score', 'PRSA_Score', 'Rank']]
        final_df = final_df.rename(columns={'Total_Score': 'Total Score'})
        
        # Sort by PRSA score and reset the index
        final_df = final_df.sort_values(by='PRSA_Score', ascending=False).reset_index(drop=True)
        
        # Save the results to a new CSV file
        final_df.to_csv('prsa_rank_m.csv', index=False)
        print("PRSA results saved to prsa_results_ranked.csv")
    else:
        print("'URL' column not found in the CSV file.")
else:
    print("'Content' column not found in the CSV file.")
