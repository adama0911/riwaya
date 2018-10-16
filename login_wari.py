import os
import sys
import time

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Set the MOZ_HEADLESS environment variable which casues Firefox to start in headless mode.

#os.environ['MOZ_HEADLESS'] = '1'

# Select your Firefox binary.
binary = FirefoxBinary('/usr/bin/firefox', log_file=sys.stdout)

# Start selenium with the configured binary.
driver = webdriver.Firefox(firefox_binary=binary)

print("Firefox has been launched ...")

# Visit this webpage. 
#driver.get("https://intoli.com/blog/running-selenium-with-headless-firefox/")


############################### LANCEMENT PAGE AUTHENTIFICATION WARI ###########################################
driver.get("https://www.warime.com/callmoney/checking.zul")

print("warime has been launched ...")

# Grab the heading element from the response.

#heading_element = driver.find_element_by_xpath('//*[@id="heading-breadcrumbs"]')

#heading_element = driver.find_element_by_xpath('//*[@placeholder="Identifiant"]')

#heading_element = driver.find_element_by_xpath('//*[@class="panel-title"][1]')

heading_element = driver.find_element_by_tag_name('title')

driver.get_screenshot_as_file('main-page.png')

# Print the title in the terminal.
if heading_element:
    print(heading_element.get_property('textContent'))
else:
    print("Heading element not found!")

################################# SAISIE PARAMETRES D'ACCES ET VALIDATION POUR CONNEXION ############################################

heading_element_2 = driver.find_element_by_xpath('//*[@placeholder="Identifiant"]')

if heading_element_2:
    print(heading_element_2.get_property('placeholder'))
    heading_element_2.clear()
    heading_element_2.send_keys("AARRY409")
    print(heading_element_2.get_property('value'))    
else:
    print("Heading element not found!")

heading_element_3 = driver.find_element_by_xpath('//*[@placeholder="Mot de Passe"]')

if heading_element_3:
    print(heading_element_3.get_property('placeholder'))
    heading_element_3.clear()
    heading_element_3.send_keys("DAKAR2018")
    driver.get_screenshot_as_file('main-page-post-saisie.png')
    heading_element_3.send_keys(Keys.RETURN)
else:
    print("Heading element not found!")



##########################  TRAITEMENT REPONSE WARI APRES TENTATIVE DE CONNEXION ############################################

try:
    element_mask = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CLASS_NAME, "z-modal-mask"))
    )
    print("The desired element was there")

    driver.get_screenshot_as_file('main-page-post-validation.png')

    secondLevel_PWD_element = driver.find_element_by_xpath('html/body/div/div/div/div/div/table/tbody/tr/td/div/input')
    secondLevel_PWD_element.clear()
    secondLevel_PWD_element.send_keys("DAKAR2020")
    print( secondLevel_PWD_element.get_property('type') )    

    driver.get_screenshot_as_file('modal-pwd-second-level.png')
   
    secondLevel_PWD_validBTN = driver.find_element_by_xpath('//div[@class="z-div"]/button')
    print( secondLevel_PWD_validBTN.get_property('textContent') )
    secondLevel_PWD_validBTN.click()


    second_element_mask = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".z-window-header.z-window-header-move"))
    )

    print("After wait period")
    driver.get_screenshot_as_file('modal-pwd-second-level-post-validation.png')

    guichetierChoice = driver.find_element_by_xpath("//div[@class='z-listcell-content'][text()='Guichetier de  Distributeur']")

    print( guichetierChoice.get_property('textContent') )

    guichetierChoice.click()

    second_element_mask = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='z-listcell-content'][text()='CITE DIAMALAYE 2 VILLA N° 33']"))
    )
    
    driver.get_screenshot_as_file('modal-post-choix-typeCompte.png')
    
    distribToChoose = driver.find_element_by_xpath("//div[@class='z-listcell-content'][text()='CITE DIAMALAYE 2 VILLA N° 33']")

    distribToChoose.click()

    home_element_mask = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//button[@class='messagebox-btn z-button'][text()='OK']"))
    )
    
    driver.get_screenshot_as_file('modal-ok-page-principale.png')
    
    #geolocBTN = driver.find_element_by_xpath("//div[@class='z-window-header z-window-header-move']/div[@class='z-window-icon z-window-close']/i[@class='z-icon-times']")

    #geolocBTN.click()

    geoloc = driver.find_element_by_xpath("//button[@class='messagebox-btn z-button']")
   
    geoloc.click()

    full_home_element_mask = WebDriverWait(driver, 60).until(EC.invisibility_of_element_located((By.XPATH,"//div[@class='z-window-header z-window-header-move']/div[@class='z-window-icon z-window-close']/i[@class='z-icon-times']")))

    
    driver.get_screenshot_as_file('full-page-principale.png')

    #deconnectBTN = driver.find_element_by_xpath("//i[@class='z-icon-power-off fa-3x']")

    #deconnectBTN.click()

    # retour_login_page_element_mask = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Mot de Passe']"))
    # )

    driver.get_screenshot_as_file('de-retour-page-connexion.png')
    
    warim_menu_items = driver.find_elements_by_xpath("//a[@class='btn btn-success z-toolbarbutton']")
