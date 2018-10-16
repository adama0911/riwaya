"""
    @Project: Robot 
    @Author: G'Optimus
    @Git : adama0911
    @version: 0.0.0
"""
import os
import sys
import time

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver

# Set the MOZ_HEADLESS environment variable which casues Firefox to start in headless mode.

#os.environ['MOZ_HEADLESS'] = '1'

# Select your Firefox binary.
binary = FirefoxBinary('/usr/bin/firefox', log_file=sys.stdout)

# Start selenium with the configured binary.
driver = webdriver.Firefox(firefox_binary=binary)

# Visit this webpage.
driver.get("https://jonimalaw.com/pfs/authentication/authentication.zul")

# Grab the heading element from the response.

driver.implicitly_wait(50)

try:
    #driver.find_element_by_id("email").send_keys("goudiabyadama938@gmail.com")
    #driver.find_element_by_id("pass").send_keys("Programmer7")

    #driver.find_element_by_xpath('//*[@id="email"]').send_keys("goudiabyadama938@gmail.com")
    #driver.find_element_by_xpath('//*[@id="pass"]').send_keys("Programmer7") 
    #driver.find_element_by_id("u_0_2").click()

    inputs  = driver.find_elements_by_xpath("//input[@class='z-textbox']")
    btns    = driver.find_elements_by_xpath("//button[@class='z-button-os']") 

    # input_login     = inputs[0]
    # input_pasword   = inputs[1]
    # button_validate = btns[0]
    # button_annulation   =   btns[1]
    
    # input_login.send_keys("goudiabyadama938@gmail.com")
    # print("set input login----------------------------------[OK]")
    # input_pasword.send_keys("ogrammer")
    # print("set input password-------------------------------[OK]")
    # button_validate.click()
    # print("validation---------------------------------------[OK]")

    inputs[0].send_keys("goudiabyadama938@gmail.com")
    inputs[1].send_keys("goudiabyadama938@gmail")
    btns[0].click()

except:
    print("Could not find element for 50s the first time. :(")
else:
    print("Found element the first time! :)")

time.sleep(60)
driver.quit()
