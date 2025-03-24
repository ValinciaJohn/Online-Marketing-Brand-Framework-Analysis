import requests

def google_search(query, api_key, cse_id, num_results=20):
    links = []
    
    # Iterate in steps of 10, as Google Custom Search returns a max of 10 results per request
    for start_index in range(1, num_results + 1, 10):
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'q': query,
            'key': api_key,
            'cx': cse_id,
            'num': min(num_results - len(links), 10),  # Number of results per request
            'start': start_index  # Start index for pagination
        }
        response = requests.get(url, params=params)
        results = response.json()

        # Extracting URLs from the search results
        for item in results.get('items', []):
            links.append(item['link'])

        # Stop if we've collected the desired number of results
        if len(links) >= num_results:
            break

    return links

API_KEY = 'AIzaSyB7kYCCFLiiOW4g6bPf-srB5LwKKRitoRo'  # Replace with your actual Google API key
CSE_ID = 'e639ae22e69c64369'  # Replace with your actual CSE ID
queries = ["Samsung smartphone", "Motorola smartphone", "LG smartphone"]

google_results = {query: google_search(query, API_KEY, CSE_ID, num_results=20) for query in queries}

# Print the results
for query, urls in google_results.items():
    print(f"Results for {query}:")
    for url in urls:
        print(url)
