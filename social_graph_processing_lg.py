import pandas as pd
from collections import defaultdict

# Sample dictionary of URLs from different search engine results
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
df.to_csv("export_lg.csv", index=False)

print("PageRank data has been successfully exported to export_lg.csv!")
