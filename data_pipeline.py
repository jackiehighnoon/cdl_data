import pandas as pd
from pathlib import Path

class DataCollection:
    def __init__(self):
        pass

    def initialize_driver_settings(self):
        pass

    def get_matches_info(self):
        pass

    def get_player_info(self):
        pass

    def get_match(self):
        pass

    def collect_future_data(self):
        pass

class DataCleanser(DataCollection):
    # process scraped data for testing and training
    def __init__(self):
        super().__init__()

    def combine_raw(self):
        pass

    def add_rolls(self):
        pass

    def build_matchups(self):
        pass

class DataPipeline(DataCleanser):
    def __init__(self, in_dir: Path = Path("raw_data"), out_dir: Path = Path("processed_data")):
        super().__init__()
        self.in_dir = in_dir
        self.out_dir = out_dir

        # Create directories if they don't exist
        in_dir.mkdir(exist_ok=True)
        out_dir.mkdir(exist_ok=True)

    def web_scraper(self):
        # scrape past and future data from the web
        self.initialize_driver_settings()
        self.get_matches_info()
        self.get_player_info()
        self.get_match()
        self.collect_future_data()

    def data_processing(self):
        # process scraped data for testing and training
        self.combine_raw()
        self.add_rolls()
        self.build_matchups()