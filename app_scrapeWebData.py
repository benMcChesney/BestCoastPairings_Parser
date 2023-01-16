from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
# https://medium.com/analytics-vidhya/python-selenium-all-mouse-actions-using-actionchains-197530cf75df
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd 


def export_data( data ):
    htmlCode = driver.page_source
    soup=BeautifulSoup(htmlCode, "html.parser")

    links = soup.find_all('a')
    event_links = [] 
    for li in links : 
        url = li.attrs['href'] ; 
        if "/event/" in url :
            obj = {} 
            obj = { "url" : f"https://www.bestcoastpairings.com{url}" }
            event_links.append( obj )

    df = pd.DataFrame(event_links)
    df.to_csv("events_links.csv")
    print(f'exported {len(df)} rows' )
    


driver = webdriver.Edge(executable_path='C:/lab/bestcoastpairings_parser/edgedriver_win64/msedgedriver.exe')
driver.get("https://www.bestcoastpairings.com/events");
driver.implicitly_wait( 7 ); 
 

###
# location 
## mui-component-select-location
loc_elem = driver.find_element_by_css_selector( "#mui-component-select-location");
loc_elem.send_keys("Any Location" + Keys.RETURN )

actions = ActionChains(driver)
actions.move_to_element(loc_elem)
actions.click(loc_elem)
actions.send_keys("Any Location")
actions.send_keys(Keys.ENTER)
actions.perform()
print ( 'debugger')

#start date 
startDate = driver.find_element_by_xpath("//input[@id='mui-7']")
actions = ActionChains(driver)
actions.move_to_element( startDate)
actions.click(startDate)
for x in range(10):
    actions.send_keys_to_element(startDate, Keys.BACKSPACE)
actions.release()
actions.send_keys_to_element(startDate, "07/01/2022")
actions.release()
actions.perform() 
print ( 'debugger')


# end date 
startDate = driver.find_element_by_xpath("//input[@id='mui-8']")
actions = ActionChains(driver)
actions.move_to_element( startDate)
actions.click(startDate)
for x in range(10):
    actions.send_keys_to_element(startDate, Keys.BACKSPACE)
actions.release()
actions.send_keys_to_element(startDate, "02/01/2023")
actions.release()
actions.perform()
print ( 'debugger') 

# game system 
# #root > div > div.MuiBox-root.css-1rbk02f > div > div > div > div:nth-child(2) > form > div > div:nth-child(6) > div > div > input
# #mui-component-select-gameType
gameType = driver.find_element_by_css_selector("#mui-component-select-gameType")

actions = ActionChains(driver)
actions.move_to_element( gameType)
actions.click(gameType)
actions.perform() 

AosButton = driver.find_element_by_xpath( '//*[@id="menu-gameType"]/div[3]/ul/li[6]')
actions = ActionChains(driver)
actions.move_to_element(AosButton)
actions.click(AosButton)
actions.perform()
# search button button[type="submit"]

#root > div > div.MuiBox-root.css-1rbk02f > div > div > div > div:nth-child(2) > form > div > div:nth-child(9) > button
# //*[@id="root"]/div/div[3]/div/div/div/div[2]/form/div/div[8]/button
searchButton = driver.find_element_by_css_selector( 'button[type="submit"]' )

#searchButton = driver.find_element_by_partial_link_text("Search")   
actions = ActionChains(driver)
actions.move_to_element( searchButton )
actions.click(searchButton) 
actions.perform() 

pagesLoaded = 0 
doLoop = 1 
while( 1 == 1 ):
    try:
        elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "Element_to_be_found")) #This is a dummy element
        )
        loadMoreButton = driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div[1]/div/div/div[2]/div[3]/div[2]/button')
        #if ( loadMoreButton != None ) :  
        actions = ActionChains( driver ) 
        actions.move_to_element( loadMoreButton )
        actions.click( loadMoreButton ) 
        actions.perform() 
        pagesLoaded = pagesLoaded + 1 
        print( "loaded pages ", pagesLoaded )
        export_data(  driver.page_source )
        #else: 
        #    print("button not found" )
        #    doLoop = -2 
    except : 
        #print( "passing" )
        print("button not found" )
        doLoop = -2 
        pass 
        break 
        
    finally:
        print('time pass')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        

       

# if 'apples' in s:
#<a class="MuiButtonBase-root MuiCardActionArea-root css-1jluznr" tabindex="0" href="/event/9dgpLmdYHU" target="_blank">
# <img class="MuiCardMedia-root MuiCardMedia-media MuiCardMedia-img css-k012ot" src="https://d1ums0wp53uia4.cloudfront.net/bcp_dot_icon.png" alt="GemHammer AoS RTT July 2022"><div class="MuiCardHeader-root css-faujvq"><div class="MuiCardHeader-content css-11qjisw"><span class="MuiTypography-root MuiTypography-h5 MuiCardHeader-title css-1ecwsr4">
# <span class="MuiTypography-root MuiTypography-caption css-17eb3v6">Age of Sigmar</span>
# <p class="MuiTypography-root MuiTypography-body1 MuiTypography-gutterBottom css-8bka8">GemHammer AoS RTT July 2022</p><span class="MuiTypography-root MuiTypography-caption css-c279u4">Jul 17th 2022</span></span></div></div><span class="MuiCardActionArea-focusHighlight css-jo3ec3"></span><span class="MuiTouchRipple-root css-w0pj6f">
# </span>
# </a>

print( ' debugger ')
'''
# #root > div > div.MuiBox-root.css-1rbk02f > div.MuiBox-root.css-8atqhb > div > div > div:nth-child(2) > div.MuiGrid-root.MuiGrid-container.css-14w4kcq > div:nth-child(1)
link_style = 'a[tabindex="0"]'
events = driver.find_elements_by_css_selector( link_style )

events_list = [] 
for e in events : 
    print( e.text )
    events_list.append( e.text )
    print( e ) ;  
'''
'''
print(WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data='#results'] > a.btn.btn-white.btn-sm.btn-rounded.dropdown-toggle"))).get_attribute("title"))

WebDriverWait(driver,20).until( 
        EC.visibility_of_all_elements_located( 
            By.CSS_SELECTOR ,'a[tabindex="0"]' ).get_attribute("href"),
    )
print("debugger")
'''
#xPath to Grid 

##while ( 1 == 1):
'''
try:
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(By.XPATH, '//*[@id="root"]/div/div[3]/div[1]/div/div/div[2]/div[3]/div[2]/button')
        #$EC.presence_of_element_located(By.XPATH, '//*[@id="root"]/div/div[3]/div[1]/div/div/div[2]/div[3]/div[2]/button')
    )
    print('debugger')
    loadMoreActions = ActionChains(driver); 
    loadMoreActions.pause(6)
    loadMoreActions.click( element ); 
    
    loadMoreActions.perform() 
finally:
    print('debugger')
'''
print('full page')

'''
#grid = driver.find_element_by_xpath('//*[@id="root"]/div/div[4]/div/div/div/div[2]/div[2]')

# 
'''