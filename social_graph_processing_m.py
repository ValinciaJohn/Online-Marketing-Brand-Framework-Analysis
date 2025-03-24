import pandas as pd
from collections import defaultdict

# Sample dictionary of URLs from different search engine results
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

# Initialize dictionaries to store in-degree, out-degree, and total degree
in_degree = defaultdict(int)
out_degree = defaultdict(int)

# Calculate in-degree (how many times each URL appears)
for search_results in urls.values():
    for url in search_results:
        in_degree[url] += 1

# Calculate out-degree (how many URLs are listed in each search engine result)
for search_results in urls.values():
    for url in search_results:
        out_degree[url] += len(search_results)

# Create a list to store the results (URL, in-degree, out-degree, page rank)
page_rank_data = []

# Calculate the PageRank based on in-degree + out-degree + 1
for url in in_degree:
    page_rank = in_degree[url] + out_degree[url] + 1
    page_rank_data.append([url, in_degree[url], out_degree[url], page_rank])

# Convert the data to a pandas DataFrame
df = pd.DataFrame(page_rank_data, columns=["URL", "In-Degree", "Out-Degree", "PageRank"])

# Sort the DataFrame by PageRank in descending order
df = df.sort_values(by="PageRank", ascending=False)

# Export the DataFrame to a CSV file
df.to_csv("export_m.csv", index=False)

print("PageRank data has been successfully exported to export_m.csv!")
