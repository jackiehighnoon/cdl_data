from data_pipeline import DataCollection

def main():
    collector = DataCollection()
    # Scrape data from breakpoint, 93815 is the first match ID
    meta_data, team_data, player_data = collector.get_matches(start=93956)
    
    # At this point, check manually (or using print statements) that CSV files were generated.
    print("Data collection complete. Please check the 'processed' directory for output CSVs.")

if __name__ == "__main__":
    main()