# -*- coding: utf-8 -*-

import os
import re
import stat
import sys
import time
from time import sleep

from selenium import webdriver
import json

from selenium.common import NoSuchElementException, TimeoutException, ElementClickInterceptedException, \
    ElementNotInteractableException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

import datetime
import csv

# with open('/stations.JSON') as s:
#     json_data = json.load(s)

# Get the base path for the executable or script
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
folder_name = 'WeatherScraper'
json_file_path = os.path.join(desktop_path, folder_name, 'stations.JSON')
csv_folder_path = os.path.join(desktop_path, folder_name, 'station_csv_files')

# Check the constructed file path
print("Using JSON file path:", json_file_path)
print("CSV file folder path:", csv_folder_path)

# Now, you can load the JSON file
try:
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)
except FileNotFoundError:
    print(f"Error: {json_file_path} not found.")



#print(json_data['resorts'][0]['name'])
# print(datetime.datetime.now())

# from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)
# driver = webdriver.Chrome(options=chrome_options)

driver = webdriver.Firefox()



driver.implicitly_wait(7.2)
driver.maximize_window()

with open(os.path.join(desktop_path, folder_name,"ski_info_cookies.json"), "r") as file:
    s_i_cookies = json.load(file)
with open(os.path.join(desktop_path, folder_name,"courchevel_cookies.json"), "r") as file2:
    courchevel_cookies = json.load(file2)

s_i_cookies_added = False
f_i_cookies_added = False

csv_data_order = ["name", "gathered_time_day", "gathered_time_hour",
                  "f_i_resort_snow", "s_i_resort_snow", "a_resort_snow",
                  "f_i_altitude_snow", "s_i_altitude_snow", "a_altitude_snow",
                  "f_i_resort_temp", "s_i_resort_temp", "a_resort_temperature",
                  "a_am_resort_temperature", "a_pm_resort_temperature", "a_resort_min_temperature", "a_resort_max_temperature",
                  "f_i_altitude_temp", "s_i_altitude_temp", "a_altitude_temperature",
                  "a_am_altitude_temperature", "a_pm_altitude_temperature", "a_altitude_min_temperature", "a_altitude_max_temperature"
                  ]



def init_station_dict(station_id) -> dict:
    station_name = json_data['resorts'][station_id]['name']

    station_dictionary = {"name" : station_name,
                          "gathered_time_day": "",
                          "gathered_time_hour": "",
                          "f_i_resort_snow" : -100,
                          "f_i_altitude_snow": -100,
                          "f_i_resort_temp": -100,
                          "f_i_altitude_temp": -100,

                          "s_i_resort_snow": -100,
                          "s_i_altitude_snow": -100,
                          "s_i_resort_temp": -100,
                          "s_i_altitude_temp": -100,



                          }

    if has_additional_link(station_id):
        if 'a_snow_resort_element_id' in json_data['resorts'][station_id]:
            station_dictionary["a_resort_snow"] = -100
        if 'a_snow_altitude_element_id' in json_data['resorts'][station_id]:
            station_dictionary["a_altitude_snow"] = -100

        if 'a_temp_resort_element_id' in json_data['resorts'][station_id]:
            station_dictionary["a_resort_temperature"] = -100
        if 'a_temp_altitude_element_id' in json_data['resorts'][station_id]:
            station_dictionary["a_altitude_temperature"] = -100

        if 'a_am_temp_resort_element_id' in json_data['resorts'][station_id]:
            station_dictionary["a_am_resort_temperature"] = -100
        if 'a_pm_temp_resort_element_id' in json_data['resorts'][station_id]:
            station_dictionary["a_pm_resort_temperature"] = -100
        if 'a_am_temp_altitude_element_id' in json_data['resorts'][station_id]:
            station_dictionary["a_am_altitude_temperature"] = -100
        if 'a_pm_temp_altitude_element_id' in json_data['resorts'][station_id]:
            station_dictionary["a_pm_altitude_temperature"] = -100

        if 'a_min_temp_resort_element_id' in json_data['resorts'][station_id]:
            station_dictionary["a_resort_min_temperature"] = -100
        if 'a_max_temp_resort_element_id' in json_data['resorts'][station_id]:
            station_dictionary["a_resort_max_temperature"] = -100
        if 'a_min_temp_altitude_element_id' in json_data['resorts'][station_id]:
            station_dictionary["a_altitude_min_temperature"] = -100
        if 'a_max_temp_altitude_element_id' in json_data['resorts'][station_id]:
                station_dictionary["a_altitude_max_temperature"] = -100

        if 'a_min_max_temp_resort_element_id' in json_data['resorts'][station_id]:
            station_dictionary["a_resort_min_temperature"] = -100
            station_dictionary["a_resort_max_temperature"] = -100
        if 'a_min_max_temp_altitude_element_id' in json_data['resorts'][station_id]:
            station_dictionary["a_altitude_min_temperature"] = -100
            station_dictionary["a_altitude_max_temperature"] = -100

    return station_dictionary

def has_additional_link(station_id):
    return 'additional_link' in json_data['resorts'][station_id]

def run_data_scraper():
    #for station_num in range(6,7):
    for station_num in range(16):
        # try:
            # add_data_to_csv(json_data['resorts'][station_num]['name'], get_all_station_data(station_num))
            d = get_all_station_data(station_num)
            # print(type(d))
            add_data_to_csv(json_data['resorts'][station_num]['name'], d)
            #print(json_data['resorts'][station_num]['name'], d)
        # except Exception:
        #     print(Exception)


def get_all_station_data(station_id):
    data_gathered_day = datetime.date.today().strftime("%Y-%m-%d")
    data_gathered_hour = datetime.datetime.today().hour

    station_data = init_station_dict(station_id)
    station_data['gathered_time_day'] = data_gathered_day
    station_data['gathered_time_hour'] = data_gathered_hour

    get_all_station_data_from_france_info(station_id, station_data)
    get_all_station_data_from_ski_info(station_id, station_data)
    get_all_station_data_from_bonus_info(station_id, station_data)

    # print (type(station_data))
    return station_data

# selenium
def get_all_station_data_from_france_info(station_id, station_dict):
    go_to_f_i(station_id)

    global f_i_cookies_added
    if not f_i_cookies_added:
        WebDriverWait(driver, 6).until(expected_conditions.presence_of_element_located((By.ID, "didomi-notice-disagree-button")))
        driver.find_element(By.ID, "didomi-notice-disagree-button").click()
        f_i_cookies_added = True

    station_dict['f_i_resort_snow'] = get_data_point("f_i_snow_resort_element_id", "g")
    station_dict['f_i_altitude_snow'] = get_data_point("f_i_snow_altitude_element_id", "g")

    station_dict['f_i_resort_temp'] = get_data_point("f_i_temp_element_id", "g")

    click_switch_button(json_data['buttons_data']["f_i_switch_to_altitude_button_element_id"])
    station_dict['f_i_altitude_temp'] = get_data_point("f_i_temp_element_id", "g")


def load_cookies(website):
    cookies_added = True
    cookies = []
    match website:
        case "ski_info":
            global s_i_cookies_added
            cookies_added = s_i_cookies_added
            cookies = s_i_cookies
        case "courchevel":
            cookies_added = False
            cookies = courchevel_cookies

    if not cookies_added:
        for cookie in cookies:
            filtered_cookie = {
                "name": cookie["name"],
                "value": cookie["value"]
            }
            driver.add_cookie(filtered_cookie)
        if website == "ski_info": s_i_cookies_added = True

def get_all_station_data_from_ski_info(station_id, station_dict):
    go_to_s_i_snow(station_id)
    load_cookies("ski_info")

    first_snow_element = get_data_point("s_i_snow_resort_element_id", "g")
    #check if the element is resort or altitude snow
    element = get_element(get_element_by_from_json("s_i_snow_resort_element_id", "g"))
    h3_text = ""
    if element != "":
        try:
            h3_element = element.find_element(By.XPATH, "./preceding-sibling::h3")
            h3_text = h3_element.text.strip()
            # print(h3_text)
        except (NoSuchElementException, TimeoutException):
            pass

    if "En haut" in h3_text:
        station_dict['s_i_altitude_snow'] = first_snow_element
    else:
        station_dict['s_i_resort_snow'] = first_snow_element
        station_dict['s_i_altitude_snow'] = get_data_point("s_i_snow_altitude_element_id", "g")

    go_to_s_i_temp(station_id)
    station_dict['s_i_resort_temp'] = get_average_temp(get_data_point("s_i_temp_element_id", "g"))

    click_switch_button(json_data['buttons_data']["s_i_switch_to_altitude_button_element_id"])
    station_dict['s_i_altitude_temp'] = get_average_temp(get_data_point("s_i_temp_element_id", "g"))


def get_all_station_data_from_bonus_info(station_id, station_dict):
    if not has_additional_link(station_id):
        return
    else: go_to_website(json_data['resorts'][station_id]['additional_link'])

    if station_id == 14 :
        load_cookies("courchevel")
    elif "a_cookies_pop_up_button_element_id" in json_data['resorts'][station_id]:
        #print("§§§§§ !!!!!  ", str(json_data['resorts'][station_id]['a_cookies_pop_up_button_element_id']))
        driver.find_element(By.XPATH, json_data['resorts'][station_id]['a_cookies_pop_up_button_element_id']).click()

    if 'a_switch_to_altitude_button_element_id' in json_data['resorts'][station_id]:
        if 'a_snow_resort_element_id' in json_data['resorts'][station_id]:
            station_dict["a_resort_snow"] = get_data_point("a_snow_resort_element_id", "r", station_id)
        if 'a_temp_resort_element_id' in json_data['resorts'][station_id]:
            station_dict["a_resort_temperature"] = get_data_point("a_temp_resort_element_id", "r", station_id)
        if 'a_am_temp_resort_element_id' in json_data['resorts'][station_id]:
            station_dict["a_am_resort_temperature"] = get_data_point("a_am_temp_resort_element_id", "r", station_id)
        if 'a_pm_temp_resort_element_id' in json_data['resorts'][station_id]:
            station_dict["a_pm_resort_temperature"] = get_data_point("a_pm_temp_resort_element_id", "r", station_id)
        if 'a_min_temp_resort_element_id' in json_data['resorts'][station_id]:
            station_dict["a_resort_min_temperature"] = get_data_point("a_min_temp_resort_element_id", "r", station_id)
        if 'a_max_temp_resort_element_id' in json_data['resorts'][station_id]:
            station_dict["a_resort_max_temperature"] = get_data_point("a_max_temp_resort_element_id", "r", station_id)
        if 'a_min_max_temp_resort_element_id' in json_data['resorts'][station_id]:
            station_dict["a_resort_min_temperature"] = get_separate_slash_data(get_data_point("a_min_max_temp_resort_element_id", "r", station_id), True)
            station_dict["a_resort_max_temperature"] = get_separate_slash_data(get_data_point("a_min_max_temp_resort_element_id", "r", station_id), False)

        click_switch_button(get_element_by_from_json("a_switch_to_altitude_button_element_id", "r", station_id))

        if 'a_snow_altitude_element_id' in json_data['resorts'][station_id]:
            station_dict["a_altitude_snow"] = get_data_point("a_snow_altitude_element_id", "r", station_id)
        if 'a_temp_altitude_element_id' in json_data['resorts'][station_id]:
            station_dict["a_altitude_temperature"] = get_data_point("a_temp_altitude_element_id", "r", station_id)
        if 'a_am_temp_altitude_element_id' in json_data['resorts'][station_id]:
            station_dict["a_am_altitude_temperature"] = get_data_point("a_am_temp_altitude_element_id", "r", station_id)
        if 'a_pm_temp_altitude_element_id' in json_data['resorts'][station_id]:
            station_dict["a_pm_altitude_temperature"] = get_data_point("a_pm_temp_altitude_element_id", "r", station_id)
        if 'a_min_temp_altitude_element_id' in json_data['resorts'][station_id]:
            station_dict["a_altitude_min_temperature"] = get_data_point("a_min_temp_altitude_element_id", "r", station_id)
        if 'a_max_temp_altitude_element_id' in json_data['resorts'][station_id]:
             station_dict["a_altitude_max_temperature"] = get_data_point("a_max_temp_altitude_element_id", "r", station_id)
        if 'a_min_max_temp_altitude_element_id' in json_data['resorts'][station_id]:
            station_dict["a_altitude_min_temperature"] = get_separate_slash_data(get_data_point("a_min_max_temp_altitude_element_id", "r", station_id), True)
            station_dict["a_altitude_max_temperature"] = get_separate_slash_data(get_data_point("a_min_max_temp_altitude_element_id", "r", station_id), False)


    else:
        if 'a_temp_resort_element_id' in json_data['resorts'][station_id]:
            station_dict["a_resort_temperature"] = get_data_point("a_temp_resort_element_id", "r", station_id)
        if 'a_temp_altitude_element_id' in json_data['resorts'][station_id]:
            station_dict["a_altitude_temperature"] = get_data_point("a_temp_altitude_element_id", "r", station_id)

        if 'a_am_temp_resort_element_id' in json_data['resorts'][station_id]:
            station_dict["a_am_resort_temperature"] = get_data_point("a_am_temp_resort_element_id", "r", station_id)
        if 'a_pm_temp_resort_element_id' in json_data['resorts'][station_id]:
            station_dict["a_pm_resort_temperature"] = get_data_point("a_pm_temp_resort_element_id", "r", station_id)
        if 'a_am_temp_altitude_element_id' in json_data['resorts'][station_id]:
            station_dict["a_am_altitude_temperature"] = get_data_point("a_am_temp_altitude_element_id", "r", station_id)
        if 'a_pm_temp_altitude_element_id' in json_data['resorts'][station_id]:
            station_dict["a_pm_altitude_temperature"] = get_data_point("a_pm_temp_altitude_element_id", "r", station_id)

        if 'a_min_temp_resort_element_id' in json_data['resorts'][station_id]:
            station_dict["a_resort_min_temperature"] = get_data_point("a_min_temp_resort_element_id", "r", station_id)
        if 'a_max_temp_resort_element_id' in json_data['resorts'][station_id]:
            station_dict["a_resort_max_temperature"] = get_data_point("a_max_temp_resort_element_id", "r", station_id)
        if 'a_min_temp_altitude_element_id' in json_data['resorts'][station_id]:
            station_dict["a_altitude_min_temperature"] = get_data_point("a_min_temp_altitude_element_id", "r", station_id)
        if 'a_max_temp_altitude_element_id' in json_data['resorts'][station_id]:
             station_dict["a_altitude_max_temperature"] = get_data_point("a_max_temp_altitude_element_id", "r", station_id)

        if 'a_min_max_temp_resort_element_id' in json_data['resorts'][station_id]:
            station_dict["a_resort_min_temperature"] = get_separate_slash_data(get_data_point("a_min_max_temp_resort_element_id", "r", station_id), True)
            station_dict["a_resort_max_temperature"] = get_separate_slash_data(get_data_point("a_min_max_temp_resort_element_id", "r", station_id), False)
        if 'a_min_max_temp_altitude_element_id' in json_data['resorts'][station_id]:
            station_dict["a_altitude_min_temperature"] = get_separate_slash_data(get_data_point("a_min_max_temp_altitude_element_id", "r", station_id), True)
            station_dict["a_altitude_max_temperature"] = get_separate_slash_data(get_data_point("a_min_max_temp_altitude_element_id", "r", station_id), False)

        if 'a_switch_to_snow_button_element_id' in json_data['resorts'][station_id]:
            click_switch_button(get_element_by_from_json("a_switch_to_snow_button_element_id", "r", station_id))



        if 'a_snow_resort_element_id' in json_data['resorts'][station_id]:
            station_dict["a_resort_snow"] = get_data_point("a_snow_resort_element_id", "r", station_id)
        if 'a_snow_altitude_element_id' in json_data['resorts'][station_id]:
            station_dict["a_altitude_snow"] = get_data_point("a_snow_altitude_element_id", "r", station_id)






# selenium small bits
def go_to_website(url):
    driver.get(url)
    sleep(0.3)

def go_to_f_i(station_id):
    go_to_website("https://meteo.francetvinfo.fr/meteo-neige/" + json_data['resorts'][station_id]['france_info_link_param'])
def go_to_s_i_snow(station_id):
    go_to_website("https://www.skiinfo.fr/" + json_data['resorts'][station_id]['ski_info_link_param'] + "/bulletin-neige")
def go_to_s_i_temp(station_id):
    go_to_website("https://www.skiinfo.fr/" + json_data['resorts'][station_id]['ski_info_link_param'] + "/meteo")


def get_data_point(element_id, dtype, station_id = ""):
    #if driver.current_url != url:
    #    go_to_website(url)
    selector = get_element_by_from_json(element_id, dtype, station_id)

    if get_element(selector) != "":
        # print(get_element(selector).text)
        num = clean_num_data(get_element(selector).text)
        if not "/" in num:
            # print(num)
            if num == "":
                num = -100
            num = float(num)
        return num
    else : return -100

def get_element_by_from_json(element_id, dtype, station_id = ""):
    selector = ""
    match dtype:
        case "g":
            selector = json_data['global_elements_data'][element_id]
        case "b":
            selector = json_data['buttons_data'][element_id]
        case "r":
            selector = json_data['resorts'][station_id][element_id]
    return selector

def click_switch_button(button_element_id):
    button = get_element(button_element_id)
    try:
        button.click()
    except ElementNotInteractableException :
        # print("Not interactable. Waiting.")
        sleep(1.4)
        try:
            button.click()
        except ElementNotInteractableException:
            pass
    except ElementClickInterceptedException:
        # print("Can't click. Scrolling.")
        ActionChains(driver) \
            .scroll_to_element(button) \
            .perform()
        try:
            button.click()
        except ElementClickInterceptedException:
            pass

    sleep(0.4)

def is_xpath(selector):
    return selector[0] == "/" or selector[0] == "("

def get_element(selector):
    #print(selector)
    try:
        if is_xpath(selector):
            #WebDriverWait(driver, 6).until(expected_conditions.presence_of_element_located((By.XPATH, selector)))
            return driver.find_element(By.XPATH, selector)
        else:
            #WebDriverWait(driver, 6).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, selector)))
            return driver.find_element(By.CSS_SELECTOR, selector)
    except (NoSuchElementException, TimeoutException):
        return ""
    # except ElementClickInterceptedException:
    #     print("Can't click. Scrolling.")
    #     ActionChains(driver) \
    #         .scroll_to_element(get_element(selector)) \
    #         .perform()
    #     return get_element(selector)


# data cleaning
def get_separate_slash_data(data, get_before_slash = True):
    before_slash, after_slash = data.split("/", 1)
    if get_before_slash:
        return float(before_slash)
    else: return float(after_slash)

def get_average_temp(double_temp_data_point):
    #For s_i_temp that has min and max for temperature within an hour
    return (int(get_separate_slash_data(double_temp_data_point, True)) + int(get_separate_slash_data(double_temp_data_point, False))) / 2

def clean_num_data(data):
    clean_data = data.replace("°C l", "/")
    # clean_data.replace("1200m", "")
    # clean_data.replace("900m", "")
    clean_data.replace(" ", "")

    clean_data = re.sub(r"-?\d+m", '', clean_data)
    clean_data = re.sub(r"Ressentie -?\d+ °C", '', clean_data)
    clean_data = re.sub(r"[^0-9/-]", '', clean_data)

    return clean_data


# data storage
def add_data_to_csv(station_name, data_dict):
    filename = str(csv_folder_path + "\\" + station_name.replace(" ", "_")) + "_data.csv"
    # print(filename)
    """Appends a list of dictionaries to a CSV file, ensuring all keys are included."""
    # Step 1: Get all unique keys from all dictionaries (headers)
    file_exists = os.path.isfile(filename)

    # Extract all keys to ensure consistent column headers
    all_keys = [key for key in csv_data_order if key in data_dict]

    # try:
    # if file_exists:
    #     os.chmod(filename, stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        os.chmod(filename, stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)

        writer = csv.DictWriter(csvfile, fieldnames=all_keys)

        if not file_exists:
            writer.writeheader()  # Create headers only if file doesn't exist

        writer.writerow(data_dict)  # Append the new data entry

    print(f"Data for {station_name} saved to {filename}")
    # except PermissionError:
    #     print("Permission denied. Please run the program as Administrator or check file permissions.")


# Execution
#get_all_station_data(15)
run_data_scraper()