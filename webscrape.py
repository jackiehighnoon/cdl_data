from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from io import StringIO
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def initialize_driver_settings():
    options = Options()
    options.page_load_strategy = 'normal'
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    options.add_argument("--window-size=1200,800")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# CDL tournament match details

def CDL_major_2(driver):
    for match in range(93939, 93940): #, 93957):
        driver.get(f"https://www.breakingpoint.gg/match/{match}")
        match_id = match
        date_time = driver.find_element(By.TAG_NAME, 'p').text
        tournament_id = "CDL_Major_2"
        gamemode = driver.find_elements(By.XPATH, "//div[contains(@class, 'css-jh7uq1')]/*[contains(@class, 'css-1ylx6zt')]")
        gamemode_list = [item.find_element(By.TAG_NAME, "p").text for item in gamemode]
        maps = driver.find_elements(By.XPATH, "//div[contains(@class, 'css-jh7uq1')]/*[contains(@class, 'css-1ylx6zt')]/div/p")
        map_list = [item.text for item in maps]
        bo_type = f'BO ${len(map_list)}'
        if len(map_list) == 7:
            stage = 'grand final'
        else:
            stage = 'playoffs'
    # convert variables into csv file and return

driver = initialize_driver_settings()
CDL_major_2(driver)


def get_tournament_stats(website: str):
    pass

""" driver.get(website)

table = driver.find_element(By.TAG_NAME, "table")

# Extract table content
html_content = table.get_attribute('outerHTML')

# Close the driver
driver.quit() """

# Wrap HTML in StringIO to avoid FutureWarning
# html_buffer = StringIO(html_content)
# df = pd.read_html(html_buffer)[0]

# print(df)