import pandas as pd
from collections import defaultdict

# Sample dictionary of URLs from different search engine results
urls = {
    "Google Results for Samsung smartphone": [
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
df.to_csv("export_s.csv", index=False)

print("PageRank data has been successfully exported to export_s.csv!")
