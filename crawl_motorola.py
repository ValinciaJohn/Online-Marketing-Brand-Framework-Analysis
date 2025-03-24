from neo4j import GraphDatabase
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

# Function to extract all outbound links from a given URL
def extract_links(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all anchor (<a>) tags with 'href' attribute
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            # Resolve relative URLs
            full_url = urljoin(url, href)
            # Add only valid http/https links
            if full_url.startswith('http'):
                links.add(full_url)
        return links
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return set()

# Sample search engine results (dictionary of search engine to list of URLs)
urls ={ "Google Results for Motorola smartphone": [
        "https://www.motorola.com/us/smartphones",
        "https://www.reddit.com/r/motorola/comments/11yjtio/how_good_are_motorola_phones_really/",
        "https://www.motorola.com/us/",
        "https://www.reddit.com/r/Android/comments/19bcosq/lenovo_bets_its_motorola_smartphone_brand_will_be/",
        "https://www.zdnet.com/article/i-wore-motorolas-bendable-smartphone-watch-hybrid-and-it-left-me-all-kinds-of-confused/",
        "https://www.verizon.com/smartphones/motorola/",
        "https://www.wired.com/story/best-motorola-phones/",
        "https://forums.lenovo.com/t5/Moto-G5-Moto-G5-Plus/Moto-smartphones-with-removable-battery-in-2023/m-p/5245119",
        "https://mea.motorola.com/smartphones-moto-edge-40/p",
        "https://www.walmart.com/browse/cell-phones/motorola-phones/1105910_7551331_4278347",
        "https://www.motorola.co.uk/smartphones",
        "https://en.wikipedia.org/wiki/Motorola_Mobility",
        "https://www.washingtonpost.com/news/innovations/wp/2013/10/31/why-i-dumped-my-smartphone-for-a-7-year-old-motorola-razr/",
        "https://en-us.support.motorola.com/app/software-upgrade",
        "https://us.motorola.com/smartphones-moto-g-stylus-5g-gen-4/p",
        "https://en-emea.support.motorola.com/app/answers/detail/a_id/160550/~/smart-connect-compatibility-chart",
        "https://www.motorola.in/",
        "https://we.motorola.com/smartphones-moto-e-13/p",
        "https://www.lenovo.com/us/en/d/motorola-smartphones/",
        "https://news.lenovo.com/pressroom/press-releases/motorola-redefines-possible-ai-adaptive-display-tech-world-2023/"
    ],
     "Yahoo Results for Motorola smartphone": [
        "https://www.motorola.com/us/smartphones",
        "https://images.search.yahoo.com/search/images?p=Motorola+smartphone",
        "https://www.motorola.com/us/smartphones-moto-g-5g-gen-2/p?skuId=894",
        "https://news.search.yahoo.com/search?p=Motorola+smartphone&fr2=p%3As%2Cv%3Aw%2Cm%3Anewsdd_sna_t%2Cct%3Anuwa",
        "https://us.motorola.com/smartphones-2",
        "https://www.motorola.com/us/smartphones-moto-g-5g-gen-3/p",
        "https://us.motorola.com/",
        "https://wwwuat.motorola.com/us/smartphones",
        "https://www.androidcentral.com/best-motorola-phones"
    ],
    "Bing Results for Motorola smartphone": [
        "https://www.motorola.com/us/smartphones",
        "https://us.motorola.com/smartphones-2",
        "https://www.motorola.com/us/smartphones-moto-g-5g-gen-3/p",
        "https://wwwuat.motorola.com/us/smartphones",
        "https://us.motorola.com/",
        "https://www.techradar.com/news/best-moto-phones",
        "https://www.bestbuy.com/site/brands/motorola/pcmcat159400050006.c?id=pcmcat159400050006"
    ],
    }

# Connect to Neo4j
uri = "bolt://localhost:7687"  # Adjust based on your Neo4j instance
driver = GraphDatabase.driver(uri, auth=("neo4j", "Akshaya."))

def create_search_engine_node(tx, engine_name):
    query = """
    MERGE (e:SearchEngine {name: $engine_name})
    RETURN e
    """
    tx.run(query, engine_name=engine_name)

def create_webpage_node(tx, url):
    query = """
    MERGE (w:WebPage {url: $url})
    RETURN w
    """
    tx.run(query, url=url)

def create_link_relationship(tx, parent_url, child_url):
    query = """
    MATCH (parent:WebPage {url: $parent_url})
    MATCH (child:WebPage {url: $child_url})
    MERGE (parent)-[:LINKS_TO]->(child)
    """
    tx.run(query, parent_url=parent_url, child_url=child_url)

def create_search_relationship(tx, engine_name, page_url):
    query = """
    MATCH (e:SearchEngine {name: $engine_name})
    MATCH (w:WebPage {url: $page_url})
    MERGE (e)-[:RETURNS]->(w)
    """
    tx.run(query, engine_name=engine_name, page_url=page_url)

def store_relationships_in_neo4j(relationships):
    with driver.session() as session:
        for engine_name, urls in relationships.items():
            print(f"Creating Search Engine Node: {engine_name}")  # Debugging info
            session.write_transaction(create_search_engine_node, engine_name)
            for url in urls:
                print(f"Processing URL: {url} for Engine: {engine_name}")  # Debugging info
                session.write_transaction(create_webpage_node, url)
                
                # Create relationship between Search Engine and WebPage (RETURNS relationship)
                session.write_transaction(create_search_relationship, engine_name, url)
                
                # Extract outbound links and create link relationships
                outbound_links= extract_links(url)
                for link in outbound_links:
                    print(f"Creating link from {url} to {link}")  
                    session.write_transaction(create_webpage_node, link)
                    session.write_transaction(create_link_relationship, url, link)

                    

store_relationships_in_neo4j(urls)
# Close the Neo4j connectio
driver.close()
