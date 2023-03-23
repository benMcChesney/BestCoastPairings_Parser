from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
# https://medium.com/analytics-vidhya/python-selenium-all-mouse-actions-using-actionchains-197530cf75df
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd 
import selenium_utils as su 

#local RTT
event_guid = "Dv3LDfBRAU"
#LVO 
#event_guid = "AjzJ5hifwT"
url = f"https://www.bestcoastpairings.com/event/{event_guid}?active_tab=pairings&round=1"
driver = webdriver.Edge(executable_path='C:/lab/bestcoastpairings_parser/edgedriver_win64/msedgedriver.exe')
driver.get( url )
driver.maximize_window() 
su.loginAndWait(driver , 'settings.ini', 3 )


def parseRoundResults( driver, eventId, round ): 

    event_guid = "ZMe2dZaoUv"
    url = f"https://www.bestcoastpairings.com/event/{eventId}?active_tab=pairings&round={round}"
    driver.get( url )
    su.waitSync( 6 )
    # #undefined-tabpanel-2 > div > div > div > div > div.MuiGrid-root.MuiGrid-container.css-nwzen1 > div:nth-child(1) > div > div > div
    # /html/body/div/div/div[3]/div/div[2]/div/div/div/div/div[4]/div[1]/div/div/div

    # //*[@id="undefined-tabpanel-2"]/div/div/div/div/div[4]/div[1]/div/div/input
    # 
    '''
    <div tabindex="0" role="button" aria-expanded="true" aria-haspopup="listbox" aria-labelledby="undefined-label" 
    class="MuiSelect-select MuiSelect-outlined MuiOutlinedInput-input MuiInputBase-input css-nlnh1t">24</div>
    '''
    # /html/body/div/div/div[3]/div/div[2]/div/div/div/div/div[4]/div[1]/div/div/input

    '''
    //finds all tags of a type, for example h1,a,etc...
    //Here Driver is my instance of WebDriver

    var allTags = Driver.FindElements(By.XPath("//" + tagType));

    //iterate over all elements of that tag, and find the one whose attribute value you want

    foreach (var v in allTags)
            {             
            if ((v.GetAttribute.getText().equals(attributeName))
                return v;             
            }
            return null;
    '''
    #resultsButton = driver.find_element_by_xpath( '//*[@id="undefined-tabpanel-2"]/div/div/div/div/div[4]/div[1]/div/div/input' ) 
    resultsButton = driver.find_element_by_xpath( '//*[@tabIndex=0]' )
                                                 #//html/body/div/div/div[3]/div/div[2]/div/div/div/div/div[4]/div[1]/div/div/input' ); 
                                                 # /html/body/div/div/div[3]/div/div[2]/div/div/div/div/div[4]/div[1]/div/div/input
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #resultsButton = driver.find_element_by_tag_name( 'input')

    actions = ActionChains( driver ); 
    actions.move_to_element( resultsButton ) 
    actions.click() 
    actions.pause( 1 ) 
    actions.send_keys( 'A')  
    actions.send_keys( Keys.ENTER )
    actions.perform() 

    su.waitSync( 2 )
    
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
                pairing_obj["game_index"] = len(pairings)
                pairings.append( pairing_obj )
                print('adding a pairing')
                pairing_obj = {} 
    return pairings



games = parseRoundResults( driver, "ZMe2dZaoUv" , 1 )
games_df = pd.json_normalize( games )
su.waitSync( 3 )

games = parseRoundResults( driver, "ZMe2dZaoUv" , 2 )
games_df = pd.concat( [ games_df , pd.json_normalize( games ) ] )
su.waitSync( 3 )

games = parseRoundResults( driver, "ZMe2dZaoUv" , 3 )
games_df = pd.concat( [ games_df , pd.json_normalize( games ) ] )
su.waitSync( 3 )

games_df.to_csv( "pairings.csv")