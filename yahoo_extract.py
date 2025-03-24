import requests
from bs4 import BeautifulSoup

def yahoo_search(query, num_results):
    query = query.replace(' ', '+')  # format the search query
    url = f"https://search.yahoo.com/search?p={query}&n={num_results}"

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = []
    for result in soup.find_all('a', href=True):
        link = result['href']
        if 'http' in link and 'yahoo' not in link:  # filter out internal Yahoo links
            links.append(link)
    
    return links

queries = ["Samsung smartphone", "Motorola smartphone", "LG smartphone"]

# Collect results for each query
yahoo_results = {query: yahoo_search(query, num_results=20) for query in queries}

# Print the results
for query, urls in yahoo_results.items():
    print(f"Results for {query}:")
    for url in urls:
        print(url)
    print()  
