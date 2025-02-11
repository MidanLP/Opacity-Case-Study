import sys
import io
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
import time


driver_path = "C:/Program Files/chromedriver/chromedriver.exe"
chrome_binary_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

chrome_options = Options()
chrome_options.binary_location = chrome_binary_path

service = Service(driver_path)

driver = webdriver.Chrome(service=service, options=chrome_options)


driver.get("http://healthcare.local:8080/pages/risk-assessment.html")

def clear(): # function to clear browser cache
    print("Clearing the browser cache and cookies...")
    driver.execute_script("""
        document.cookie.split(";").forEach(function(c) {
            document.cookie = c.trim().split("=")[0] + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/";
        });

        window.localStorage.clear();
        window.sessionStorage.clear();
    
        console.log("Cache, cookies, and storage cleared.");
    """)

def test(): #try to extract time value from webpage
    try:
        time_value = driver.execute_script("return time;")  
        print(f"Time value extracted from webpage: {time_value}")
    
        with open('time_output.txt', 'a') as f:
            f.writelines(f"Time value: {time_value}\n")

        print("Time value written to time_output.txt")
    except Exception as e:
        print(f"Error: {e}")

    time.sleep(0.8)

def testCache(): #try to extract time value from webpage
    try:
        time_value = driver.execute_script("return time;")  
        print(f"Time value extracted from webpage: {time_value}")
    
        with open('time_output_server.txt', 'a') as f:
            f.writelines(f"Time value: {time_value}\n")

        print("Time value written to time_output.txt")
    except Exception as e:
        print(f"Error: {e}")

    time.sleep(0.8)


time.sleep(2)

try:#open the risk assessment page, from the main page
    link = driver.find_element(By.LINK_TEXT, "Risk Assessment")
    link.click()  
    print("Link clicked successfully!")
except Exception as e:
    print(f"Error: {e}")

testtimes = 1000 #number of tests to run
try:
    time_value = driver.execute_script("return time;")  #gives back the time value
    print(f"Time value extracted from webpage: {time_value}")
    
    with open('time_output.txt', 'a') as f:
        f.writelines(f"Testing_Amount:{testtimes}, Date: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")} \n") #write the time 

    print("Text Header made")
except Exception as e:
    print(f"Error: {e}")

for i in range(testtimes):#main loop, repeat "testimes" amount of times
    clear()
    driver.refresh()
    test()


driver.quit() # Close browser

print("Script completed successfully!")
