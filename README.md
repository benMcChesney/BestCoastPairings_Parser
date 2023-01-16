# BestCoastPairings_Parser
# 2023-01-15

core concept is to web scrape BCP to get enough meta data to do some analysis. 


1. app_scrapeWebData
    - TODO : add start / end params 
    - opens web browsers types in info , selects AoS searches
    - on results page - hits "load more" button until it no longer appears
    - stores all events links in csv 

2. app_eventWebData
    - 