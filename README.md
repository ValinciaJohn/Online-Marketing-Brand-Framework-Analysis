# 🌐 Online Marketing Brand Framework Analysis  

## 📌 Project Overview  
This project leverages **web scraping**, **network analysis**, and **PageRank** using **Python** and **Neo4j** to create a **graph-based representation** of search engine results. It extracts pages and outbound links from search engines (**Google**, **Yahoo**, **Bing**) to analyze their relationships, forming a network of linked web pages. The goal is to identify the most effective websites and social media channels for brand advertisements and assess their influence on brand popularity.  

---

## 🔧 Technologies Used  
- **Python:** For scripting, data processing, and PageRank implementation.  
- **BeautifulSoup:** Web scraping to extract page content and links.  
- **Requests:** Making HTTP requests to search engines.  
- **Neo4j:** Graph database for storing and analyzing the network of linked web pages.  
- **NetworkX:** Network visualization and basic graph operations.  

---

## 🔎 How It Works  
### 1. Web Scraping  
- **Search Engine Queries:** Sends search requests to Google, Yahoo, and Bing.  
- **HTML Parsing:** Uses BeautifulSoup to extract page links and outbound links from search results.  
- **Data Storage:** Scraped data is saved in the `data/` directory for further processing.  

### 2. Network Analysis  
- **Graph Construction:** Links are modeled as directed graphs using Neo4j.  
- **PageRank Calculation:**  
  - Implemented using Neo4j's built-in algorithms.  
  - Python's NetworkX is used for comparison.  

---

## 🧠 PageRank Calculation Techniques  
PageRank is calculated using **three techniques** to analyze the influence of webpages:  

### 1. Social Graph Processing  
- PageRank is assigned based on the **degree** (sum of in-degree and out-degree) of each webpage.  
- Higher in-degree from search engines indicates greater influence.  
- Formula:  
  \[
  PR_{sg} = \sum (\text{in-degree} + \text{out-degree} - 1)
  \]  
  Where **PRsg** is the PageRank based on social graph.  

---

### 2. Text Edge Processing  
- Analyzes the frequency of predefined terms and concepts related to the brand/product.  
- Filters out stop-words and applies stemming techniques.  
- Measures relationships like "good battery," "excellent camera" to determine edge strength.  
- Formula:  
  \[
  PR_{TE} = \text{Frequency of relationships between objects}
  \]  
  Where **PRTE** is the PageRank based on text edge processing.  

---

### 3. Sentiment Analysis  
- Analyzes positive, negative, and neutral sentiments from web pages and social media reviews.  
- Uses **WordStat sentiment dictionary** and considers negation handling for accurate sentiment classification.  
- Formula:  
  \[
  PR_{SA} = (a \times \text{positive probability}) + (b \times \text{neutral probability}) - (c \times \text{negative probability})
  \]  
  Where **a**, **b**, and **c** are weights with **a > b > c**, and **PRSA** is the PageRank based on sentiment analysis.  

---

### 4. Cumulative PageRank  
- The final cumulative PageRank for a webpage is the sum of the three methods:  
  \[
  PR_{c} = PR_{sg} + PR_{TE} + PR_{SA}
  \]  
  Where **PRc** is the overall cumulative PageRank.  

---

## 📊 Results and Analysis
- **Top Influential Pages:** Pages with the highest cumulative PageRank values indicate strong influence within the network.
- **Network Visualization:** Visualizes the connectivity and impact of each page.
- **Search Engine Comparison:** Highlights differences in link distribution across Google, Yahoo, and Bing.
- **Sentiment Insights:** Analyzes sentiment trends to assess public perception of brands.
