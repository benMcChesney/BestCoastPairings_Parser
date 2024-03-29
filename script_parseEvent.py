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


    
lists_df = pd.DataFrame() 

driver = su.createDriver( 'C:/lab/bestcoastpairings_parser/edgedriver_win64/msedgedriver.exe' )
su.loadEventList(  'Dv3LDfBRAU' , lists_df )

driver.get( 'https://www.bestcoastpairings.com/event/Dv3LDfBRAU' )

su.waitSync( 2 )
i = 0 

# address1 = //*[@id="undefined-tabpanel-0"]/div/div[2]/div/div/div/div[1]/div/div[4]/a/p[1]
# address2 = //*[@id="undefined-tabpanel-0"]/div/div[2]/div/div/div/div[1]/div/div[4]/a/p[2]
# address3 = //*[@id="undefined-tabpanel-0"]/div/div[2]/div/div/div/div[1]/div/div[4]/a/p[3]
# ticketPrice = //*[@id="undefined-tabpanel-0"]/div/div[2]/div/div/div/div[2]/div[1]/div[1]/h5
# eventName = //*[@id="undefined-tabpanel-0"]/div/div[2]/div/div/div/div[1]/div/div[1]/h4
# event Owner //*[@id="undefined-tabpanel-0"]/div/div[2]/div/div/div/div[1]/div/div[5]/h5
# date end = //*[@id="undefined-tabpanel-0"]/div/div[2]/div/div/div/div[1]/div/div[3]/h5[1]

