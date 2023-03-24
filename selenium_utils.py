from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
# https://medium.com/analytics-vidhya/python-selenium-all-mouse-actions-using-actionchains-197530cf75df
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd 
from selenium.webdriver.edge.service import Service
import os



def createDriver ( exec_path ):

    # Let python handle it
    #driverNew = webdriver.Edge()
    #Se = Service("C:/lab/bestcoastpairings_parser/edgedriver_win64/msedgedriver.exe")
    #options = EdgeOptions()
    ##options.add_argument("--headless")
    #options.add_argument("disable-gpu")
    #options.add_argument('--allow-running-insecure-content')
    #options.add_argument('--ignore-certificate-errors')
    driverNew = webdriver.Edge(executable_path=exec_path, service_log_path='NUL')
    #driver.get("https://ipsis.adm.arcor.net/gui/pl/login?func=loginmask&option=nosession")

    # The proper null device option for Windows
    #driverNew = webdriver.Edge(service_log_path='NUL')
    return driverNew 
 
def viewAllListResults( driver ) :
    try:
        elem = WebDriverWait(driver, 15 ).until(
            EC.presence_of_element_located((By.TAG_NAME,  'input')) #This is a dummy element
            )
        resultsButton = driver.find_elements_by_tag_name( 'input')[1]
        #resultsButton = driver.find_elements_by_tag_name( 'input')[1]
        actions = ActionChains( driver ); 
        actions.pause(  ) 
        actions.move_to_element( resultsButton ) 
        actions.click() 
        actions.pause( 1 ) 
        actions.send_keys( 'A')  
        actions.send_keys( Keys.ENTER )
        actions.perform() 
    except : 
        pass 
    finally:
        print('time pass - view all ')

    

def waitSync( driver , waitInSeconds = 3 ) :

    try:
        elem = WebDriverWait(driver, waitInSeconds ).until(
            EC.presence_of_element_located((By.ID, "Element_to_be_found")) #This is a dummy element
            )
    except : 
        pass 
    finally:
        print('time pass')

# 'settings.ini')
def loginAndWait(driver , config_path, waitInSeconds=3 ):
    
    ###
    # location 
    ## mui-component-select-location
    login = driver.find_element_by_xpath( '//*[@id="root"]/div/div[1]/header/div/div[3]/button')
    accept = driver.find_element_by_id( 'rcc-confirm-button')
    
    actions = ActionChains(driver)
    actions.move_to_element(accept)
    actions.click(accept)
    actions.pause(1)
    actions.move_to_element(login)
    actions.click(login)
    actions.pause(1)
    actions.click(login)
    actions.pause(1)
    actions.perform()

    import configparser
    config = configparser.ConfigParser()
    config.sections()
    config.read(config_path)


    # logging in 
    try:
        user = WebDriverWait(driver, waitInSeconds ).until(
            EC.presence_of_element_located((By.NAME, "email"))
            )
        pw = WebDriverWait(driver, waitInSeconds ).until(
            EC.presence_of_element_located((By.NAME, "password"))
            )
        checkbox = WebDriverWait(driver, waitInSeconds ).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]/div[1]/main/div/form/div[1]/div[4]/label/span[1]/input'))
            )
        btn = WebDriverWait(driver, waitInSeconds ).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]/div[1]/main/div/form/div[1]/div[6]/button'))
            )
    except : 
        pass 
    finally:
        print('time pass - login')
    
    #user  = driver.find_element_by_name( "email" )
    #pw = driver.find_element_by_name("password")
    #checkbox = driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div[1]/main/div/form/div[1]/div[4]/label/span[1]/input')
    #btn = driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div[1]/main/div/form/div[1]/div[6]/button')

    actions = ActionChains( driver ); 
    actions.pause( 1 )
    actions.send_keys_to_element(user, config['bcp']['user']  )
    actions.send_keys_to_element(pw, config['bcp']['pw'] )
    actions.move_to_element( checkbox )
    actions.click( checkbox )
    actions.pause( 1 )
    actions.move_to_element( btn )
    actions.click( btn )
    actions.pause( 1 )
    actions.perform() 

    waitSync( driver , waitInSeconds ) 


def loadEventList( driver, eventId ):

    #eventUrl = row["url"]
    #slashIndex = eventUrl.rfind( "/")
    #eventId = eventUrl[ slashIndex + 1 : ]
    #print( 'loading event ', eventId )
    lists_df = pd.DataFrame() 

    url = f"https://www.bestcoastpairings.com/event/{eventId}"
    #if ( line == 0 ):
    #driver = createDriver()
    #driver.maximize_window() 
    driver.get( url )
    #waitSync( driver , 2 ) 
    #loginAndWait( driver ,  'settings.ini' )
    waitSync( driver , 2 ) 
    date = '1970-01-01'
    try :
        elem = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located( By.XPATH, '//*[@id="undefined-tabpanel-0"]/div/div[2]/div/div/div/div/div/div[3]/h5[1]' ) #This is a dummy element
            )
        date = elem.text
    except : 
        pass 
    waitSync( driver , 2 ) 

    url = f"https://www.bestcoastpairings.com/event/{eventId}?active_tab=roster"
    driver.get( url )
    viewAllListResults( driver ) 
    waitSync( driver , 5 )

    htmlCode = driver.page_source
    soup=BeautifulSoup(htmlCode, "html.parser")

    list_links = soup.find_all('a')
    army_lists = []
    for li in list_links : 
        if 'href' in li.attrs : 
            url = li.attrs['href'] ; 
            if "list" in url :
                obj = {} 
                obj = { 
                        "event" : eventId 
                        , "list_url" : f"https://www.bestcoastpairings.com{url}"
                        , "date" : date  
                    }
                army_lists.append( obj )
    return army_lists
    
    #lists_df.to_csv( f"event_army_lists.csv ")

def scrapeArmyListFromURL( driver, army_lists ):
    objList = [] 
    obj = {} 
    for al in army_lists :
        driver.get( al["list_url"])
        try:
            elem = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "list")) #This is a dummy element
               )
            #full_list_text = driver.find_element_by_class_name( "list" ).text
            full_list_text = elem.text 
            al["full_list_text"] = full_list_text 
            obj = al 
            objList.append( obj )

        except Exception as e : 
            print( e )
            pass 
        finally:
            print('time pass')

    #foundLists = soup.find_all("a", string=["View List"])
    df = pd.DataFrame( pd.json_normalize(objList) )
    # now get placings data
    # https://www.bestcoastpairings.com/event/ZMe2dZaoUv?active_tab=pairings&round=1
    

    
    return df 