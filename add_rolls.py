# reads team_combined.csv → team_with_rolls.csv
import pandas as pd
from pathlib import Path

# Rolling average past 5 matches
ROLL = 5

CLEAN_DIR = Path("processed")
ROLL_DIR = Path ("processed/rolls")
ROLL_DIR.mkdir(exist_ok=True)

df = pd.read_csv(CLEAN_DIR / "team_combined.csv")

ROLL_COLS = ["series_kills", "series_deaths", "series_damage", "series_kdr", "avg_bp_rtg","bp_std","bp_max","top_kills_share","bp_range"]

def add_rolls(df: pd.DataFrame, roll: int=ROLL):
    df = df.sort_values(["team_name","date_utc"]).reset_index(drop=True)

    rolling = (
        df.groupby(["team_name"])[ROLL_COLS]
        .rolling(roll)
        .mean()
        .reset_index()
    )

    rolling = rolling.rename(columns={col: f"{col}_roll" for col in ROLL_COLS})

    df = df.merge(rolling, left_index=True, right_on="level_1").drop(columns=["level_1"])

    df = df.dropna(subset=[f"{col}_roll" for col in ROLL_COLS]).reset_index(drop=True)
    return df

df = add_rolls(df, ROLL)

df = df.drop(columns=["team_name_y"]).rename(columns={"team_name_x": "team_name"})

# Output to processed folder
df.round(4).to_csv(ROLL_DIR / "team_with_rolls.csv", index=False)