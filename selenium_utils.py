from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
# https://medium.com/analytics-vidhya/python-selenium-all-mouse-actions-using-actionchains-197530cf75df
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def viewAllListResults( driver ) :
    try:
        elem = WebDriverWait(driver, 10 ).until(
            EC.presence_of_element_located((By.XPATH, "Element_to_be_found")) #This is a dummy element
            )
        #//
        resultsButton = driver.find_elements_by_tag_name( 'input')[1]
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
        print('time pass')

    

def waitSync( waitInSeconds = 3 ) :

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
    
    user  = driver.find_element_by_name( "email" )
    pw = driver.find_element_by_name("password")
    checkbox = driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div[1]/main/div/form/div[1]/div[4]/label/span[1]/input')
    btn = driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div[1]/main/div/form/div[1]/div[6]/button')

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

    waitSync( waitInSeconds ) 
