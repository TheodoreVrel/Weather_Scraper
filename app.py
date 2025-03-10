import time
from time import sleep

from selenium import webdriver
import json

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

with open('stations.JSON') as s:
    json_data = json.load(s)

#print(json_data['resorts'][0]['name'])

from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.implicitly_wait(6.35)

with open("ski_info_cookies.json", "r") as file:
    s_i_cookies = json.load(file)
with open("courchevel_cookies.json", "r") as file2:
    courchevel_cookies = json.load(file2)

s_i_cookies_added = False
f_i_cookies_added = False





def init_station_dict(station_id) -> dict:
    station_name = json_data['resorts'][station_id]['name']

    station_dictionary = {"name" : station_name,
                          "f_i_resort_snow" : -100,
                          "f_i_altitude_snow": -100,
                          "f_i_resort_temp": -100,
                          "f_i_altitude_temp": -100,

                          "s_i_resort_snow": -100,
                          "s_i_altitude_snow": -100,
                          "s_i_resort_temp": -100,
                          "s_i_altitude_temp": -100
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
            station_dictionary["a_resort_min_max_temperature"] = -100
        if 'a_min_max_temp_altitude_element_id' in json_data['resorts'][station_id]:
            station_dictionary["a_altitude_min_max_temperature"] = -100

    return station_dictionary

def has_additional_link(station_id):
    return 'additional_link' in json_data['resorts'][station_id]

def run_data_scraper():
    for station_num in range(16):
        get_all_station_data(station_num)

def get_all_station_data(station_id):
    #data_gathered_time = time.clock_gettime(time.CLOCK_REALTIME) #truncate minutes and seconds later

    station_data = init_station_dict(station_id)


    get_all_station_data_from_france_info(station_id, station_data)
    get_all_station_data_from_ski_info(station_id, station_data)
    get_all_station_data_from_bonus_info(station_id, station_data)

    print (station_data['name'] + "     " + str(station_data))

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
    # global s_i_cookies_added
    # if not s_i_cookies_added:
    #     for cookie in s_i_cookies:
    #         filtered_cookie = {
    #             "name": cookie["name"],
    #             "value": cookie["value"]
    #         }
    #         driver.add_cookie(filtered_cookie)
    #     s_i_cookies_added = True


    #button_by =  (By.XPATH, "//*[@id=\"pigeon-access-limited-one-trust\"]/div[1]/div[2]/div[1]/button")
    #time.sleep(10)
    #button = WebDriverWait(driver, 10).until(
    #    expected_conditions.presence_of_element_located(button_by)
    #)
    #driver.execute_script("arguments[0].click();", button)
    #WebDriverWait(driver, 12).until(expected_conditions.presence_of_element_located((By.XPATH, button_by)))
    #driver.find_element(By.CSS_SELECTOR, button_by).click()

    station_dict['s_i_resort_snow'] = get_data_point("s_i_snow_resort_element_id", "g")
    station_dict['s_i_altitude_snow'] = get_data_point("s_i_snow_altitude_element_id", "g")

    go_to_s_i_temp(station_id)
    station_dict['s_i_resort_temp'] = get_data_point("s_i_temp_element_id", "g")

    click_switch_button(json_data['buttons_data']["s_i_switch_to_altitude_button_element_id"])
    station_dict['s_i_altitude_temp'] = get_data_point("s_i_temp_element_id", "g")


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
            station_dict["a_resort_min_max_temperature"] = get_data_point("a_min_max_temp_resort_element_id", "r", station_id)

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
            station_dict["a_altitude_min_max_temperature"] = get_data_point("a_min_max_temp_altitude_element_id", "r", station_id)


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
            station_dict["a_resort_min_max_temperature"] = get_data_point("a_min_max_temp_resort_element_id", "r", station_id)
        if 'a_min_max_temp_altitude_element_id' in json_data['resorts'][station_id]:
            station_dict["a_altitude_min_max_temperature"] = get_data_point("a_min_max_temp_altitude_element_id", "r", station_id)



        if 'a_switch_to_snow_button_element_id' in json_data['resorts'][station_id]:
            click_switch_button(get_element_by_from_json("a_switch_to_snow_button_element_id", "r", station_id))



        if 'a_snow_resort_element_id' in json_data['resorts'][station_id]:
            station_dict["a_resort_snow"] = get_data_point("a_snow_resort_element_id", "r", station_id)
        if 'a_snow_altitude_element_id' in json_data['resorts'][station_id]:
            station_dict["a_altitude_snow"] = get_data_point("a_snow_altitude_element_id", "r", station_id)






# selenium small bits
def go_to_website(url):
    driver.get(url)

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

    result = ""
    if get_element(selector) != "":
        return get_element(selector).text
    else : return ""

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
    button.click()
    sleep(0.3)

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


# data cleaning
def separate_slash_data(data):
    pass
def truncate_text_from_num_data(data):
    pass



# data storage
def add_data_to_csv(gather_time, station, data, column):
    pass






# Execution
#get_all_station_data(15)
run_data_scraper()