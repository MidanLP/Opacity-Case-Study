import json
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
SHEET = "Testing Timings"

driver_path = "C:/Program Files/chromedriver/chromedriver.exe"
chrome_binary_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = chrome_binary_path
chrome_options.add_argument("--incognito") # go into incognito, so we ensure no cache is used

service = Service(driver_path)

chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"}) 
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.execute_cdp_cmd("Network.enable", {})


driver.get("http://localhost:8080/")  

def clear(): # function to clear browser cache
    print("Clearing the browser cache and cookies...")
    driver.execute_cdp_cmd('Network.clearBrowserCache', {})
    driver.execute_cdp_cmd('Storage.clearDataForOrigin', {
        "origin": "*",
        "storageTypes": "cookies,local_storage,session_storage"
    })
    print("Cache and cookies cleared successfully!")

def test(): # try to extract time value from webpage
    row = {}
    try:
        time_value = driver.execute_script("return time;")  
        print(f"Time value extracted from webpage: {time_value}")
        row = {"Time": time_value}
    except Exception as e:
        print(f"Error: {e}")

    time.sleep(0.8)
    try:
        network_value = get_network_timings("parachute.jpeg")
        if network_value != []:
            print(f"Network timings extracted: {network_value}")
            row.update(network_value[0])  
            #write_to_excel(network_value[0], FILENAME, ["Queued", "Stalled", "DNS Lookup", "Initial Connection", "SSL", "Request Sent", "Waiting", "Download"])
        else:
            print("No network timings found for the specified Pic.")
    except Exception as e:
        print(f"Error while getting network timings: {e}")    
    write_to_excel(row, FILENAME, ["Time", "Queued", "Stalled", "DNS Lookup", "Initial Connection", "SSL", "Request Sent", "Waiting", "Download"])
    time.sleep(5)


def get_network_timings(target_url_substring):

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


    logs = driver.get_log("performance")
    timings = []

    for entry in logs:
        msg = json.loads(entry["message"])["message"]

        if msg["method"] == "Network.responseReceived":
            req_id = msg["params"]["requestId"]
            url = msg["params"]["response"]["url"]
            timing = msg["params"]["response"].get("timing")
            timestamp = msg["params"]["timestamp"]  
            if target_url_substring in url and timing:
                timings.append({
                    "requestId": req_id,
                    "url": url,
                    "timing": timing,
                    "logTimestamp": timestamp
                })

        elif msg["method"]=="Network.loadingFinished":
            req_id = msg["params"]["requestId"]
            for t in timings:
                if t["requestId"] == req_id:
                    t["loadingFinished"] = msg["params"]

    results = []
    for t in timings:

        if "loadingFinished" not in t:
            continue
        timing = t["timing"]
        lf = t["loadingFinished"]
        request_time = timing["requestTime"]

        results.append({
            "Queued": resource_timings[0]["fetchStart"] - resource_timings[0]["startTime"], 
            "Stalled": min([
                t for t in [timing.get("dnsStart", -1), timing.get("connectStart", -1), timing.get("sendStart", -1)]
                if t >= 0
                ]),
            "DNS Lookup": timing["dnsEnd"] - timing["dnsStart"],
            "Initial Connection": timing["connectEnd"] - timing["connectStart"],
            "SSL": timing["sslEnd"] - timing["sslStart"],
            "Request Sent": timing["sendEnd"] - timing["sendStart"],
            "Waiting": timing["receiveHeadersEnd"] - timing["sendEnd"],
            "Download": (lf["timestamp"] - (request_time + timing["receiveHeadersEnd"]/ 1000)) * 1000
        })
    return results

def write_to_excel(data, filename="time_output.xlsx", column=None):
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

try:# open the risk assessment page, from the main page
    link = driver.find_element(By.LINK_TEXT, "Risk Assessment")
    link.click()  
    print("Link clicked successfully!")
except Exception as e:
    print(f"Error: {e}")

while True:
    try:
        testtimes = int(input("How many times do you want to test? (default 1): ") or 1)
        if testtimes <= 0:
            print("Please enter a positive integer.")
            continue
        break
    except ValueError:
        print("Invalid input. Please enter a valid integer.")


for i in range(testtimes):# main loop, repeat "testimes" amount of times
    clear()
    driver.refresh()
    time.sleep(4)
    test()


driver.quit() # Close browser

print("Script completed successfully!")
