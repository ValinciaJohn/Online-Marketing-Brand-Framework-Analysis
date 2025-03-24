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

# Connect to Neo4j
uri = "bolt://localhost:7687"  # Adjust based on your Neo4j instance
driver = GraphDatabase.driver(uri, auth=("neo4j", "akshval."))

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
# Close the Neo4j connection
driver.close()
