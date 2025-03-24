import requests
from bs4 import BeautifulSoup
from neo4j import GraphDatabase

# Connect to Neo4j Database
uri = "bolt://localhost:7687"
username = "neo4j"
password = "your_password_here"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Function to create a Search Engine node
def create_search_engine_node(tx, engine_name):
    query = """
    MERGE (e:SearchEngine {name: $engine_name})
    """
    tx.run(query, engine_name=engine_name)
    print(f"Inserted/Updated Search Engine: {engine_name}")

# Function to create a Page node with URL and page rank
def create_page_node(tx, page_url, page_rank, title=None):
    query = """
    MERGE (p:Page {url: $page_url})
    SET p.page_rank = $page_rank, p.title = $title
    """
    tx.run(query, page_url=page_url, page_rank=page_rank, title=title)
    print(f"Inserted/Updated Page: {page_url} with rank {page_rank}")

# Function to create a relationship between Search Engine and Page nodes
def create_search_result_relationship(tx, engine_name, page_url):
    query = """
    MATCH (e:SearchEngine {name: $engine_name})
    MATCH (p:Page {url: $page_url})
    MERGE (e)-[:RESULTS_IN]->(p)
    """
    tx.run(query, engine_name=engine_name, page_url=page_url)
    print(f"Created relationship between {engine_name} and {page_url}")

# Function to extract outbound links from a page
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def extract_links_from_page(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return [a['href'] for a in soup.find_all('a', href=True)]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

# Function to create a relationship between Pages that link to each other
def create_relationship(tx, source_url, target_url):
    query = """
    MATCH (a:Page {url: $source_url}), (b:Page {url: $target_url})
    MERGE (a)-[:POINT_TO]->(b)
    """
    tx.run(query, source_url=source_url, target_url=target_url)
    print(f"Created POINT_TO relationship between {source_url} and {target_url}")

# Insert all pages into Neo4j
def insert_search_results(search_results, driver):
    with driver.session() as session:
        for engine, links in search_results.items():
            session.execute_write(create_search_engine_node, engine)
            for i, url in enumerate(links):
                page_rank = i + 1
                session.execute_write(create_page_node, url, page_rank)

                # Extract and create relationships for outbound links that are also in the dataset
                outbound_links = extract_links_from_page(url)
                for outbound_url in outbound_links:
                    if outbound_url in search_results['Google'] + search_results['Yahoo'] + search_results['Bing']:
                        session.execute_write(create_relationship, url, outbound_url)

# Function to run the PageRank algorithm in Neo4j
def run_pagerank(tx):
    query = """
    CALL gds.pageRank.stream('Page', {
      relationshipProjection: {
        POINT_TO: {
          type: 'POINT_TO',
          orientation: 'NATURAL'
        }
      }
    })
    YIELD nodeId, score
    RETURN gds.util.asNode(nodeId).url AS url, score
    ORDER BY score DESC
    """
    result = tx.run(query)
    return [(record["url"], record["score"]) for record in result]

# Function to display PageRank results
def display_pagerank_results(driver):
    with driver.session() as session:
        pagerank_results = session.execute_read(run_pagerank)
    
    # Print the PageRank results
    for url, score in pagerank_results:
        print(f"Page: {url}, PageRank: {score}")

# Full workflow automation
def full_workflow(search_results):
    # Insert search results into Neo4j
    insert_search_results(search_results, driver)
    
    # Run PageRank and display results
    display_pagerank_results(driver)

# Search results dictionary
search_results = {
    "Google": [
        "https://www.samsung.com/us/smartphones/",
        "https://www.samsung.com/us/",
        # Other URLs...
    ],
    "Yahoo": [
        "https://www.samsung.com/us/smartphones/",
        "https://images.search.yahoo.com/search/images?p=Samsung+smartphone",
        # Other URLs...
    ],
    "Bing": [
        "https://www.samsung.com/us/smartphones/",
        "https://www.samsung.com/us/mobile/phones/all-phones/",
        # Other URLs...
    ]
}

# Run the full workflow
full_workflow(search_results)

# Close the Neo4j driver
driver.close()
