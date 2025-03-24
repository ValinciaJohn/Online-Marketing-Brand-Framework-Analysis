
from bs4 import BeautifulSoup
import requests
import csv
import re
from gensim import corpora
from gensim.models import LdaModel
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import nltk
nltk.download('punkt')        # For tokenizing text
nltk.download('stopwords')
nltk.download('punkt_tab')
# Function to scrape the content of a webpage
def scrape_all_content(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract content from various tags
        content = []
        for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'div', 'span', 'section', 'article']):
            content.append(tag.get_text(strip=True))  # Get text from the tag

        # Join all extracted content into a single string with spaces
        return ' '.join(content)  # This will ensure proper spacing between words
    
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return ""

# Function to clean the text
'''def clean_text(raw_text):
    # Remove any non-alphanumeric characters except for spaces
    cleaned_text = re.sub(r'[^A-Za-z0-9\s]', '', raw_text)  # Remove punctuation and special characters

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    # Split the text into words to remove stop words, then join back without tokenization
    #cleaned_text = ' '.join([word for word in cleaned_text.split() if word.lower() not in stop_words])

    # Stemming
    #ps = PorterStemmer()
    #cleaned_text = ' '.join([ps.stem(word) for word in cleaned_text.split()])

    return cleaned_text'''
'''def prepare_lda_data(texts):
    # Create a dictionary representation of the documents
    dictionary = corpora.Dictionary(texts)

    # Convert to bag-of-words format
    corpus = [dictionary.doc2bow(text) for text in texts]

    return dictionary, corpus

# Apply LDA
def apply_lda(corpus, dictionary, num_topics=5):
    # Train LDA model
    lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, passes=10)
    return lda_model'''

urls ={ "Google Results for Samsung smartphone": [
        "https://www.samsung.com/us/smartphones/",
        "https://www.samsung.com/us/",
        "https://www.samsung.com/us/mobile/phones/all-phones/",
        "https://www.verizon.com/smartphones/samsung/",
        "https://www.samsung.com/levant/smartphones/all-smartphones/",
        "https://www.bestbuy.com/site/mobile-cell-phones/samsung-galaxy/pcmcat305200050001.c?id=pcmcat305200050001",
        "https://eu.community.samsung.com/t5/other-galaxy-s-series/samsung-smartphone-with-asha-technology/td-p/3038370",
        "https://www.reddit.com/r/SamsungDex/comments/ke63xo/moving_mouse_between_samsung_smartphone_and/",
        "https://www.amazon.com/samsung-smartphones/s?k=samsung+smartphones",
        "https://news.samsung.com/global/how-samsung-galaxy-has-rewritten-smartphone-history-in-10-innovative-technologies",
        "https://semiconductor.samsung.com/processor/showcase/smartphone/",
        "https://meta.stackoverflow.com/questions/401413/how-can-i-type-backticks-on-my-samsung-smartphone-which-are-needed-for-inline-c",
        "https://insights.samsung.com/2023/02/09/8-tips-for-maximizing-your-smartphones-battery-life-3/",
        "https://community.spiceworks.com/t/any-way-to-reset-unlock-a-terminated-employees-company-samsung-smartphone/778454",
        "https://answers.microsoft.com/en-us/msoffice/forum/all/why-do-screenshots-from-my-samsung-smartphone/02281d1f-f382-4fce-90a5-befc879bb785",
        "https://www.sciencedirect.com/science/article/pii/S1877042816300696",
        "https://en.wikipedia.org/wiki/Samsung_Galaxy",
        "https://www.quora.com/Which-came-first-the-Apple-smartphone-or-the-Samsung-smartphone",
        "https://www.t-mobile.com/offers/samsung-phone-deals",
        "https://www.googlenestcommunity.com/t5/Cameras-and-Doorbells/Nest-doorbell-and-cam-whit-Samsung-smartphone/td-p/94985"
    ],
     "Yahoo Results for Samsung smartphone": [
        "https://www.samsung.com/us/smartphones/",
        "https://images.search.yahoo.com/search/images?p=Samsung+smartphone",
        "https://www.samsung.com/us/mobile/phones/all-phones/",
        "https://www.samsung.com/us/mobile/",
        "https://www.bestbuy.com/site/mobile-cell-phones/samsung-galaxy/pcmcat305200050001.c?id=pcmcat305200050001",
        "https://www.bestbuy.com/site/samsung-galaxy/all-samsung-galaxy-phones/pcmcat1661803373461.c?id=pcmcat1661803373461",
        "https://www.samsung.com/us/smartphones/",
        "https://news.samsung.com/us/samsung-galaxy-s21-ultra-unpacked-2021-ultimate-smartphone-experience-designed-epic/",
        "https://www.amazon.com/Samsung-Galaxy-S21-5G-Snapdragon/dp/B092CFFM84"
    ],
     "Bing Results for Samsung smartphone": [
        "https://www.samsung.com/in/smartphones/#:~:text=Looking ",
        "https://www.samsung.com/in/smartphones/all-smartphones/#:~:text=Explore",
        "https://www.samsung.com/us/mobile/",
        "https://www.bestbuy.com/site/samsung-galaxy/all-samsung-galaxy-phones/pcmcat1661803373461.c?id=pcmcat1661803373461",
        "https://www.cnet.com/tech/mobile/best-samsung-galaxy-phone/",
        "https://www.amazon.com/Samsung-Galaxy-S21-5G-Snapdragon/dp/B092CFFM84"
    ]

    }
# Iterate through the dictionary to scrape the content of each URL
scraped_data = []  # List to store scraped content as tuples (URL, content)

for engine, url_list in urls.items():
    print(f"\nScraping content for: {engine}")
    
    for url in url_list:
        print(f"Scraping URL: {url}")
        raw_content = scrape_all_content(url)  # Use the correct function name
         # Clean the content
        
        # Append the URL and cleaned content to the list
        scraped_data.append([url,raw_content])
        # Append the scraped content to the list
        

# Write the scraped data to a CSV file
with open('scraped_web_content.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['URL', 'Content'])  # Write the headers
    writer.writerows(scraped_data)       # Write the data rows

print("Scraped data has been written to 'scraped_web_content.csv'")
