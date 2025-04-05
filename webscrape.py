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
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

driver = initialize_driver_settings()

def get_matches(driver):

    """"
    CDL MINOR 1 Tournament: 93839-93849 // Online // ALL BO5
    CDL MAJOR 1 Qualifier: 93815-93838 & 93850-93867 // Online // ALL BO5
    CDL MAJOR 1 Tournament: 93868-93885 // LAN // BO5 (BO7 for Grand Final)

    CDL MINOR 2 Tournament: 93907-93917 // Online // ALL BO5
    CDL MAJOR 2 Qualifier: 93886-93906 & 93918-93938 // Online // ALL BO5
    CDL MAJOR 2 Tournament: 93939-93956 // LAN // BO5 (BO7 for Grand Final)

    match_id, date_utc, tournament, tier, stage, best_of, is_lan

    """

    for match in range(93939, 93957):
        driver.get(f"https://www.breakingpoint.gg/match/{match}")
        match_id = match
        iso = pd.to_datetime(driver.find_element(By.TAG_NAME, 'p').text, utc=True).isoformat()
        tournament_name = driver.find_element(By.XPATH, "//div[contains(@class, 'css-1e7ynd8')]/div/div/a").text
        maps = driver.find_elements(By.XPATH, "//div[contains(@class, 'css-jh7uq1')]/*[contains(@class, 'css-1ylx6zt')]/div/p")
        map_list = [item.text for item in maps]
        bestof_type = len(map_list)

        if len(map_list) == 7:
            stage = 'major finals'
            method = 1
        elif 'major' and 'tournament' in tournament_name.lower():
            stage = 'major'
            method = 1
        else:
            stage = 'minor'
            method = 0


        data = {
            'match_id': match_id,
            'date_utc': iso,
            'tournament': tournament_name,
            'best_of': bestof_type,
            'stage': stage,
            'is_lan' : method
        }

    return data

def get_matches_info(driver, match):
    # use this to figure out how to get selenium to click tabs
    data_values = []
    driver.get(f"https://www.breakingpoint.gg/match/{match}")

    #map_names = driver.find_elements(By.XPATH, "//div[contains(@class, 'css-jh7uq1')]/*[contains(@class, 'css-1ylx6zt')]/div/p")
    #map_list = [item.text for item in map_names]

    #gamemode_names = driver.find_elements(By.XPATH, "//div[contains(@class, 'css-jh7uq1')]/*[contains(@class, 'css-1ylx6zt')]")
    #gamemode_list = [item.find_element(By.TAG_NAME, "p").text for item in gamemode_names]

    team_names = driver.find_elements(By.XPATH, "//div[contains(@class, 'm_b0c91715')]/table/tbody/tr/td/a[contains(@href, 'teams')]")
    team_list = [item.text for item in team_names]

    # used to determine how many maps were played in total
    map_count = driver.find_elements(By.XPATH, "//div[contains(@class, 'm_8bffd616')]/div[2]/p[contains(@class, 'css-i1vu1j m_b6d8b162')]")
    total_maps_played = 0
    for round in map_count:
        total_maps_played += int(round.text)
    total_rounds_list = [int(round.text) for round in map_count]

    round_scores = driver.find_elements(By.XPATH, "//div[contains(@class, 'm_8bffd616')]/div[contains(@class, 'css-11t6rk7 m_e615b15f')]/div[2]/p")
    round_scores_list = []
    for round in round_scores:
        if round.text == '-':
            continue
        else:
            round_scores_list.append(int(round.text))

    rounds_first_team = [round_scores_list[i] for i in range(0,len(round_scores_list)) if i % 2 == 0] # this will get the first team scores
    rounds_second_team = [round_scores_list[i] for i in range(0,len(round_scores_list)) if i % 2 != 0] # this will get the second team scores

    series_everything = driver.find_elements(By.XPATH, "//tbody/tr/td")
    series_everything_elements = [element.text for element in series_everything if element.text not in ['',team_list[0],team_list[1]]]

    series_kills_list = []
    series_kills_list.append(series_everything_elements[1])
    for i in range(8,len(series_everything_elements),7):
        series_kills_list.append(series_everything_elements[i])
    series_deaths_list = []
    series_deaths_list.append(series_everything_elements[2])
    for i in range(9,len(series_everything_elements),7):
        series_deaths_list.append(series_everything_elements[i])
    series_damage_list = []
    series_damage_list.append(series_everything_elements[5].replace(',',''))
    for i in range(12,len(series_everything_elements),7):
        series_damage_list.append(series_everything_elements[i].replace(',',''))
    series_BP_rtg_list = []
    series_BP_rtg_list.append(series_everything_elements[6])
    for i in range(13,len(series_everything_elements),7):
        series_BP_rtg_list.append(series_everything_elements[i])

    # get overall match stats
    for team in team_list:
        team_name = team
        maps_won = total_rounds_list[0] if team == team_list[0] else total_rounds_list[1]
        maps_lost = total_rounds_list[1] if team == team_list[0] else total_rounds_list[0]
        series_win = 1 if maps_won > maps_lost else 0
        team_summary = range(0,4) if team == team_list[0] else range(4,8)
        series_kills = 0
        series_deaths = 0
        series_damage = 0
        series_BP_rtg = 0
        for team_count in team_summary:
            series_kills += int(series_kills_list[team_count])
            series_deaths += int(series_deaths_list[team_count])
            series_damage += int(series_damage_list[team_count])
            series_BP_rtg += float(series_BP_rtg_list[team_count])

        data = {
                'match_id': match,  # Match ID
                'team_name': team_name,     # Team Name
                'series_win': series_win,
                'maps_won': maps_won,
                'maps_lost': maps_lost,
                'series_kills': series_kills,
                'series_deaths': series_deaths,
                'series_damage': series_damage,
                'series_kdr': series_kills / series_deaths,
                'avg_bp_rtg': series_BP_rtg / 4
            }
        
        data_values.append(data)

    df = pd.DataFrame(data_values, columns=['match_id', 'team_name', 'series_win', 'maps_won', 'maps_lost', 'series_kills', 'series_deaths', 'series_damage', 'series_kdr', 'avg_bg_rtg'])
    return data_values

def get_player_info(driver, match):
    # use this to figure out how to get selenium to click tabs
    data_values = []
    driver.get(f"https://www.breakingpoint.gg/match/{match}")

    team_names = driver.find_elements(By.XPATH, "//div[contains(@class, 'm_b0c91715')]/table/tbody/tr/td/a[contains(@href, 'teams')]")
    team_list = [item.text for item in team_names]

    series_everything = driver.find_elements(By.XPATH, "//tbody/tr/td")
    series_everything_elements = [element.text for element in series_everything if element.text not in ['',team_list[0],team_list[1]]]

    series_player_names = []
    series_player_names.append(series_everything_elements[0])
    for i in range(7,len(series_everything_elements),7):
        series_player_names.append(series_everything_elements[i])
    series_kills_list = []
    series_kills_list.append(series_everything_elements[1])
    for i in range(8,len(series_everything_elements),7):
        series_kills_list.append(series_everything_elements[i])
    series_deaths_list = []
    series_deaths_list.append(series_everything_elements[2])
    for i in range(9,len(series_everything_elements),7):
        series_deaths_list.append(series_everything_elements[i])
    series_damage_list = []
    series_damage_list.append(series_everything_elements[5].replace(',',''))
    for i in range(12,len(series_everything_elements),7):
        series_damage_list.append(series_everything_elements[i].replace(',',''))
    series_BP_rtg_list = []
    series_BP_rtg_list.append(series_everything_elements[6])
    for i in range(13,len(series_everything_elements),7):
        series_BP_rtg_list.append(series_everything_elements[i])

    # get overall match stats
    for team in team_list:
        team_name = team
        player_range = range(0,4) if team == team_list[0] else range(4,8)
        for player in player_range:
            player_name = series_player_names[player]
            kills = series_kills_list[player]
            deaths = series_deaths_list[player]
            damage = series_damage_list[player]
            bp_rtg = series_BP_rtg_list[player]

            data = {
                'match_id': match,  # Match ID
                'player_name': player_name,     # Team Name
                'team_name': team_name,
                'kills': kills,
                'deaths': deaths,
                'damage': damage,
                'bp_rtg': bp_rtg
            }
        
            data_values.append(data)

    df = pd.DataFrame(data_values, columns=['match_id', 'player_name', 'team_name', 'kills', 'deaths', 'damage', 'bp_rtg'])
    return data_values