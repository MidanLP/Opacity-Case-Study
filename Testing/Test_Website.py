import json
import sys
import io
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

## This script is the main testing script for the healthcare website, which is running on localhost:8080.
## It automates the process of testing the website, extracting timings for the loading of the parachute.png, and writing the results to an Excel file.



caps = DesiredCapabilities.CHROME 
caps["goog:loggingPrefs"] = {"performance": "ALL"} # for Timings measurement

FILENAME = "time_output.xlsx" #File to be written to
SHEET = "Testing Timings" #Sheet in the file to be written to

driver_path = "C:/Program Files/chromedriver/chromedriver.exe" #Path to your ChromeDriver executable (standard)
chrome_binary_path = "C:/Program Files/Google/Chrome/Application/chrome.exe" #Path to your Chrome browser executable (standard)

chrome_options = Options()
chrome_options.binary_location = chrome_binary_path
#chrome_options.add_argument("--incognito") #go into incognito, so we ensure no cache is used

service = Service(driver_path)

chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"}) 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.execute_cdp_cmd("Network.enable", {}) #Enable network tracking, needed for timing results

#driver.get("http://localhost:8081/") #


driver.get("http://localhost:8080/")   #Instruction to open the healthcare website, which is running on localhost:8080 (or other if changed)





def clear(): # function to clear browser cache
    print("Clearing the browser cache and cookies...")
    driver.execute_cdp_cmd('Network.clearBrowserCache', {})
    driver.execute_cdp_cmd('Storage.clearDataForOrigin', {
        "origin": "*",
        "storageTypes": "cookies,local_storage,session_storage"
    })
    print("Cache and cookies cleared!")

def test(): # try to extract time value from webpage
    row = {}
    try:
        time_value = driver.execute_script("return time;")  # take value in the "time" variable: -1 if not set, otherwise the time value in ms
        bust_value = driver.execute_script("return bust;")  # take value in the "bust" variable: -1 if not set, otherwise the bust value in ms
        is_cached = driver.execute_script("return isCached;")  # take value in the "isCached" variable: false if not set, otherwise true
        print(f"Time value extracted from webpage: {time_value}")
        print(f"Bust value extracted from webpage: {bust_value}")
        print(f"Is cached value extracted from webpage: {is_cached}")
        row = {"Time": time_value, "Bust": bust_value, "Is Cached": is_cached}
    except Exception as e:
        print(f"Error: {e}")

    time.sleep(0.8)
    try: # try to extract network timings
        network_value = get_network_timings("parachute.jpeg") #This is the resource we want the timings for
        if network_value != []:
            print(f"Network timings extracted: {network_value}") #Here we have the times for both normal and cache bust requests, we save only the normal values
            for key in network_value[0]:
                if(network_value[0][key] < 0 or network_value[0][key] > 900): # if the value is negative or greater, we set it to 0, as it is not a valid timing
                    network_value[0][key] = 0 # replace negative values with 0, as they are not valid timings (happends if times are so small for memCache that they are rounded to 0), program cant handle these microseconds
                    print(f"Warning: {key} value is negative, setting to 0")
                row[key] = network_value[0][key] # add the timings to the row
        else:
            print("No network timings found for the specified Pic.")
    except Exception as e:
        print(f"Error while getting network timings: {e}")
    write_to_excel(row, FILENAME, ["Time", "Bust", "Is Cached", "Queued", "Stalled", "DNS Lookup", "Initial Connection", "SSL", "Request Sent", "Waiting", "Download"])
    time.sleep(10)

# Attempt to automate the timing extraction process, opposed to manual testing and noting of timings 
def get_network_timings(target_url_substring): # function to get network timings for a specific resource (parachute.jpeg in this case)from the Resource Timing API as described in
                                               # https://stackoverflow.com/questions/55957240/how-to-calculate-total-time-for-one-request-from-chrome-driver-performance-logs
                                               # 
    resource_timings = driver.execute_script("""
    return performance.getEntriesByType('resource')
        .filter(r => r.name.includes('parachute.jpeg'))
        .map(r => ({
            name: r.name,
            startTime: r.startTime,
            fetchStart: r.fetchStart,
            domainLookupStart: r.domainLookupStart,
            domainLookupEnd: r.domainLookupEnd,
            connectStart: r.connectStart,
            connectEnd: r.connectEnd,
            secureConnectionStart: r.secureConnectionStart,
            requestStart: r.requestStart,
            responseStart: r.responseStart,
            responseEnd: r.responseEnd
        }));
""")


    logs = driver.get_log("performance") # Get performance logs from Selenium WebDriver
    timings = []

    for entry in logs: # Iterate through each log entry, much help from ChatGPT(https://chatgpt.com/) to develop and understand the structure of the logs and get right values
        msg = json.loads(entry["message"])["message"]

        if msg["method"] == "Network.responseReceived": 
            req_id = msg["params"]["requestId"]
            url = msg["params"]["response"]["url"]
            timing = msg["params"]["response"].get("timing")
            timestamp = msg["params"]["timestamp"]  
            if target_url_substring in url and timing: # if it is our target (parachute.jpeg) append results
                timings.append({
                    "requestId": req_id,
                    "url": url,
                    "timing": timing,
                    "logTimestamp": timestamp
                })
        #find the corresponding loadingFinished event for already added target resource
        elif msg["method"]=="Network.loadingFinished":
            req_id = msg["params"]["requestId"]
            for t in timings:
                if t["requestId"] == req_id:
                    t["loadingFinished"] = msg["params"]

    results = []
    for t in timings:
        if "loadingFinished" not in t: # skip if not loaded yet
            continue
        timing = t["timing"] 
        lf = t["loadingFinished"]
        request_time = timing["requestTime"]
        # calculate and append the timings
        results.append({ # find results for "queued", "stalled", "DNS Lookup", "Initial Connection", "SSL", "Request Sent", "Waiting" and "Download"
            "Queued": resource_timings[0]["fetchStart"] - resource_timings[0]["startTime"],  # for some reason, only the API has these values, not the logs, so both are used
            "Stalled": min([
                t for t in [timing.get("dnsStart", -1), timing.get("connectStart", -1), timing.get("sendStart", -1)]
                if t >= 0
                ]),
            "DNS Lookup": timing["dnsEnd"] - timing["dnsStart"],
            "Initial Connection": timing["connectEnd"] - timing["connectStart"],
            "SSL": timing["sslEnd"] - timing["sslStart"], # SSL timing is not always present, so it might be -1 (depends on architecture and connection)
            "Request Sent": timing["sendEnd"] - timing["sendStart"],
            "Waiting": timing["receiveHeadersEnd"] - timing["sendEnd"],
            "Download": (lf["timestamp"] - (request_time + timing["receiveHeadersEnd"]/ 1000)) * 1000
        })
    return results

def write_to_excel(data, filename="time_output.xlsx", column=None): #our results are in the parameter "data", which is a dictionary with the keys as column names
    df = pd.DataFrame([data], columns=column)
    try:
        with pd.ExcelWriter(filename, mode='a', if_sheet_exists='overlay', engine='openpyxl') as writer:
            if SHEET not in writer.book.sheetnames:
                df.to_excel(writer, sheet_name=SHEET, index=False)
            else:
                df.to_excel(writer, sheet_name=SHEET, index=False, header=False, startrow=writer.sheets[SHEET].max_row)
    except FileNotFoundError:
        df.to_excel(filename, sheet_name=SHEET, index=False, engine='openpyxl')

time.sleep(2)

while True:
    try:
        testtimes = int(input("How many times do you want to test? (default 1): ") or 1) # wait for user input for testtimes
        if testtimes <= 0:
            print("Please enter a positive integer.")
            continue
        break
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

while True:
    try:
        clear_cache_bool = input("Do you want to clear the browser cache before each test? (y/n, default y): ").strip().lower() or "y" #wait for user input, should cache be cleared
        if clear_cache_bool in ["yes", "no", "y", "n"]: # validate input
            if clear_cache_bool in ["yes", "y"]:
                clear_cache_bool = True
            else:
                clear_cache_bool = False
            break
        else:
            print("Please enter 'yes' or 'no'.")
    except Exception as e:
        print(f"Error: {e}")

try:# open the risk assessment page, from the main page
    link = driver.find_element(By.LINK_TEXT, "Risk Assessment")
    link.click()  
    print("Link clicked successfully!")
except Exception as e:
    print(f"Error: {e}")





for i in range(testtimes):# main loop, repeat "testimes" amount of times
    print(f"Test iteration {i + 1} of {testtimes}")
    if clear_cache_bool: # if user wants a clear cache
        clear()
    driver.refresh() 
    time.sleep(4)
    test() # actual test function


driver.quit() # Close browser

print("Script completed successfully!")
