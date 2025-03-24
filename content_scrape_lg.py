import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape the content of a webpage
def scrape_all_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)  # Increase timeout
        response.raise_for_status()  # Raise an error for bad responses
        
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract content from various tags
        content = []
        for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'div', 'span', 'section', 'article']):
            content.append(tag.get_text(strip=True))  # Get text from the tag

        # Join all extracted content into a single string with spaces
        return ' '.join(content)
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.Timeout:
        print(f"Timeout error for {url}")
    except requests.exceptions.RequestException as err:
        print(f"Other error occurred: {err}")
    
    return ""  # Return empty string for failed requests

# Read URLs from CSV file
input_csv = 'links_lg.csv'
scraped_data = []

# Open the input CSV and read URLs
with open(input_csv, mode='r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header
    
    for row in reader:
        url = row[0]
        print(f"Scraping URL: {url}")
        raw_content = scrape_all_content(url)
        scraped_data.append([url, raw_content])

# Write the scraped data to a new CSV file
output_csv = 'scraped_web_content_lg.csv'
with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['URL', 'Content'])  # Write the headers
    writer.writerows(scraped_data)       # Write the data rows

print(f"Scraped data has been written to '{output_csv}'")
