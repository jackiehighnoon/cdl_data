from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
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

def get_matches_info(driver):
    data_values = []

    """"
    CDL MINOR 1 Tournament: 93839-93849 // Online // ALL BO5
    CDL MAJOR 1 Qualifier: 93815-93838 & 93850-93867 // Online // ALL BO5
    CDL MAJOR 1 Tournament: 93868-93885 // LAN // BO5 (BO7 for Grand Final)

    CDL MINOR 2 Tournament: 93907-93917 // Online // ALL BO5
    CDL MAJOR 2 Qualifier: 93886-93906 & 93918-93938 // Online // ALL BO5
    CDL MAJOR 2 Tournament: 93939-93956 // LAN // BO5 (BO7 for Grand Final)
    """

    for match in range(93939, 93957):
        driver.get(f"https://www.breakingpoint.gg/match/{match}")
        match_id = match
        date_time = driver.find_element(By.TAG_NAME, 'p').text
        tournament_name = driver.find_element(By.XPATH, "//div[contains(@class, 'css-1e7ynd8')]/div/div/a").text
        gamemode = driver.find_elements(By.XPATH, "//div[contains(@class, 'css-jh7uq1')]/*[contains(@class, 'css-1ylx6zt')]")
        gamemode_list = [item.find_element(By.TAG_NAME, "p").text for item in gamemode]
        maps = driver.find_elements(By.XPATH, "//div[contains(@class, 'css-jh7uq1')]/*[contains(@class, 'css-1ylx6zt')]/div/p")
        map_list = [item.text for item in maps]
        bestof_type = f'BO{len(map_list)}'

        if len(map_list) == 7:
            stage = 'major finals'
            method = 'LAN'
        elif 'major' and 'tournament' in tournament_name.lower():
            stage = 'major'
            method = 'LAN'
        else:
            stage = 'minor'
            method = 'online'


        data = {
            'match_id': match_id,
            'date_time': date_time,
            'tournament_id': tournament_name,
            'gamemode': gamemode_list,
            'maps': map_list,
            'bo_type': bestof_type,
            'stage': stage,
            'method' : method
        }
        data_values.append(data)

    df = pd.DataFrame(data_values, columns=['match_id', 'date_time', 'tournament_id', 'gamemode', 'maps', 'bo_type', 'stage'])
    return df

driver = initialize_driver_settings()
data = get_matches_info(driver)
print(data)