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
pd.DataFrame() 

#local RTT

event_df = pd.read_csv( "events_links.csv" )
#event_df = pd.read_csv( "Dv3LDfBRAU_event_data_badParsing.csv") 
event_df.reset_index() 
lists_df = pd.DataFrame( )

debugCount = 0 
driver = su.createDriver()

debugMax = 20 
for index, row in event_df.iterrows():
    #print(row['c1'], row['c2'])
    eventUrl = row["url"]
    if debugCount == 0 : 
        driver.get( eventUrl )
        su.waitSync( 5 )
        su.loginAndWait(driver,  'settings.ini' , 5 )  
    slashIndex = eventUrl.rfind( "/")
    eventId = eventUrl[ slashIndex + 1 : ]
    print( 'loading event ', eventId )

    linksList = su.loadEventList( driver , eventId )
    if len(linksList) > 6 : 
        ret_df = su.scrapeArmyListFromURL( driver, linksList )
        prevLen = len( lists_df )
        lists_df = pd.concat( [ lists_df , pd.json_normalize( ret_df ) ] )
        lists_df.to_csv( f"./armyList/event_{eventId}_armyLists.csv")
        print( f"appending data {prevLen} -> {len(lists_df)} with {len(ret_df)} rows" )
        # trying to get all the pairings data 
        print( "end of browser ") ; 
        ret_df.to_csv( f"event_army_lists_progress.csv ")
    debugCount = debugCount + 1 
    if debugCount > debugMax : 
        break

ret_df.to_csv( f"event_army_lists_events.csv ")