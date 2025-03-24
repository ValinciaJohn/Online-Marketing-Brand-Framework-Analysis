import requests
from bs4 import BeautifulSoup
from neo4j import GraphDatabase

# Connect to Neo4j Database
uri = "bolt://localhost:7687"
username = "neo4j"
password = "Akshaya."
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

# Run the full workflow
full_workflow(search_results)

# Close the Neo4j driver
driver.close()
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
        "https://www.samsung.com/us/smartphones/",
        "https://www.samsung.com/us/mobile/phones/all-phones/",
        "https://www.samsung.com/us/mobile/",
        "https://www.bestbuy.com/site/samsung-galaxy/all-samsung-galaxy-phones/pcmcat1661803373461.c?id=pcmcat1661803373461",
        "https://www.cnet.com/tech/mobile/best-samsung-galaxy-phone/",
        "https://news.samsung.com/us/samsung-galaxy-s21-ultra-unpacked-2021-ultimate-smartphone-experience-designed-epic/",
        "https://www.amazon.com/Samsung-Galaxy-S21-5G-Snapdragon/dp/B092CFFM84"
    ]

    }