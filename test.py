from data_pipeline import DataPipeline, UpcomingMatchCollection

def main():
    """ # Instantiate the DataPipeline
    pipeline = DataPipeline()
    
    # Run the web scraper method which scrapes data and saves raw CSVs into the in_dir
    upcoming_match, meta_data, team_data, player_data = pipeline.web_scraper(93965)
    print("Web scraping complete. Raw data files have been saved to the designated in_dir.")
    print(f"Upcoming match: {upcoming_match}")
    
    # Run the data processing method which processes data and saves intermediate and final results
    X, y = pipeline.data_processing()
    print("Data processing complete. Processed files have been saved in the out_dir and its intermediate folder.") """

    upcoming = UpcomingMatchCollection()

    upcoming_data = upcoming.get_upcoming_match(93970)

    print(upcoming_data)

if __name__ == "__main__":
    main()