# Webscraping adidas.de
Hi. I do it because it's fun.
# The Idea
* Collect Ecommerce webstore data, to track their supply level using their webpage API.  
* I like shoes, I'm okay with Adidas, but I'm in love with webscraping.

# Kaggle
I plan to upload compiled versions of the results for data science projects.  
Let's see how frequently.  
[The Kaggle dataset](https://www.kaggle.com/datasets/tamsnd/adidas-webstore-shoe-data)
# .py Files
* **main()** collects and stores the data
* **memory_handling()** ensures that I have backup after an IP Block
* **bronze_process()** organizes the collected data

# Plan
**Getting the data**
- [x] Scraping the **German Adidas** website
- [ ] Figuring out how to stay undetectable
- [ ] Be able to scrape multiple countries data

**Building the pipeline**
- [x] Store the data locally **(SQL Server)**
- [x] Connecting the SQL Server with **MS Fabric**
- [x] Bronze -> Silver pipeline
- [ ] Silver -> Gold pipeline

**Visualization**
- [ ] Construct a daily refreshing Power BI dashboard
- [ ] With the data, answer Ecommerce questions
- [ ] Compare prices and trends across countries
