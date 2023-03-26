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



def parseRoundResults( driver, eventId, round ): 
    url = f"https://www.bestcoastpairings.com/event/{eventId}?active_tab=pairings&round={round}"
    driver.get( url )
    su.waitSync( 2 )
   
    su.viewAllListResults( driver )
    #su.waitSync( 5 )
    #driver.implicitly_wait(5)

    try:
        elem = WebDriverWait(driver, 5 ).until(
            EC.presence_of_element_located((By.ID, "Element_to_be_found")) #This is a dummy element
            )
    except : 
        pass 
    finally:
        print('time pass - grabbing source code ')
        htmlCode = driver.page_source
        soup=BeautifulSoup(htmlCode, "html.parser")
    

        #list_links1 = soup.find_all('//*[@id="undefined-tabpanel-2"]/div/div/div/div/div[3]/div[2]/a')
        list_links = soup.find_all( 'a' )
        
        # get title
        roundTitle = driver.find_element_by_xpath( '//*[@id="undefined-tabpanel-2"]/div/div/div/div/div[1]/div[1]/p').text

        # TODO : // need a beter way to detect the "games dev" - it can change between rounds the order of DIVs
        games = driver.find_elements_by_xpath ( '//*[@id="undefined-tabpanel-2"]/div/div/div/div/div[3]/div/a')
        
        # round three having troulbe let's compare paths
        #                                       //*[@id="undefined-tabpanel-2"]/div/div/div/div/div[4]/div[2]/a
        div_index = 0 
        pairingRound = [] 
        for g in games :  
            
            #pairings_list = g.find_elements_by_tag_name( 'p' )
            # each pairing with  a table 
            tableNumber = g.find_element_by_xpath( ".//div/p").text
            child_divs = g.find_elements_by_xpath( './/div/div/a')
            pairing_obj = {}
            pairing_obj["round"] = round 
            pairing_obj["eventId"] = eventId
            pairing_obj['tableNumber'] = tableNumber
            
            #player = 1 
            playerName = ""
            nameEnd = 0

            print( f'start player section @ pairing')
            child_index = 0 
            for child in child_divs :
                lines = child.text.split( '\n')
                pairingId = child.get_attribute( "href")[39:]
                pairing_obj['pairingId'] = pairingId
                for line in lines :  
                    #line = child.text
                    print( f'div[{div_index}]:pElem[{child_index}] = {line}') 
                
                        # elem_index > 0 : 
                    if nameEnd == 0: 
                        if "-----" not in line :  
                            playerName = playerName + " " + line
                            pairing_obj['playerName'] = playerName.strip()
                        else :
                            #pairing_obj[f"playerName"] = playerName.strip() 
                            playerName = ""
                            nameEnd = 1 

                    elif "Loss:" in line : 
                        pairing_obj["playerResult"] = 'Loss' 
                        pairing_obj["score"] = line[5:].strip()

                    elif "Win:" in line : 
                        pairing_obj["playerResult"] = 'Win' 
                        pairing_obj["score"] = line[4:].strip()

                    elif "Draw:" in line :
                        pairing_obj["playerResult"] = 'Draw' 
                        pairing_obj["score"] = line[5:].strip()
                    #https://www.bestcoastpairings.com/game/pairing/437FH4B0ND'
                    elif line == "View List" or line == "No List" : 
                        if line == "View List":
                            c2 = child.find_element_by_tag_name( 'a')
                            listUrl = c2.get_attribute('href')
                            debugger = 2
                            #htmlCode = line.page_source
                            #p.contents[0]['href']
                            href_index = listUrl.find( '/list/')
                            if href_index > -1 : 
                                pairing_obj[f"playerListId"] = listUrl[ href_index+6 : ]
                        pairingRound.append( pairing_obj )
                        print('player object added, resetting player obj')
                        pairing_obj = {}
                        pairing_obj["round"] = round 
                        pairing_obj["eventId"] = eventId
                        pairing_obj['tableNumber'] = tableNumber
                        pairing_obj['pairingId'] = pairingId

                        playerName = ""
                        nameEnd = 0 
                        # ///TODO : make this better later
                        # stop at two players to prevent nested tags from being counted
                        #if len( pairingRound) >= 2 :
                        #    print('two players found, breaking out of pairing')
                        #    break 
                        #nameEnd = 0
                    # start of new player 
                    elif '------' in line and nameEnd == 1 :
                        print('end of player section')
                        
                    else :
                        print( 'uncaught line')
            
            child_index = child_index + 1       
                    
            #if pairing_obj["playerName"] != "": 
            #pairing_obj = {} 
        div_index = div_index + 1 
        df = pd.json_normalize( pairingRound )
        df.to_csv( f"event_{eventId}_round{round}.csv")
        print ( f'adding {len( pairingRound )} pairings ')
        return pairingRound, roundTitle

driver = su.createDriver( 'C:/lab/bestcoastpairings_parser/edgedriver_win64/msedgedriver.exe' )
su.waitSync( 1 )
su.loginAndWait( driver, "settings.ini" , 4 )
eventObjs = []

event_df = pd.read_csv( "events_links.csv" )
#event_df = pd.read_csv( "Dv3LDfBRAU_event_data_badParsing.csv") 
event_df.reset_index() 
all_pairings = [] 
#https://www.bestcoastpairings.com/event/tFIPqaYN2S
debugCount = 0 
roundTitle = "" 
prevRoundTitle = ""
i = 1 
while 1 == 1 : 
    print( f'parsing round [{i}]')
    pairings, roundTitle = parseRoundResults( driver, "Dv3LDfBRAU", i )
    
    if roundTitle == prevRoundTitle : 
        print('repeat round! exiting')
        break   
    else : 
        all_pairings.extend( pairings )
    prevRoundTitle = roundTitle
    i = i + 1

#for index, row in event_df.iterrows():
#    eventId = row["url"][40:]
#    obj = su.getEventDetails( driver, eventId )
#    eventObjs.append( obj )    

pairings_df = pd.json_normalize( all_pairings )
pairings_df.to_csv( "pairingsData.csv" )

i = 0 

  
