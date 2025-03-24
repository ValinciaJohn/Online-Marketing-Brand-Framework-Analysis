from neo4j import GraphDatabase
import requests
from bs4 import BeautifulSoup

# Connect to Neo4j Database
uri = "bolt://localhost:7687"
username = "neo4j"
password = "Akshaya."

driver = GraphDatabase.driver(uri, auth=(username, password))

# Function to create or update a Search Engine node
def create_search_engine_node(tx, engine_name):
    query = """
    MERGE (e:SearchEngine {name: $engine_name})
    """
    tx.run(query, engine_name=engine_name)
    print(f"Inserted/Updated Search Engine: {engine_name}")

# Function to create or update a Page node
def create_page_node(tx, page_url):
    query = """
    MERGE (p:Page {url: $page_url})
    """
    tx.run(query, page_url=page_url)
    print(f"Inserted/Updated Page: {page_url}")
    return page_url  # Return the URL for later use

# Function to create a relationship between Search Engine and Page nodes
def create_search_result_relationship(tx, engine_name, page_url):
    query = """
    MATCH (e:SearchEngine {name: $engine_name})
    MATCH (p:Page {url: $page_url})
    MERGE (e)-[:RESULTS_IN]->(p)
    """
    tx.run(query, engine_name=engine_name, page_url=page_url)
    print(f"Created relationship between {engine_name} and {page_url}")

# Function to create a relationship between parent and child pages
def create_parent_child_relationship(tx, parent_url, child_url):
    query = """
    MATCH (p:Page {url: $parent_url})
    MATCH (c:Page {url: $child_url})
    MERGE (p)-[:POINT_TO]->(c)
    """
    tx.run(query, parent_url=parent_url, child_url=child_url)
    print(f"Created relationship between {parent_url} and {child_url}")

# Function to scrape pages and create nodes and relationships
def scrape_and_insert(url, search_engine_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find div with id='web'
    web_div = soup.find('div', id='web')
    
    # Process 'ol' tags within the web div
    if web_div:
        ol_tags = web_div.find_all('ol')
        for ol in ol_tags:
            li_tags = ol.find_all('li')
            for li in li_tags:
                # Extract href from <a> tags inside li
                a_tags = li.find_all('a', href=True)
                for a in a_tags:
                    href = a['href']
                    if href:  # Ensure href is not None
                        # Create or update the Page node
                        page_url = create_page_node(driver.session(), href)
                        # Create a relationship from the search engine to the page
                        create_search_result_relationship(driver.session(), search_engine_name, page_url)

                        # Check for other href links in this page
                        outbound_links = extract_links_from_page(href)
                        for outbound_url in outbound_links:
                            # Create or update the Page node for outbound links
                            create_page_node(driver.session(), outbound_url)
                            # Create a relationship between the parent and child
                            create_parent_child_relationship(driver.session(), page_url, outbound_url)

# Function to extract outbound links from a given page
def extract_links_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return [a['href'] for a in soup.find_all('a', href=True)]

search_results = {
    "Google": [
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
        "https://www.lg.com/levant_en/smartphones",
        "https://www.reddit.com/r/LGV60/comments/169p8g2/lg_to_start_making_mobile_phones_again_if/",
        "https://www.lg.com/us/cell-phones",
        "https://www.reddit.com/r/LGV60/comments/xlnema/now_that_lg_isnt_making_smart_phones_anymore/",
        "https://www.lg.com/levant_en/mobile-phones",
        "https://www.reddit.com/r/Smartphones/comments/rucn3g/need_help_with_alternatives_to_the_awesomeness_of/",
        "https://www.forbes.com/sites/ianmorris/2014/07/11/lg-g3-review-the-perfect-smartphone/",
        "https://www.reddit.com/r/TIdaL/comments/jzgy7s/mqa_files_with_lg_mobile_phones/",
        "https://www.quora.com/Are-lg-phones-good",
        "https://www.reddit.com/r/LGV60/comments/12c8d2y/lg_is_still_selling_phones_in_korea_and_its_5g/"
    ],
    "Yahoo":[
        "https://www.samsung.com/us/smartphones/",
        "https://images.search.yahoo.com/search/images?p=Samsung+smartphone",
        "https://www.samsung.com/us/mobile/phones/all-phones/",
        "https://www.samsung.com/us/mobile/",
        "https://www.bestbuy.com/site/mobile-cell-phones/samsung-galaxy/pcmcat305200050001.c?id=pcmcat305200050001",
        "https://www.bestbuy.com/site/samsung-galaxy/all-samsung-galaxy-phones/pcmcat1661803373461.c?id=pcmcat1661803373461",
        "https://www.samsung.com/us/smartphones/",
        "https://news.samsung.com/us/samsung-galaxy-s21-ultra-unpacked-2021-ultimate-smartphone-experience-designed-epic/",
        "https://www.amazon.com/Samsung-Galaxy-S21-5G-Snapdragon/dp/B092CFFM84",
        "https://www.motorola.com/us/smartphones",
        "https://images.search.yahoo.com/search/images?p=Motorola+smartphone",
        "https://www.motorola.com/us/smartphones-moto-g-5g-gen-2/p?skuId=894",
        "https://news.search.yahoo.com/search?p=Motorola+smartphone&fr2=p%3As%2Cv%3Aw%2Cm%3Anewsdd_sna_t%2Cct%3Anuwa",
        "https://us.motorola.com/smartphones-2",
        "https://www.motorola.com/us/smartphones-moto-g-5g-gen-3/p",
        "https://us.motorola.com/",
        "https://wwwuat.motorola.com/us/smartphones",
        "https://www.androidcentral.com/best-motorola-phones",
        "https://www.lg.com/us/android-phones",
        "https://www.lg.com/us/cell-phones",
        "https://www.lg.com/us/smartphones/view-all",
        "https://www.bestbuy.com/site/shop/lg-phones",
        "https://www.gsmarena.com/lg-phones-20.php",
        "https://www.techradar.com/news/best-lg-phones",
        "https://www.walmart.com/browse/cell-phones/lg-phones/1105910_7551331_3916202"
    ],
   "Bing": [
        "https://www.samsung.com/us/smartphones/",
        "https://www.samsung.com/us/mobile/phones/all-phones/",
        "https://www.samsung.com/us/mobile/",
        "https://www.bestbuy.com/site/samsung-galaxy/all-samsung-galaxy-phones/pcmcat1661803373461.c?id=pcmcat1661803373461",
        "https://www.cnet.com/tech/mobile/best-samsung-galaxy-phone/",
        "https://news.samsung.com/us/samsung-galaxy-s21-ultra-unpacked-2021-ultimate-smartphone-experience-designed-epic/",
        "https://www.amazon.com/Samsung-Galaxy-S21-5G-Snapdragon/dp/B092CFFM84",
        "https://www.motorola.com/us/smartphones",
        "https://us.motorola.com/smartphones-2",
        "https://www.motorola.com/us/smartphones-moto-g-5g-gen-3/p",
        "https://wwwuat.motorola.com/us/smartphones",
        "https://us.motorola.com/",
        "https://www.techradar.com/news/best-moto-phones",
        "https://www.bestbuy.com/site/brands/motorola/pcmcat159400050006.c?id=pcmcat159400050006",
        "https://www.lg.com/us/android-phones",
        "https://www.lg.com/us/cell-phones",
        "https://www.lg.com/us/smartphones/view-all",
        "https://www.bestbuy.com/site/shop/lg-phones",
        "https://www.techradar.com/news/best-lg-phones",
        "https://www.androidauthority.com/best-lg-phones-775532/",
        "https://www.gsmarena.com/lg-phones-20.php"
    ]
}

# Start the process
with driver.session() as session:
    for engine_name, urls in search_results.items():
        create_search_engine_node(session, engine_name)  # Create the search engine node
        for url in urls:
            scrape_and_insert(url, engine_name)

# Close the Neo4j driver when done
driver.close()
