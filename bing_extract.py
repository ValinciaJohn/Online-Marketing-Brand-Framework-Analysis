import requests
from bs4 import BeautifulSoup

def bing_search(query, num_results):
    query = query.replace(' ', '+')  # format the search query
    url = f"https://www.bing.com/search?q={query}&count={num_results}"

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = []
    for result in soup.find_all('a', href=True):
        link = result['href']
        if 'http' in link:  # filter out non-http links
            links.append(link)
    
    return links

queries = ["Samsung smartphone", "Motorola smartphone", "LG smartphone"]

# Collect results for each query
bing_results = {query: bing_search(query, num_results=20) for query in queries}

# Print the results
for query, urls in bing_results.items():
    print(f"Results for {query}:")
    for url in urls:
        print(url)
    print()
