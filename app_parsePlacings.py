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
import time


def parsePlacingResults( driver, eventId, skipCountMax=6 ): 
    url = f"https://www.bestcoastpairings.com/event/{eventId}?active_tab=placings"
    driver.get( url )
    #su.waitSync( 1 )
   
    su.viewAllListResults( driver )
    placings = [] 
    
    try : 
         user = WebDriverWait(driver, 5 ).until(
            EC.presence_of_element_located((By.TAG_NAME, "hr"))
            )
    except :

        pass
    finally :
        searchBarList = driver.find_elements_by_xpath ( '//input[@placeholder="Search for a player"]' )
        if len( searchBarList ) > 0 : 
            searchBar = searchBarList[0] 
            pHeadTag = searchBar.find_element_by_xpath( "../../../../../../div")
            placeElements = driver.find_elements_by_xpath( "//hr")
                
            if len ( placeElements ) < skipCountMax : 
                return None 
            div_index = 0 
            for elem in placeElements :  
                placingObj = {} 
        
                parentDivs = elem.find_elements_by_xpath( "../div")
                if len ( parentDivs ) > 0 : 
                    parentDiv = parentDivs[0]
                    #parentDiv = elem.find_element_by_xpath( "../div")
                    
                    #placingDiv = parentDiv.find_element_by_xpath( 'div')
                    #button = parentDiv.find_element_by_xpath( "./button")
                    buttonList = parentDiv.find_elements_by_xpath( './*/*[@type="button"]')
                    if len ( buttonList ) > 0 : 
                        button = buttonList[ 0 ] 
                        actions = ActionChains(driver)
                        #actions.pause(1)
                        actions.move_to_element(button)
                        actions.click(button)
                        actions.perform()
                        #su.waitSync( driver, 1 ) 
                    #time.sleep(1)
                    parentDiv = elem.find_element_by_xpath( "../div")
                    nameEnd = 0

                    # print( f'start player section @ pairing')
                    viewList = parentDiv.find_elements_by_xpath( './/a')
                    if len ( viewList ) > 0 :
                        link = viewList[0].get_attribute( 'href' )
                        if link != None : 
                            elem = viewList[0]
                            listId = elem.get_attribute( 'href' )[39:]
                            placingObj[ 'listId'] = listId 
                    #child_index = 0 
                    #for child in child_divs :
                    lines = parentDiv.text.split( '\n')

                    placingObj[ 'rank'] = lines[0]
                    placingObj[ 'playerName'] = lines[1]
                
                    if 'TEAM NAME' in lines[2] : 
                        placingObj['teamName'] = lines[3]
                    prevLineNum = -1 
                    lineNum = 0 
                    for line in lines :  

                        if "Record:" in line : 
                            placingObj["record_src"] = line.replace( 'Record:' , '' ).strip()

                        elif "SWISS POINTS" in line : 
                            placingObj["swissPoints"] = line.replace('SWISS POINTS ', '' ).strip()

                        elif "MARGIN OF VICTORY" in line : 
                            placingObj["marginOfVictory"] = line.replace('MARGIN OF VICTORY ', '' ).strip()

                        elif "BATTLE TACTICS" in line : 
                            placingObj["countBattleTactic"] = line.replace('BATTLE TACTICS ', '' ).strip()

                        elif "GRAND STRATEGIES" in line : 
                            placingObj["countGrandStrategy"] = line.replace('GRAND STRATEGIES ', '' ).strip()
                        else :
                            acceptedTags = [ 'WINS SOS' ,'BATTLE POINTS SOS' ,'WINS EXTENDED SOS' ,'BATTLE POINTS EXTENDED SOS' ] 
                            if any(tag in line for tag in acceptedTags ):
                            #if [ 'WINS SOS' ,'BATTLE POINTS SOS' ,'WINS EXTENDED SOS' ,'BATTLE POINTS EXTENDED SOS' ] in line : 
                                spaceIndex = line.rfind( ' ') ;  
                                if ( spaceIndex > 0 ) : 
                                    key = line[ 0 : spaceIndex ] 
                                    keyValue = line [ spaceIndex + 1 : ]
                                    placingObj[ key ] = keyValue 
                                    #print ( f'[{key}] = {keyValue}')
                                    #print ( 'debug ')
                        prevLineNum = lineNum 
                        lineNum = lineNum + 1 
                        
                    placings.append( placingObj )

                #child_index = child_index + 1       
                        
                #if pairing_obj["playerName"] != "": 
                #pairing_obj = {} 
            div_index = div_index + 1 
            df = pd.json_normalize( placings )
            df.to_csv( f"./armylist/event_{eventId}_placings.csv")
            print ( f'adding {len( df )} placings ')
            return placings

driver = su.createDriver( 'C:/lab/bestcoastpairings_parser/edgedriver_win64/msedgedriver.exe' )
#su.waitSync( 1 )
su.loginAndWait( driver, "settings.ini" , 4 )
eventObjs = []


event_df = pd.read_csv( "events_links.csv" )
event_df.reset_index() 
all_placings = [] 
#https://www.bestcoastpairings.com/event/tFIPqaYN2S
debugCount = 0 
eventIdStart = "XXXXXXXXX"
doParsing = 1 
i = 0 
for index, row in event_df.iterrows():
#if 1 == 1:
    placings = []
    eventId = row["url"][40:]
    #eventId = "ZMe2dZaoUv"
    print( 'parsing event ', eventId )
    
    #if ( doParsing == 1) : 
    #print( f'parsing round [{i}]')

    #try:
    placings = parsePlacingResults( driver,eventId )
    if placings != None and len ( placings ) > 0 : 
        all_placings.extend( placings )
            #except Exception as e : 
            #    print ( e ) 
            #    print( 'could not parse placings - skipping')
            #    pass 
            #finally:
            #    all_placings.extend( placings )
        #i = i + 1
        #if eventId == eventIdStart:
        #   doParsing = 1 
        pairings_df = pd.json_normalize( all_placings )
        #pairings_df
        #pairings_df['game'] = df['V'].str.split('-',expand=True) 
        pairings_df.to_csv( "placingsData_progress.csv" )


#for index, row in event_df.iterrows():
#    eventId = row[
# "url"][40:]
#    obj = su.getEventDetails( driver, eventId )
#    eventObjs.append( obj )    

pairings_df = pd.json_normalize( all_placings )
pairings_df.to_csv( "placingsData.csv" )

  
