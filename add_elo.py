# (optional) adds pre‑match Elo to team_with_rolls.csv

from pathlib import Path
import pandas as pd

INITIAL_ELO = 1500
K_FACTOR = 32

CLEAN_DIR = Path("processed/rolls")
ELO_DIR = Path ("processed/elo")
ELO_DIR.mkdir(exist_ok=True)

df = pd.read_csv(CLEAN_DIR / "team_with_rolls.csv")

# Sort data by time of match

df = df.sort_values(["date_utc"]).reset_index(drop=True)

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

df.to_csv(ELO_DIR / "team_with_elo.csv", index=False)  # Output to processed folder




