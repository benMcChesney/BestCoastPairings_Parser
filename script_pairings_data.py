from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
# https://medium.com/analytics-vidhya/python-selenium-all-mouse-actions-using-actionchains-197530cf75df
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd 


def waitSync( waitInSeconds = 3 ) :
    try:
        elem = WebDriverWait(driver, 3).until(
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

    
    actions = ActionChains(driver)
    actions.move_to_element(login)
    actions.click(login)
    actions.pause(1)
    actions.click(login)
    actions.pause(3)
    actions.perform()

    import configparser
    config = configparser.ConfigParser()
    config.sections()
    config.read(config_path)


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
    actions.pause( 2 )
    actions.perform() 

    waitSync( 3 ) 

event_guid = "ZMe2dZaoUv"
url = f"https://www.bestcoastpairings.com/event/{event_guid}?active_tab=pairings&round=1"
driver = webdriver.Edge(executable_path='C:/lab/bestcoastpairings_parser/edgedriver_win64/msedgedriver.exe')
driver.get( url )
driver.maximize_window() 
loginAndWait(driver , 'settings.ini', 3 )


def parseRoundResults( driver, eventId, round ): 

    event_guid = "ZMe2dZaoUv"
    url = f"https://www.bestcoastpairings.com/event/{eventId}?active_tab=pairings&round={round}"
    driver.get( url )
    waitSync( 5 )
    htmlCode = driver.page_source
    soup=BeautifulSoup(htmlCode, "html.parser")

    list_links1 = soup.find_all('//*[@id="undefined-tabpanel-2"]/div/div/div/div/div[3]/div[2]/a')
    list_links = soup.find_all( 'a' )

    pairings = []  
    for elem in list_links : 
        if "href" in elem.attrs and "/pairing/" in elem.attrs['href'] :
            #link_elements.append( elemn )
            pairings_list = elem.find_all( 'p' )
            pairing_obj = {} 
            elem_index = 0 
            if len(pairings_list) in ( 8,9 ) : 
                player2NameKeyIndex = 5
                player1ListKeyIndex = 4
                if len(pairings_list) == 8 : 
                    player2NameKeyIndex = 4 
                    player1ListKeyIndex = 3
                debugger = 1 
                for sub_elem in pairings_list :
                    if elem_index == 1 :  
                        pairing_obj[ "Player1" ] = sub_elem.text.replace( "--------" , "" ) 
                    elif elem_index == 3 :  
                        result = sub_elem.text 
                        colon_index = result.find( ":" )
                        if colon_index > 1 :
                            game_result = result[ : colon_index ]
                            game_points = result[ colon_index + 1 : ]
                            pairing_obj[ 'player1_result' ] = game_points 
                            pairing_obj[ 'player1_score' ] = game_result.strip()   
                    elif elem_index == player1ListKeyIndex :  
                        try: 
                            htmlCode = sub_elem.contents[0]['href']
                            href_index = htmlCode.find( '/list/')
                            if href_index > -1 : 
                                pairing_obj['Player1_list_id'] = htmlCode[ href_index+6 : ]
                        except : 
                            pairing_obj['Player1_list_id'] = "" 
                        
                    elif elem_index == player2NameKeyIndex :  
                        pairing_obj[ "Player2" ] = sub_elem.text 
                    elif elem_index == player2NameKeyIndex+2 :  
                        result = sub_elem.text 
                        colon_index = result.find( ":" )
                        if colon_index > 1 :
                            game_result = result[ : colon_index  ]
                            game_points = result[ colon_index + 1 : ]
                            pairing_obj[ 'player2_result' ] = game_points 
                            pairing_obj[ 'player2_score' ] = game_result.strip()  
                    elif elem_index == player2NameKeyIndex+3 :  
                        try: 
                            pairing_obj['Player2_list_id'] = "" 
                            htmlCode = sub_elem.contents[0]['href']
                            href_index = htmlCode.find( '/list/')
                            if href_index > -1 : 
                                pairing_obj['Player2_list_id'] = htmlCode[ href_index+6 : ]
                        except:
                            pairing_obj['Player2_list_id'] = ""
                    elem_index = elem_index + 1
                    
            if pairing_obj != {}: 
                pairing_obj["round"] = round      
                pairings.append( pairing_obj )
                print('adding a pairing')
                pairing_obj = {} 
    return pairings



games = parseRoundResults( driver, "ZMe2dZaoUv" , 1 )
games_df = pd.json_normalize( games )
waitSync( 3 )

games = parseRoundResults( driver, "ZMe2dZaoUv" , 2 )
games_df = pd.concat( [ games_df , pd.json_normalize( games ) ] )
waitSync( 3 )

games = parseRoundResults( driver, "ZMe2dZaoUv" , 3 )
games_df = pd.concat( [ games_df , pd.json_normalize( games ) ] )
waitSync( 3 )

games_df.to_csv( "pairings.csv")