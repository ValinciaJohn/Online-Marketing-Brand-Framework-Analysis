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
urls ={ "Google Results for LG smartphone": [
        "https://www.lg.com/levant_en/smartphones",
        "https://www.reddit.com/r/LGV60/comments/169p8g2/lg_to_start_making_mobile_phones_again_if/",
        "https://www.lg.com/us/cell-phones",
        "https://www.reddit.com/r/LGV60/comments/xlnema/now_that_lg_isnt_making_smart_phones_anymore/",
        "https://www.lg.com/levant_en/mobile-phones",
        "https://www.reddit.com/r/Smartphones/comments/rucn3g/need_help_with_alternatives_to_the_awesomeness_of/",
        "https://www.forbes.com/sites/ianmorris/2014/07/11/lg-g3-review-the-perfect-smartphone/",
        "https://www.reddit.com/r/TIdaL/comments/jzgy7s/mqa_files_with_lg_mobile_phones/",
        "https://www.quora.com/Are-lg-phones-good",
        "https://www.reddit.com/r/LGV60/comments/12c8d2y/lg_is_still_selling_phones_in_korea_and_its_5g/",
        "https://www.gsmarena.com/lg-phones-20.php",
        "https://www.reddit.com/r/Android/comments/mlklc5/mkbhd_why_did_lg_phones_really_die/",
        "https://www.walmart.com/browse/cell-phones/lg-phones/1105910_7551331_3916202",
        "https://audiosciencereview.com/forum/index.php?threads/review-and-audio-measurement-of-lg-g7-thinq-smartphone.4468/",
        "https://www.etdphotography.com/blog/2015/7/10/lg-g4-smartphone-camera-review-dslr-replacement",
        "https://www.statista.com/chart/24569/global-smartphone-market-share/",
        "https://www.amazon.com/LG-Smartphone/s?k=LG+Smartphone",
        "https://community.hsn.com/forums/customer-service-help-support/lg-smartphone-tracfone-is-going-out-of-business/1080732/",
        "https://www.techradar.com/news/best-lg-phones",
        "https://www.androidpolice.com/lg-electronics-pivoting-to-global-entertainment/"
    ],
     "Yahoo Results for LG smartphone": [
        "https://www.lg.com/us/android-phones",
        "https://www.lg.com/us/cell-phones",
        "https://www.lg.com/us/smartphones/view-all",
        "https://www.bestbuy.com/site/shop/lg-phones",
        "https://www.gsmarena.com/lg-phones-20.php",
        "https://www.techradar.com/news/best-lg-phones",
        "https://www.walmart.com/browse/cell-phones/lg-phones/1105910_7551331_3916202"
    ],
     "Bing Results for LG smartphone": [
        "https://www.lg.com/us/android-phones",
        "https://www.lg.com/us/cell-phones",
        "https://www.lg.com/us/smartphones/view-all",
        "https://www.bestbuy.com/site/shop/lg-phones",
        "https://www.techradar.com/news/best-lg-phones",
        "https://www.androidauthority.com/best-lg-phones-775532/",
        "https://www.gsmarena.com/lg-phones-20.php"
    ]

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

# Function to store the extracted relationships in Neo4j
# Function to store the extracted relationships in Neo4j
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
                    print(f"Creating link from {url} to {link}")  # Debugging info
                    session.write_transaction(create_webpage_node, link)
                    session.write_transaction(create_link_relationship, url, link)

                    

store_relationships_in_neo4j(urls)
# Close the Neo4j connectio
driver.close()
