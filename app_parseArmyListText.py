import pandas as pd 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
# https://medium.com/analytics-vidhya/python-selenium-all-mouse-actions-using-actionchains-197530cf75df
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import selenium_utils as su 
import ParserUtilities as pu 

units_union_df = pd.DataFrame() 
factions_union_df = pd.DataFrame() 
event_df = pd.read_csv( "_DONE_event_army_lists_progress.csv" )
#event_df = pd.read_csv( "Dv3LDfBRAU_event_data_badParsing.csv") 
event_df.reset_index() 

debugCount = 0 
for index, row in event_df.iterrows():
                
    listUrl = row["list_url"] 
    eventId = row["event"]
    slashIndex = listUrl.rfind( "/")
    listId = listUrl[ slashIndex + 1 : ]
    #print( 'loading list ', listId )
    #https://www.bestcoastpairings.com/list/DWPNWKX8CK

    army_list = row [ "full_list_text" ] 
    if isinstance(army_list, str) :
        units, faction = pu.parseListString( army_list , listId )

        units_df = pd.json_normalize( units ) 
        units_df["eventId"] = eventId
        units_union_df = pd.concat( [ units_union_df , units_df ] )

        factions_df = pd.json_normalize( faction )
        factions_df["eventId"] = eventId
        factions_union_df = pd.concat( [ factions_union_df , factions_df  ] )

        #units_df.to_csv(f'listParse_units_{eventId}.csv')
        #factions_df.to_csv(f'listParse_factions_{eventId}.csv')
        debugCount = debugCount + 1 
    
         
units_union_df.to_csv('listParse_units.csv')
factions_union_df.to_csv('listParse_factions.csv')
   
