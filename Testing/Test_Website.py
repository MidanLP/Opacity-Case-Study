import sys
import io
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import time

# for Timings measurement
caps = DesiredCapabilities.CHROME
caps["goog:loggingPrefs"] = {"performance": "ALL"}

FILENAME = "time_output.xlsx"
SHEET = "Server, Cache"

driver_path = "C:/Program Files/chromedriver/chromedriver.exe"
chrome_binary_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = chrome_binary_path
chrome_options.add_argument("--incognito") # go into incognito, so we ensure no cache is used

service = Service(driver_path)

driver = webdriver.Chrome(service=service, options=chrome_options, desired_capabilities=caps)

driver.execute_cdp_cmd("Network.enable", {})


driver.get("http://healthcare.local:8080/")

def clear(): # function to clear browser cache
    print("Clearing the browser cache and cookies...")
    driver.execute_cdp_cmd('Network.clearBrowserCache', {})
    driver.execute_cdp_cmd('Storage.clearDataForOrigin', {
        "origin": "*",
        "storageTypes": "cookies,local_storage,session_storage"
    })
    print("Cache and cookies cleared successfully!")

def test(): # try to extract time value from webpage
    try:
        time_value = driver.execute_script("return time;")  
        print(f"Time value extracted from webpage: {time_value}")
    
        write_to_excel(time_value,FILENAME)
    except Exception as e:
        print(f"Error: {e}")

    time.sleep(0.8)

def write_to_excel(data, filename="time_output.xlsx"):
    df = pd.DataFrame([data], columns=["Time"])
    try:
        with pd.ExcelWriter(filename, mode='a', if_sheet_exists='overlay', engine='openpyxl') as writer:
            if SHEET not in writer.book.sheetnames:
                df.to_excel(writer, sheet_name=SHEET, index=False)
            else:
                df.to_excel(writer, sheet_name=SHEET, index=False, header=False, startrow=writer.sheets[SHEET].max_row)
    except FileNotFoundError:
        df.to_excel(filename, sheet_name=SHEET, index=False, engine='openpyxl')

time.sleep(2)

try:# open the risk assessment page, from the main page
    link = driver.find_element(By.LINK_TEXT, "Risk Assessment")
    link.click()  
    print("Link clicked successfully!")
except Exception as e:
    print(f"Error: {e}")

testtimes = 1000 # number of tests to run


for i in range(testtimes):# main loop, repeat "testimes" amount of times
    driver.refresh()
    time.sleep(1)
    test()


driver.quit() # Close browser

print("Script completed successfully!")
