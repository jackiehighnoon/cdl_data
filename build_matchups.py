# pivots to matchup rows, creates diff features
# → matchup_features.csv  (X)  +  labels.csv (y)

import pandas as pd
from pathlib import Path

ELO_DIR = Path("processed/elo")
MATCHUP_DIR = Path("processed/single_matchups")
MATCHUP_DIR.mkdir(exist_ok=True)

in_path = ELO_DIR / "team_with_elo_validation_set.csv"
out_path_x = MATCHUP_DIR / "matchup_features_validation_set.csv"
out_path_y = MATCHUP_DIR / "labels_validation_set.csv"


df = pd.read_csv(in_path, parse_dates=["date_utc"])

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

X.round(4).to_csv(out_path_x, index=False)
y.round(4).to_csv(out_path_y, index=False)
print("Matchup features and labels saved successfully.")