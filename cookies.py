import json
from time import sleep

from selenium import webdriver

# Open browser
driver = webdriver.Chrome()

# Go to the website
driver.get("https://www.skiinfo.fr/massif-central/besse-super-besse/meteo")
#driver.get("https://courchevel.com/fr/meteo/")

sleep(10)
# Get all cookies after clicking the button
cookies = driver.get_cookies()

# Save them to a file
with open("ski_info_cookies.json", "w") as file:
    json.dump(cookies, file, indent=4)

driver.quit()