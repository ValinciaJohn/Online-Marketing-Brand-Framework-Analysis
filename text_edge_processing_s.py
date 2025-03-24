from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
import re
import nltk
import csv

nltk.download('punkt')
nltk.download('stopwords')

# Increase the field size limit to handle larger fields
csv.field_size_limit(1000000) 

# Function to read the CSV file and extract URL and content
def read_csv_file(file_path):
    data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            url = row[0]       # First column is the URL
            content = row[1]   # Second column is the content
            data.append((url, content))  # Store as a tuple (URL, content)
    return data

# Function to preprocess and filter the text
def preprocess_text(content):
    # Remove any non-alphanumeric characters except for spaces
    cleaned_text = re.sub(r'[^A-Za-z0-9\s]', '', content)  # Remove punctuation and special characters

    # Tokenize the text into sentences and words
    sentences = sent_tokenize(cleaned_text.lower())  # Convert to lowercase and split into sentences
    
    # Stemming and filtering stop words
    ps = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    
    processed_sentences = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        filtered_words = [ps.stem(word) for word in words if word not in stop_words and word.isalnum()]
        processed_sentences.append(filtered_words)  # Append processed words of each sentence
    
    return processed_sentences  # List of tokenized, stemmed sentences

# Function to detect relationships between main product terms and adjectives
def detect_relationships(sentences, main_terms, relation_terms):
    relationships = []

    for sentence in sentences:
        for main_term in main_terms:
            if main_term in sentence:
                for word in sentence:
                    if word in relation_terms:
                        relationships.append((main_term, word))  # Store relationship as an edge (main term, related word)
    
    return relationships

# Function to count relationships (edges) between terms
def count_relationships(relationships):
    edge_count = Counter(relationships)  # Count each unique relationship
    return edge_count

# Function to score web pages based on term relationships
def score_web_page(content, main_terms, relation_terms):
    # Step 1: Preprocess the content
    sentences = preprocess_text(content)
    
    # Step 2: Detect relationships between terms
    relationships = detect_relationships(sentences, main_terms, relation_terms)
    
    # Step 3: Count relationships (edges)
    edge_count = count_relationships(relationships)
    
    # Return total number of relationships (edges) found
    return sum(edge_count.values()), edge_count  # Return total count and individual edge counts

main_terms = ["battery", "camera", "screen", "performance", "processor", "storage", "phones","image","price","brand","OS","touch","wireless","Memory","photos",
              "charging", "design", "software", "display", "connectivity", "models","fold","flip","resolution","windows","device","pink","snapdragon","navy","mouse",
              "durability", "waterproof", "speakers", "biometrics", "security","large screen","design","galaxy","black","grey","blue","smartphone","android","cameras","camera roll"]

relation_terms = ["good", "excellent", "poor", "fast", "slow", "strong", "first","model","security",
                  "weak", "smooth", "efficient", "powerful", "compact", "reset","awesome","color","capacity",
                  "lightweight", "premium", "affordable", "stylish", "version","fully","backup","unlocked","unlock",
                  "laggy", "reliable", "unstable", "versatile","smart","latest","high","super","fast","zoom","smart"]

# Read the CSV file containing web page content and URLs
file_path = 'scraped_web_content_s.csv'  # Path to your CSV file
web_pages = read_csv_file(file_path)

# Rank web pages based on term relationships
ranked_pages = []
url_scores = {}  # Dictionary to store URL and its total score

for url, content in web_pages:
    score, edge_count = score_web_page(content, main_terms, relation_terms)
    ranked_pages.append((url, score, edge_count))
    url_scores[url] = score  # Store URL and score in the dictionary

# Sort by score (number of relationships) in descending order
ranked_pages = sorted(ranked_pages, key=lambda x: x[1], reverse=True)

# Display the ranked pages
for url, score, edges in ranked_pages:
    print(f"URL: {url}, Score: {score}, Edges: {edges}")

# Save the URL and scores to a CSV file
output_file_path = 'url_scores_s.csv'  # Path for the output CSV file
with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['URL', 'Total Score'])  # Write the headers
    for url, score in url_scores.items():
        writer.writerow([url, score])  # Write each URL and its score

print(f"URL scores have been saved to '{output_file_path}'")
