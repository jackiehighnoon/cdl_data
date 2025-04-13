from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from pathlib import Path

class DataCollection:
    def __init__(self):
        #Initialize selenium web driver
        self.driver = self.initialize_driver_settings()
        # Initialize placeholders for data
        self.meta_data = []
        self.team_data = []
        self.player_data = []
        self.upcoming_match = ''

    def initialize_driver_settings(self):
        options = Options()
        options.page_load_strategy = 'normal'
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(4)   # seconds – Selenium will poll up to 4 s
        return driver

    def get_matches_info(self, match, team_list, total_rounds_list, series_everything_elements):
            data_values = []

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
                        'match_id': match,
                        'team_name': team_name,
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

            df = pd.DataFrame(data_values, columns=['match_id', 'team_name', 'series_win', 'maps_won', 'maps_lost', 'series_kills', 'series_deaths', 'series_damage', 'series_kdr', 'avg_bp_rtg'])
            return data_values

    def get_player_info(self, match, team_list, series_everything_elements):
        data_values = []

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
                kills = int(series_kills_list[player])
                deaths = int(series_deaths_list[player])
                damage = int(series_damage_list[player])
                bp_rtg = float(series_BP_rtg_list[player])

                data = {
                    'match_id': match,
                    'player_name': player_name,
                    'team_name': team_name,
                    'kills': kills,
                    'deaths': deaths,
                    'damage': damage,
                    'bp_rtg': bp_rtg
                }
            
                data_values.append(data)

        return data_values

    def get_matches(self, start=93815):

        """"
        CDL MINOR 1 Tournament: 93839-93849 // Online // ALL BO5
        CDL MAJOR 1 Qualifier: 93815-93838 & 93850-93867 // Online // ALL BO5
        CDL MAJOR 1 Tournament: 93868-93885 // LAN // BO5 (BO7 for Grand Final)

        CDL MINOR 2 Tournament: 93907-93917 // Online // ALL BO5
        CDL MAJOR 2 Qualifier: 93886-93906 & 93918-93938 // Online // ALL BO5
        CDL MAJOR 2 Tournament: 93939-93956 // LAN // BO5 (BO7 for Grand Final)
        """

        meta_data = []
        team_data = []
        player_data = []

        match = start

        while True:
            self.driver.get(f"https://www.breakingpoint.gg/match/{match}")

            try:
                upcoming = self.driver.find_element(By.XPATH, "//div[contains(@class, 'css-y8zqbt')]/button/span/span").text
                if upcoming.casefold() == 'upcoming':
                    upcoming_match = match
                    print(f'Match {match} is upcoming, ending scrape.')
                    break
            except Exception:
                pass
            
            try:
                match_id = match
                iso = pd.to_datetime(self.driver.find_element(By.TAG_NAME, 'p').text, utc=True).isoformat()
                tournament_name = self.driver.find_element(By.XPATH, "//div[contains(@class, 'css-1e7ynd8')]/div/div/a").text
                maps = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'css-jh7uq1')]/*[contains(@class, 'css-1ylx6zt')]/div/p")
                map_list = [item.text for item in maps]
                bestof_type = len(map_list)

                team_names = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'm_b0c91715')]/table/tbody/tr/td/a[contains(@href, 'teams')]")
                team_list = [item.text for item in team_names]

                map_count = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'm_8bffd616')]/div[2]/p[contains(@class, 'css-i1vu1j m_b6d8b162')]")
                total_maps_played = 0
                for round in map_count:
                    total_maps_played += int(round.text)
                total_rounds_list = [int(round.text) for round in map_count]
                
                series_everything = self.driver.find_elements(By.XPATH, "//tbody/tr/td")
                series_everything_elements = [element.text for element in series_everything if element.text not in ['',team_list[0],team_list[1]]]

                if len(map_list) == 7:
                    stage = 'major finals'
                    method = 1
                elif 'major' and 'tournament' in tournament_name.lower():
                    stage = 'major'
                    method = 1
                else:
                    stage = 'minor'
                    method = 0

                meta_data.append({
                    'match_id': match_id,
                    'date_utc': iso,
                    'tournament': tournament_name,
                    'best_of': bestof_type,
                    'stage': stage,
                    'is_lan' : method
                })
                team_data.extend(self.get_matches_info(match, team_list, total_rounds_list, series_everything_elements))
                player_data.extend(self.get_player_info(match, team_list, series_everything_elements))
                print(f'Finished match {match_id}, {team_list[0]} vs {team_list[1]}')
            except Exception as e:
                print(f'Error processing match {match}: {e}')
            
            match += 1
        return upcoming_match, meta_data, team_data, player_data

    def collect_future_data(self):
        pass

class DataCleanser(DataCollection):
    # process scraped data for testing and training
    def __init__(self, meta_data, team_data, player_data):
        super().__init__()
        self.meta_data = meta_data
        self.team_data = team_data
        self.player_data = player_data

    def combine_raw(self):
        meta_df = pd.DataFrame(self.meta_data)
        team_df = pd.DataFrame(self.team_data)
        player_df = pd.DataFrame(self.player_data)
        
        agg = (
        player_df.groupby(["match_id", "team_name"])
             .agg(
                 bp_mean = ("bp_rtg", "mean"),
                 bp_std  = ("bp_rtg", "std"), # How spread out the four players BP ratings are (roster balance).
                 bp_max  = ("bp_rtg", "max"), # Ceiling skill of the single best player (star power).
                 kills_sum = ("kills", "sum"),
                 kills_max = ("kills", "max"),
                 damage_sum = ("damage", "sum")
             )
             .reset_index()
        )

        agg["top_kills_share"] = agg["kills_max"] / agg["kills_sum"] # What fraction of team kills the top fragger contributes (carry dependence).
        agg["bp_range"]        = agg["bp_max"] - agg["bp_mean"]   # Star power relative to the teams average (max - mean).

        team_df = team_df.merge(agg[["match_id", "team_name",
                             "bp_std", "bp_max", "top_kills_share", "bp_range"]],
                        on=["match_id", "team_name"],
                        how="left")

        # Merge meta data into team_df

        team_df = team_df.merge(
            meta_df[["match_id", "date_utc", "best_of", "stage", "is_lan"]],
            on="match_id",
            how="left"
        )

        return team_df

    def add_rolls(self, df: pd.DataFrame, roll:int=5):
        ROLL_COLS = ["series_kills", "series_deaths", "series_damage", "series_kdr", "avg_bp_rtg","bp_std","bp_max","top_kills_share","bp_range"]
        df = df.sort_values(["team_name","date_utc"]).reset_index(drop=True)

        rolling = (
            # for the first 5 rows of data compute a mean based on what is available instead of dropping those rows
            df.groupby(["team_name"])[ROLL_COLS].rolling(window=5,min_periods=1).mean().reset_index()
            #.rolling(roll)
            #.mean()
            #.reset_index()
        )

        rolling = rolling.rename(columns={col: f"{col}_roll" for col in ROLL_COLS})
        df = df.merge(rolling, left_index=True, right_on="level_1").drop(columns=["level_1"])
        df = df.dropna(subset=[f"{col}_roll" for col in ROLL_COLS]).reset_index(drop=True)
        df_with_rolls = df.drop(columns=["team_name_y"]).rename(columns={"team_name_x": "team_name"})

        return df_with_rolls
    
    def add_elo(self, df: pd.DataFrame):
        df = df.sort_values(["date_utc"]).reset_index(drop=True)

        INITIAL_ELO = 1500
        K_FACTOR = 32

        elo_rating = {}
        pre_ratings = []

        for idx, row in df.iterrows():
            team = row["team_name"]
            match_id = row["match_id"]
            result = row["series_win"]

            opponent_row = df[(df["match_id"] == match_id) & (df["team_name"] != team)].iloc[0]
            opponent = opponent_row["team_name"]

            Ra = elo_rating.get(team, INITIAL_ELO)
            Rb = elo_rating.get(opponent, INITIAL_ELO)

            Ea = 1 / (1 + 10 ** ((Rb - Ra) / 400))
            Sa = result
            Sb = 1 - result

            pre_ratings.append(Ra)

            elo_rating[team] = Ra + K_FACTOR * (Sa - Ea)
            elo_rating[opponent] = Rb + K_FACTOR * (Sb - (1 - Ea))

        df["pre_match_elo"] = (pd.Series(pre_ratings).round(0)).astype(int)

        return df

    def build_matchups(self, df: pd.DataFrame):
        team_a = df.copy()
        team_b = df.copy()

        team_a.columns = [f"team_a_{col}" if col != "match_id" else col for col in team_a.columns]
        team_b.columns = [f"team_b_{col}" if col != "match_id" else col for col in team_b.columns]

        matchups = team_a.merge(team_b, on="match_id", suffixes=("_a", "_b"))
        matchups = matchups[matchups["team_a_team_name"] != matchups["team_b_team_name"]]

        # Keep only one direction per match
        matchups = matchups[matchups["team_a_team_name"] < matchups["team_b_team_name"]]

        # Creating differential columns for all relevant metrics

        matchups["elo_diff"] = matchups["team_a_pre_match_elo"] - matchups["team_b_pre_match_elo"]
        matchups["series_kills_roll_diff"] = matchups["team_a_series_kills_roll"] - matchups["team_b_series_kills_roll"]
        matchups["series_deaths_roll_diff"] = matchups["team_a_series_deaths_roll"] - matchups["team_b_series_deaths_roll"]
        matchups["series_damage_roll_diff"] = matchups["team_a_series_damage_roll"] - matchups["team_b_series_damage_roll"]
        matchups["series_kdr_roll_diff"] = matchups["team_a_series_kdr_roll"] - matchups["team_b_series_kdr_roll"]
        matchups["bp_rating_roll_diff"] = matchups["team_a_avg_bp_rtg_roll"] - matchups["team_b_avg_bp_rtg_roll"]
        matchups["bp_std_roll_diff"] = matchups["team_a_bp_std_roll"] - matchups["team_b_bp_std_roll"]
        matchups["bp_max_roll_diff"] = matchups["team_a_bp_max_roll"] - matchups["team_b_bp_max_roll"]
        matchups["top_kills_share_roll_diff"] = matchups["team_a_top_kills_share_roll"] - matchups["team_b_top_kills_share_roll"]
        matchups["bp_range_roll_diff"] = matchups["team_a_bp_range_roll"] - matchups["team_b_bp_range_roll"]
        matchups["series_win"] = matchups["team_a_series_win"]
        matchups["best_of"] = matchups["team_a_best_of"]
        matchups["is_lan"] = matchups["team_a_is_lan"]

        feature_cols = [
            "match_id",
            "team_a_team_name",
            "team_b_team_name",
            "best_of",
            "is_lan",
            "elo_diff",
            "series_kills_roll_diff",
            "series_deaths_roll_diff",
            "series_damage_roll_diff",
            "series_kdr_roll_diff",
            "bp_rating_roll_diff",
            "bp_std_roll_diff",
            "bp_max_roll_diff",
            "top_kills_share_roll_diff",
            "bp_range_roll_diff",
            # Optionally, add any label columns or additional identifiers you need
        ]

        X = matchups[feature_cols]
        y = matchups["series_win"]

        return X, y


class DataPipeline(DataCleanser):
    def __init__(self, in_dir: Path = Path("raw_data"), out_dir: Path = Path("processed_data")):
        super().__init__(meta_data=[], team_data=[], player_data=[])
        self.in_dir = in_dir
        self.out_dir = out_dir

        # Create directories if they don't exist
        self.in_dir.mkdir(exist_ok=True)
        self.out_dir.mkdir(exist_ok=True)
        self.intermediate_dir = self.out_dir / "intermediate"
        self.intermediate_dir.mkdir(exist_ok=True)

    def web_scraper(self, start=93815):
        # scrape past and future data from the web
        upcoming_match, meta_data, team_data, player_data = self.get_matches(start=start)

        self.meta_data = meta_data
        self.team_data = team_data
        self.player_data = player_data

        # Convert raw lists to DataFrames
        meta_df = pd.DataFrame(meta_data)
        team_df = pd.DataFrame(team_data)
        player_df = pd.DataFrame(player_data)

        # Save raw data CSVs to in_dir
        meta_df.to_csv(self.in_dir / "meta_data.csv", index=False)
        team_df.to_csv(self.in_dir / "team_data.csv", index=False)
        player_df.to_csv(self.in_dir / "player_data.csv", index=False)

        return upcoming_match, meta_data, team_data, player_data

    def data_processing(self):
        # Combine raw data (using data stored by web_scraper)
        combined_data = self.combine_raw()
        combined_path = self.intermediate_dir / "combined_data.csv"
        combined_data.to_csv(combined_path, index=False)

        # Add rolling metrics, default is 5
        data_with_rolls = self.add_rolls(combined_data)
        rolls_path = self.intermediate_dir / "data_with_rolls.csv"
        data_with_rolls.to_csv(rolls_path, index=False)

        # Calculate pre-match Elo ratings
        data_with_elo = self.add_elo(data_with_rolls)
        elo_path = self.intermediate_dir / "data_with_elo.csv"
        data_with_elo.to_csv(elo_path, index=False)

        # Build matchups to create features (X) and labels (y)
        X, y = self.build_matchups(data_with_elo)
        x_path = self.out_dir / "X.csv"
        y_path = self.out_dir / "y.csv"
        X.round(4).to_csv(x_path, index=False)
        y.round(4).to_csv(y_path, index=False)

        return X, y
    
class UpcomingMatchCollection(DataCollection):
    def __init__(self):
        super().__init__()

    def get_upcoming_match(self, match_id: int):
        url = f"https://www.breakingpoint.gg/match/{match_id}"
        self.driver.get(url)
        self.match_id = match_id
        
        try:
            # Check if the match status indicates it's upcoming.
            status_element = self.driver.find_element(By.XPATH, "//div[contains(@class, 'css-y8zqbt')]/button/span/span")
            status_text = status_element.text.strip()
            if status_text.casefold() != "upcoming":
                print(f"Match {match_id} is not upcoming: status is completed.")
                return None
        except Exception as e:
            print(f"Could not verify match status for match {match_id}: {e}")
            return None
        
        try:
            iso = pd.to_datetime(self.driver.find_element(By.TAG_NAME, 'p').text, utc=True).isoformat()
            tournament_name = self.driver.find_element(By.XPATH, "//div[contains(@class, 'css-1e7ynd8')]/div/div/a").text
            maps = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'css-jh7uq1')]/div/div")
            map_list = [item.text for item in maps]
            bestof_type = len(map_list)

            team_names = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'css-1nkbb35') or contains(@class,'css-89bxeg')]/div/div/a[contains(@href, 'teams')]")
            team_list = [item.text for item in team_names]
            
            if len(map_list) == 7:
                stage = 'major finals'
                method = 1
            elif 'major' and 'tournament' in tournament_name.lower():
                stage = 'major'
                method = 1
            else:
                stage = 'minor'
                method = 0

            match_data = {
                'match_id': match_id,
                'date_utc': iso,
                'tournament': tournament_name,
                'best_of': bestof_type,
                'stage': stage,
                'is_lan' : method
            }

            match_df = pd.DataFrame([match_data])
            team_df = pd.DataFrame({
            'match_id': [match_id] * len(team_list),
            'team_name': team_list
            })
            
            # Merge the team list with the match metadata on match_id
            upcoming_df = team_df.merge(match_df, on="match_id", how="left")

            # Merge rolling and ELO statistics
            # Load the historical data (data_with_elo.csv) and parse date_utc as datetime
            historical_df = pd.read_csv("processed_data/intermediate/data_with_elo.csv", parse_dates=["date_utc"])

            # Define the columns you need
            cols_to_keep = [
                "team_name", 
                "series_kills_roll", "series_deaths_roll", "series_damage_roll", 
                "series_kdr_roll", "avg_bp_rtg_roll", "bp_std_roll", 
                "bp_max_roll", "top_kills_share_roll", "bp_range_roll", 
                "pre_match_elo"
            ]

            # Sort by date and group by team_name to get the latest record for each team
            latest_team_metrics = (
                historical_df.sort_values("date_utc")
                            .groupby("team_name", as_index=False)
                            .last()[cols_to_keep]
            )

            final_upcoming = upcoming_df.merge(latest_team_metrics, how="left", on="team_name")

            #final_upcoming.round(4).to_csv("upcoming.csv", index=False)

            team_a = final_upcoming.copy()
            team_b = final_upcoming.copy()

            team_a.columns = [f"team_a_{col}" if col != "match_id" else col for col in team_a.columns]
            team_b.columns = [f"team_b_{col}" if col != "match_id" else col for col in team_b.columns]

            matchups = team_a.merge(team_b, on="match_id", suffixes=("_a", "_b"))
            matchups = matchups[matchups["team_a_team_name"] != matchups["team_b_team_name"]]

            # Keep only one direction per match
            matchups = matchups[matchups["team_a_team_name"] < matchups["team_b_team_name"]]

            # Creating differential columns for all relevant metrics

            matchups["elo_diff"] = matchups["team_a_pre_match_elo"] - matchups["team_b_pre_match_elo"]
            matchups["series_kills_roll_diff"] = matchups["team_a_series_kills_roll"] - matchups["team_b_series_kills_roll"]
            matchups["series_deaths_roll_diff"] = matchups["team_a_series_deaths_roll"] - matchups["team_b_series_deaths_roll"]
            matchups["series_damage_roll_diff"] = matchups["team_a_series_damage_roll"] - matchups["team_b_series_damage_roll"]
            matchups["series_kdr_roll_diff"] = matchups["team_a_series_kdr_roll"] - matchups["team_b_series_kdr_roll"]
            matchups["bp_rating_roll_diff"] = matchups["team_a_avg_bp_rtg_roll"] - matchups["team_b_avg_bp_rtg_roll"]
            matchups["bp_std_roll_diff"] = matchups["team_a_bp_std_roll"] - matchups["team_b_bp_std_roll"]
            matchups["bp_max_roll_diff"] = matchups["team_a_bp_max_roll"] - matchups["team_b_bp_max_roll"]
            matchups["top_kills_share_roll_diff"] = matchups["team_a_top_kills_share_roll"] - matchups["team_b_top_kills_share_roll"]
            matchups["bp_range_roll_diff"] = matchups["team_a_bp_range_roll"] - matchups["team_b_bp_range_roll"]
            matchups["best_of"] = matchups["team_a_best_of"]
            matchups["is_lan"] = matchups["team_a_is_lan"]

            feature_cols = [
                "best_of",
                "is_lan",
                "elo_diff",
                "series_kills_roll_diff",
                "series_deaths_roll_diff",
                "series_damage_roll_diff",
                "series_kdr_roll_diff",
                "bp_rating_roll_diff",
                "bp_std_roll_diff",
                "bp_max_roll_diff",
                "top_kills_share_roll_diff",
                "bp_range_roll_diff",
                # Optionally, add any label columns or additional identifiers you need
            ]

            X = matchups[feature_cols]
    
            # Add any additional pre-match details as needed.
        except Exception as e:
            print(f"Error processing upcoming match {match_id}: {e}")
            return None

        return X