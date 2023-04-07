# BestCoastPairings_Parser
# 2023-01-15

core concept is to web scrape BCP to get enough meta data to do some analysis. 


1. app_scrapeWebData
    - TODO : add start / end params 
    - opens web browsers types in info , selects AoS searches
    - on results page - hits "load more" button until it no longer appears
    - stores all events links in OUTPUT CSV - events.csv 
    - *** to do return delta CSV name

2. app_eventWebData
    - input CSV 
    - army list per event concatted
    - OUTPUT CSV event_army_lists_events.csv

3. app_parserEVent.py
    - input CSV 
    - get all metadata associated with events 
    - OUTPUT CSV  event_meta.csv

4. app_parsePlacings.py
    - INPUT CSV
    - get "placings" from each event
    - OUTPUT CSV placingsData_progress.csv

5. app_parseRounds.py
    - INPUT CSV
    - get each round from each event 
    - OUTPUT CSV pairingsData.csv

6. app_parseArmyList.py
    - INPUT CSV 
    - parse local CSV army lists
    - OUTPUT CSV 1 - listParse_units.csv CSV 
    - OUTPUT CSV 2 - listParse_factions.csv CSV 

