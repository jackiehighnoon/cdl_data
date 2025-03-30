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

# CDL tournament match details

driver = initialize_driver_settings()

def get_matches_info(driver, match):
    # use this to figure out how to get selenium to click tabs
    data_values = []
    driver.get(f"https://www.breakingpoint.gg/match/{match}")

    map_names = driver.find_elements(By.XPATH, "//div[contains(@class, 'css-jh7uq1')]/*[contains(@class, 'css-1ylx6zt')]/div/p")
    map_list = [item.text for item in map_names]

    gamemode_names = driver.find_elements(By.XPATH, "//div[contains(@class, 'css-jh7uq1')]/*[contains(@class, 'css-1ylx6zt')]")
    gamemode_list = [item.find_element(By.TAG_NAME, "p").text for item in gamemode_names]

    team_names = driver.find_elements(By.XPATH, "//div[contains(@class, 'm_b0c91715')]/table/tbody/tr/td/a[contains(@href, 'teams')]")
    team_list = [item.text for item in team_names]

    map_count = driver.find_elements(By.XPATH, "//div[contains(@class, 'm_8bffd616')]/div[2]/p[contains(@class, 'css-i1vu1j m_b6d8b162')]")
    total_rounds = 0
    for round in map_count:
        total_rounds += int(round.text)
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

    # get overall match stats
    match_id = match

    for team in team_list:
        team_name = team
        opponent = team_list[1] if team == team_list[0] else team_list[0] # get the opponent team name
        maps_won = total_rounds_list[team_list.index(team)]
        maps_lost = total_rounds - maps_won
        i = 0
        for round in range(0,total_rounds):
            map = map_list[round]
            gamemode = gamemode_list[round]
            points_scored = rounds_first_team[round] if team_name == team_list[0] else rounds_second_team[round]
            result = 1 if (team_name == team_list[0] and rounds_first_team[round] > rounds_second_team[round]) or (team_name == team_list[1] and rounds_second_team[round] > rounds_first_team[round]) else 0
            diff = rounds_first_team[round] - rounds_second_team[round] if team_name == team_list[0] else rounds_second_team[round] - rounds_first_team[round]
            i+=1

            data = {
                'match_id': match_id,  # Match ID
                'team': team_name,     # Team Name
                'opponent': opponent,   # Opponent Team Name
                'gamemode': gamemode,  # Gamemode
                'map': map,            # Map Name
                'points_scored': points_scored,  # Points Scored
                'result': result,      # Result (1 = Win, 0 = Loss)
                'diff': diff           # Point Differential
            }
            i+=1
            data_values.append(data)
    df = pd.DataFrame(data_values, columns=['match_id', 'team', 'opponent', 'gamemode', 'map', 'points_scored', 'result', 'diff'])
    return df

print(get_matches_info(driver, 93949))

def get_player_match_info(driver, match):
    data_values = []
    driver.get(f"https://www.breakingpoint.gg/match/{match}")
    games = driver.find_elements(By.XPATH, "//div[contains(@class, 'm_576c9d4 m_89d33d6d')]/button")
    map_names = driver.find_elements(By.XPATH, "//div[contains(@class, 'css-jh7uq1')]/*[contains(@class, 'css-1ylx6zt')]/div/p")
    map_list = [item.text for item in map_names]
    gamemode_names = driver.find_elements(By.XPATH, "//div[contains(@class, 'css-jh7uq1')]/*[contains(@class, 'css-1ylx6zt')]")
    gamemode_list = [item.find_element(By.TAG_NAME, "p").text for item in gamemode_names]
    team_names = driver.find_elements(By.XPATH, "//div[contains(@class, 'm_b0c91715')]/table/tbody/tr/td/a[contains(@href, 'teams')]")
    team_list = [item.text for item in team_names]
    # get overall match stats
    games.pop(0)
    match_id = match

    for team in team_list:
        i = 0
        for game in games:
            map = map_list[i]
            gamemode = gamemode_list[i]
            game.click()
            i+=1

            data = {
                'match_id': match_id,  # Match ID
                'team': team,          # Team Name
                'gamemode': gamemode,  # Gamemode
                'map': map             # Map Name
            }
            data_values.append(data)

def get_team_match_info(driver):
    pass

def get_matches(driver):

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
            'bo_type': bestof_type,
            'gamemode': gamemode_list,
            'maps': map_list,
            'stage': stage,
            'method' : method
        }

    return data



"""     data_values.append(data)

    df = pd.DataFrame(data_values, columns=['match_id', 'date_time', 'tournament_id', 'gamemode', 'maps', 'bo_type', 'stage'])
    return df """