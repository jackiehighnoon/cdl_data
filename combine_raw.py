import pandas as pd
from pathlib import Path
from collections import defaultdict

RAW_DIR = Path("raw_tables")
CLEAN_DIR = Path("processed")
CLEAN_DIR.mkdir(exist_ok=True)

meta_df   = pd.read_csv(RAW_DIR / "meta.csv", parse_dates=["date_utc"])
team_df   = pd.read_csv(RAW_DIR / "team_series.csv")
player_df = pd.read_csv(RAW_DIR / "player_stats.csv")

meta_df["dayofweek"] = meta_df["date_utc"].dt.dayofweek
meta_df["hour"] = meta_df["date_utc"].dt.hour             
meta_df["is_weekend"] = meta_df["dayofweek"].isin([5, 6])

# Merge player derived stats into team_df

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

# Output to processed folder

OUT = Path("processed")
OUT.mkdir(exist_ok=True)

team_df.to_csv(OUT / "team_combined.csv", index=False)