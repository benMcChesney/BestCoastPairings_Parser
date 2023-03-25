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




driver = su.createDriver( 'C:/lab/bestcoastpairings_parser/edgedriver_win64/msedgedriver.exe' )
driver.get( 'https://www.bestcoastpairings.com/login') 
su.waitSync( 3 )
su.loginAndWait( driver, "settings.ini" , 4 )
eventObjs = []

event_df = pd.read_csv( "events_links.csv" )
#event_df = pd.read_csv( "Dv3LDfBRAU_event_data_badParsing.csv") 
event_df.reset_index() 
#https://www.bestcoastpairings.com/event/tFIPqaYN2S
debugCount = 0 
for index, row in event_df.iterrows():
    eventId = row["url"][40:]
    obj = su.getEventDetails( driver, eventId )
    eventObjs.append( obj )    
    #print(f"@ {index}/{len(event_df)}")
    #debugCount = debugCount + 1
    #if debugCount > 5 : 
    #    break 
event_df = pd.json_normalize( eventObjs )
event_df.to_csv( "event_meta.csv" )

i = 0 

  


# address1 = //*[@id="undefined-tabpanel-0"]/div/div[2]/div/div/div/div[1]/div/div[4]/a/p[1]
# address2 = //*[@id="undefined-tabpanel-0"]/div/div[2]/div/div/div/div[1]/div/div[4]/a/p[2]
# address3 = //*[@id="undefined-tabpanel-0"]/div/div[2]/div/div/div/div[1]/div/div[4]/a/p[3]
# ticketPrice = eventObj[ 'ticketPrice' ] = driver.get_element_by_xpath('//*[@id="undefined-tabpanel-0"]/div/div[2]/div/div/div/div[2]/div[1]/div[1]/h5' ).text
# eventName = //*[@id="undefined-tabpanel-0"]/div/div[2]/div/div/div/div[1]/div/div[1]/h4
# event Owner //*[@id="undefined-tabpanel-0"]/div/div[2]/div/div/div/div[1]/div/div[5]/h5
# date end = //*[@id="undefined-tabpanel-0"]/div/div[2]/div/div/div/div[1]/div/div[3]/h5[1]

