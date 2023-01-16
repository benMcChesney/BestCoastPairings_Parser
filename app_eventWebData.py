from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
# https://medium.com/analytics-vidhya/python-selenium-all-mouse-actions-using-actionchains-197530cf75df
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd 


event_guid = "ZMe2dZaoUv"
url = f"https://www.bestcoastpairings.com/event/{event_guid}?active_tab=roster"
driver = webdriver.Edge(executable_path='C:/lab/bestcoastpairings_parser/edgedriver_win64/msedgedriver.exe')
driver.get( url )

try:
    elem = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.ID, "Element_to_be_found")) #This is a dummy element
    )
    htmlCode = driver.page_source
    soup=BeautifulSoup(htmlCode, "html.parser")

    soup.find('//*[@id="undefined-tabpanel-0"]/div/div[2]/div/div/div/div[1]/div')
    print('debugger')
   
except : 
    #print( "passing" )
    print("button not found" )
    doLoop = -2 
    pass 
    
finally:
    print('time pass')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

print("debugger")




###
# location 
## mui-component-select-location
login = driver.find_element_by_xpath( '//*[@id="root"]/div/div[1]/header/div/div[3]/button')


actions = ActionChains(driver)
actions.move_to_element(login)
actions.click(login)
actions.pause(3)
actions.perform()

import configparser
config = configparser.ConfigParser()
config.sections()
config.read('settings.ini')


# logging in 
user  = driver.find_element_by_xpath("//input[@id='mui-3']")
pw = driver.find_element_by_xpath("//input[@id='mui-4']")
checkbox = driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div[1]/main/div/form/div[1]/div[4]/label/span[1]/input')
btn = driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div[1]/main/div/form/div[1]/div[6]/button')

actions = ActionChains( driver ); 
actions.pause( 3 )
actions.send_keys_to_element(user, config['bcp']['user']  )
actions.send_keys_to_element(pw, config['bcp']['pw'] )
actions.move_to_element( checkbox )
actions.click( checkbox )
actions.pause( 2 )
actions.move_to_element( btn )
actions.click( btn )
actions.pause( 6 )
actions.perform() 


#driver.get( url )


try:
    elem = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "Element_to_be_found")) #This is a dummy element
        )
except : 
    pass 
finally:
    print('time pass')

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
df = pd.DataFrame( army_lists )
df.to_csv( f"event_{event_guid}_army_lists.csv ")
print( "debugger") ; 
