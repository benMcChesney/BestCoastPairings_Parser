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

pd.DataFrame() 

def viewAllListResults( driver ) :
    try:
        elem = WebDriverWait(driver, 10 ).until(
            EC.presence_of_element_located((By.NAME, "Element_to_be_found")) #This is a dummy element
            )
        #//
        resultsButton = driver.find_elements_by_tag_name( 'input')[1]
        actions = ActionChains( driver ); 
        actions.pause(1) 
        actions.move_to_element( resultsButton ) 
        actions.click() 
        actions.pause( 1 ) 
        actions.send_keys( 'A')  
        actions.send_keys( Keys.ENTER )
        actions.perform() 
    except : 
        pass 
    finally:
        print('time pass')

    try:
        driver.implicitly_wait( 3 )
        resultsButton = driver.find_elements_by_tag_name( 'input')[1]
        actions = ActionChains( driver ); 
        actions.pause( 2 ) 
        actions.move_to_element( resultsButton ) 
        actions.click() 
        actions.pause( 1 ) 
        actions.send_keys( 'A')  
        actions.send_keys( Keys.ENTER )
        actions.perform() 
    except : 
        pass 
    finally:
        print('post results found')
#local RTT
event_guid = "ZMe2dZaoUv"
#LVO 
event_guid = "GYoZGtzElR"
url = f"https://www.bestcoastpairings.com/event/{event_guid}?active_tab=roster"
driver = webdriver.Edge(executable_path='C:/lab/bestcoastpairings_parser/edgedriver_win64/msedgedriver.exe')
driver.maximize_window() 
driver.get( url )
su.waitSync( 2 ) 
su.loginAndWait( driver ,  'settings.ini' )
#su.waitSync( 10 ) 
driver.implicitly_wait( 60 )
viewAllListResults( driver )
driver.implicitly_wait( 5 ) 
#su.waitSync( 15 )


htmlCode = driver.page_source
soup=BeautifulSoup(htmlCode, "html.parser")

list_links = soup.find_all('a')
army_lists = [] 
for li in list_links : 
    url = li.attrs['href'] ; 
    if "list" in url :
        obj = {} 
        obj = { 
                "event" : event_guid 
                , "list_url" : f"https://www.bestcoastpairings.com{url}" }
        army_lists.append( obj )

for al in army_lists :
    driver.get( al["list_url"])
    try:
        elem = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "Element_to_be_found")) #This is a dummy element
            )
    except : 
        pass 
    finally:
        print('time pass')
    full_list_text = driver.find_element_by_class_name( "list" ).text
    al["full_list_text"] = full_list_text 
#foundLists = soup.find_all("a", string=["View List"])
df = pd.DataFrame( pd.json_normalize(army_lists) )
df.to_csv( f"event_{event_guid}_army_lists.csv ")

# now get placings data
# https://www.bestcoastpairings.com/event/ZMe2dZaoUv?active_tab=pairings&round=1

# trying to get all the pairings data 
print( "debugger") ; 
