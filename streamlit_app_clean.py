import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from zoneinfo import ZoneInfo

# =========================================================
# 0) PAGE SETUP
# =========================================================

st.set_page_config(layout="wide")

st.image("FIFA-world-cup-2026-752x440.png")
st.title("R&C World Cup Sweepstake Dashboard")

st.caption(
    f"Last updated (UK): {datetime.now(ZoneInfo('Europe/London')).strftime('%d %b %Y, %H:%M')}"
)

# =========================================================
# 1) PARTICIPANTS
# =========================================================

participants = {
    "Audrey": ["Panama", "Uzbekistan", "England", "South Korea", "Netherlands"],
    "Esperanza": ["Belgium", "Jordan", "Switzerland", "New Zealand", "Mexico"],
    "Anna": ["Colombia", "Qatar", "Egypt", "Cape Verde", "Sweden"],
    "Becky": ["New Zealand", "Switzerland", "Senegal", "Bosnia and Herzegovina", "Austria"],
    "Anne-Sophie": ["Portugal", "Morocco", "Cape Verde", "Croatia", "DR Congo"],
    "Sophie": ["Czechia", "Australia", "Egypt", "Ghana", "Spain"],
    "Anil": ["Tunisia", "England", "Paraguay", "Iran", "Panama"],
    "Enrique": ["Norway", "Paraguay", "Australia", "Iraq", "Ivory Coast"],
    "Sam": ["South Korea", "Algeria", "South Africa", "Norway", "Saudi Arabia"],
    "Chris": ["Japan", "Haiti", "Ecuador", "France", "Uruguay"],
    "Akhil": ["Saudi Arabia", "DR Congo", "France", "Algeria", "Canada"],
    "Scott": ["Netherlands", "Scotland", "Uzbekistan", "Haiti", "Morocco"],
    "Sonam": ["Sweden", "Ghana", "Canada", "Colombia", "Czechia"],
    "Zoey": ["Ivory Coast", "Bosnia and Herzegovina", "Spain", "Japan", "Brazil"],
    "Pavan": ["Iran", "South Africa", "Brazil", "Qatar", "Argentina"],
    "Spyros": ["Mexico", "Senegal", "Jordan", "United States", "Ecuador"],
    "Rajiv": ["Germany", "United States", "Argentina", "Tunisia", "Belgium"],
    "Kash": ["Croatia", "Uruguay", "Portugal", "Germany", "Curacao"],
    "Salima": ["Curacao", "Iraq", "Turkey", "Scotland", "Senegal"],
    "Barlas": ["Austria", "Turkey", "Qatar", "Algeria", "Switzerland"]
}

# =========================================================
# 2) TEAM NAME NORMALISATION
# =========================================================

TEAM_ALIASES = {
    "Korea Republic": "South Korea",
    "USA": "United States",
    "IR Iran": "Iran",
    "Türkiye": "Turkey",
    "Côte d'Ivoire": "Ivory Coast",
    "Curaçao": "Curacao",
    "Congo DR": "DR Congo",
    "Cabo Verde": "Cape Verde",
}

def canonical_team(name):
    return TEAM_ALIASES.get(str(name), str(name))

def is_placeholder_team(name):
    name = str(name)
    return (
        name.startswith("1")
        or name.startswith("2")
        or name.startswith("3")
        or name.startswith("W")
        or name.startswith("RU")
    )

# =========================================================
# 2B) ELIMINATION / DISPLAY HELPERS
# =========================================================

GROUP_STAGE_ELIMINATED_TEAMS = {
    "Czechia",
    "South Korea",
    "Qatar",
    "Haiti",
    "Scotland",
    "Turkey",
    "Curacao",
    "Tunisia",
    "New Zealand",
    "Iran",
    "Uruguay",
    "Saudi Arabia",
    "Iraq",
    "Jordan",
    "Uzbekistan",
    "Panama",
}

KNOCKOUT_STAGES = {"R32", "R16", "QF", "SF", "Final"}

def strike_text(text):
    """
    Unicode strikethrough so it works in Streamlit dataframes and matplotlib labels.
    """
    text = str(text)
    return "".join(char + "\u0336" for char in text)

def display_team(team, eliminated_teams):
    """
    Display canonical team name, struck-through if eliminated.
    """
    team = canonical_team(team)

    if is_placeholder_team(team):
        return team

    return strike_text(team) if team in eliminated_teams else team

def normalise_pen_winner(value, home, away):
    """
    Accepts pen_winner as:
      - "home" / "away"
      - "H" / "A"
      - actual team name, e.g. "France"
      - None
    """
    if value is None:
        return None

    value_str = str(value).strip()
    value_lower = value_str.lower()

    home = canonical_team(home)
    away = canonical_team(away)

    if value_lower in {"home", "h"}:
        return home

    if value_lower in {"away", "a"}:
        return away

    value_team = canonical_team(value_str)

    if value_team == home:
        return home

    if value_team == away:
        return away

    return None

def get_match_winner_loser(match):
    """
    Returns (winner, loser).

    For group-stage matches:
      - Draw returns (None, None)

    For knockout matches:
      - If goals are unequal, winner is decided by goals.
      - If goals are equal, winner comes from pen_winner.
    """
    stage = match["stage"]
    home = canonical_team(match["home"])
    away = canonical_team(match["away"])
    hg = match["home_goals"]
    ag = match["away_goals"]

    if hg is None or ag is None:
        return None, None

    if is_placeholder_team(home) or is_placeholder_team(away):
        return None, None

    if hg > ag:
        return home, away

    if ag > hg:
        return away, home

    # Draw
    if stage in KNOCKOUT_STAGES:
        pen_winner = normalise_pen_winner(match.get("pen_winner"), home, away)

        if pen_winner == home:
            return home, away

        if pen_winner == away:
            return away, home

    return None, None

def calculate_eliminated_teams(fixtures):
    """
    Starts with known group-stage eliminations, then adds knockout losers
    once results are entered.
    """
    eliminated = set(GROUP_STAGE_ELIMINATED_TEAMS)

    for match in fixtures:
        stage = match["stage"]

        if stage not in KNOCKOUT_STAGES:
            continue

        winner, loser = get_match_winner_loser(match)

        if winner is not None and loser is not None:
            eliminated.add(loser)

    return eliminated

def format_score(match):
    """
    Handles normal score and penalty score display.

    Example:
      1-1 (France win 4-3 pens)
    """
    hg = match["home_goals"]
    ag = match["away_goals"]

    if hg is None or ag is None:
        return ""

    base_score = f"{hg}-{ag}"
    stage = match["stage"]

    if stage in KNOCKOUT_STAGES and hg == ag:
        home = canonical_team(match["home"])
        away = canonical_team(match["away"])
        pen_winner = normalise_pen_winner(match.get("pen_winner"), home, away)

        home_pens = match.get("home_pens")
        away_pens = match.get("away_pens")

        if pen_winner is not None and home_pens is not None and away_pens is not None:
            return f"{base_score} ({pen_winner} win {home_pens}-{away_pens} pens)"

        if pen_winner is not None:
            return f"{base_score} ({pen_winner} win on pens)"

    return base_score

# =========================================================
# 3) SCORING RULES
# =========================================================

STAGE_BONUS = {
    "R32": 5,
    "R16": 5,
    "QF": 5,
    "SF": 5,
    "Final": 10,
}

FINAL_WINNER_BONUS = 10

# =========================================================
# 4) FIXTURES
#    Update scores manually by replacing None with integers
#
#    For knockout games decided on penalties:
#
#    {
#        "date": "2026-06-28",
#        "stage": "R32",
#        "home": "South Africa",
#        "away": "Canada",
#        "home_goals": 1,
#        "away_goals": 1,
#        "pen_winner": "home",
#        "home_pens": 4,
#        "away_pens": 3,
#    }
#
#    pen_winner can be:
#      - "home"
#      - "away"
#      - actual team name
# =========================================================

fixtures = [
    # Thu 11 Jun
    {"date": "2026-06-11", "stage": "Group", "group": "A", "home": "Mexico", "away": "South Africa", "home_goals": 2, "away_goals": 0},
    {"date": "2026-06-11", "stage": "Group", "group": "A", "home": "Korea Republic", "away": "Czechia", "home_goals": 2, "away_goals": 1},

    # Fri 12 Jun
    {"date": "2026-06-12", "stage": "Group", "group": "B", "home": "Canada", "away": "Bosnia and Herzegovina", "home_goals": 1, "away_goals": 1},
    {"date": "2026-06-12", "stage": "Group", "group": "D", "home": "USA", "away": "Paraguay", "home_goals": 4, "away_goals": 1},

    # Sat 13 Jun
    {"date": "2026-06-13", "stage": "Group", "group": "B", "home": "Qatar", "away": "Switzerland", "home_goals": 1, "away_goals": 1},
    {"date": "2026-06-13", "stage": "Group", "group": "C", "home": "Brazil", "away": "Morocco", "home_goals": 1, "away_goals": 1},

    # Sun 14 Jun
    {"date": "2026-06-14", "stage": "Group", "group": "C", "home": "Haiti", "away": "Scotland", "home_goals": 0, "away_goals": 1},
    {"date": "2026-06-14", "stage": "Group", "group": "D", "home": "Australia", "away": "Türkiye", "home_goals": 2, "away_goals": 0},
    {"date": "2026-06-14", "stage": "Group", "group": "E", "home": "Germany", "away": "Curaçao", "home_goals": 7, "away_goals": 1},
    {"date": "2026-06-14", "stage": "Group", "group": "F", "home": "Netherlands", "away": "Japan", "home_goals": 2, "away_goals": 2},
    {"date": "2026-06-14", "stage": "Group", "group": "E", "home": "Côte d'Ivoire", "away": "Ecuador", "home_goals": 1, "away_goals": 0},

    # Mon 15 Jun
    {"date": "2026-06-15", "stage": "Group", "group": "F", "home": "Sweden", "away": "Tunisia", "home_goals": 5, "away_goals": 1},
    {"date": "2026-06-15", "stage": "Group", "group": "H", "home": "Spain", "away": "Cabo Verde", "home_goals": 0, "away_goals": 0},
    {"date": "2026-06-15", "stage": "Group", "group": "G", "home": "Belgium", "away": "Egypt", "home_goals": 1, "away_goals": 1},
    {"date": "2026-06-15", "stage": "Group", "group": "H", "home": "Saudi Arabia", "away": "Uruguay", "home_goals": 1, "away_goals": 1},

    # Tue 16 Jun
    {"date": "2026-06-16", "stage": "Group", "group": "G", "home": "IR Iran", "away": "New Zealand", "home_goals": 2, "away_goals": 2},
    {"date": "2026-06-16", "stage": "Group", "group": "I", "home": "France", "away": "Senegal", "home_goals": 3, "away_goals": 1},
    {"date": "2026-06-16", "stage": "Group", "group": "I", "home": "Iraq", "away": "Norway", "home_goals": 1, "away_goals": 4},

    # Wed 17 Jun
    {"date": "2026-06-17", "stage": "Group", "group": "J", "home": "Argentina", "away": "Algeria", "home_goals": 3, "away_goals": 0},
    {"date": "2026-06-17", "stage": "Group", "group": "J", "home": "Austria", "away": "Jordan", "home_goals": 3, "away_goals": 1},
    {"date": "2026-06-17", "stage": "Group", "group": "K", "home": "Portugal", "away": "Congo DR", "home_goals": 1, "away_goals": 1},
    {"date": "2026-06-17", "stage": "Group", "group": "L", "home": "England", "away": "Croatia", "home_goals": 4, "away_goals": 2},
    {"date": "2026-06-17", "stage": "Group", "group": "L", "home": "Ghana", "away": "Panama", "home_goals": 1, "away_goals": 0},

    # Thu 18 Jun
    {"date": "2026-06-18", "stage": "Group", "group": "K", "home": "Uzbekistan", "away": "Colombia", "home_goals": 1, "away_goals": 3},
    {"date": "2026-06-18", "stage": "Group", "group": "A", "home": "Czechia", "away": "South Africa", "home_goals": 1, "away_goals": 1},
    {"date": "2026-06-18", "stage": "Group", "group": "B", "home": "Switzerland", "away": "Bosnia and Herzegovina", "home_goals": 4, "away_goals": 1},
    {"date": "2026-06-18", "stage": "Group", "group": "B", "home": "Canada", "away": "Qatar", "home_goals": 6, "away_goals": 0},

    # Fri 19 Jun
    {"date": "2026-06-19", "stage": "Group", "group": "A", "home": "Mexico", "away": "Korea Republic", "home_goals": 1, "away_goals": 0},
    {"date": "2026-06-19", "stage": "Group", "group": "D", "home": "USA", "away": "Australia", "home_goals": 2, "away_goals": 0},
    {"date": "2026-06-19", "stage": "Group", "group": "C", "home": "Scotland", "away": "Morocco", "home_goals": 0, "away_goals": 1},

    # Sat 20 Jun
    {"date": "2026-06-20", "stage": "Group", "group": "C", "home": "Brazil", "away": "Haiti", "home_goals": 3, "away_goals": 0},
    {"date": "2026-06-20", "stage": "Group", "group": "D", "home": "Türkiye", "away": "Paraguay", "home_goals": 0, "away_goals": 1},
    {"date": "2026-06-20", "stage": "Group", "group": "F", "home": "Netherlands", "away": "Sweden", "home_goals": 5, "away_goals": 1},
    {"date": "2026-06-20", "stage": "Group", "group": "E", "home": "Germany", "away": "Côte d'Ivoire", "home_goals": 2, "away_goals": 1},

    # Sun 21 Jun
    {"date": "2026-06-21", "stage": "Group", "group": "E", "home": "Ecuador", "away": "Curaçao", "home_goals": 0, "away_goals": 0},
    {"date": "2026-06-21", "stage": "Group", "group": "F", "home": "Tunisia", "away": "Japan", "home_goals": 0, "away_goals": 4},
    {"date": "2026-06-21", "stage": "Group", "group": "H", "home": "Spain", "away": "Saudi Arabia", "home_goals": 4, "away_goals": 0},
    {"date": "2026-06-21", "stage": "Group", "group": "G", "home": "Belgium", "away": "IR Iran", "home_goals": 0, "away_goals": 0},
    {"date": "2026-06-21", "stage": "Group", "group": "H", "home": "Uruguay", "away": "Cabo Verde", "home_goals": 2, "away_goals": 2},

    # Mon 22 Jun
    {"date": "2026-06-22", "stage": "Group", "group": "G", "home": "New Zealand", "away": "Egypt", "home_goals": 1, "away_goals": 3},
    {"date": "2026-06-22", "stage": "Group", "group": "J", "home": "Argentina", "away": "Austria", "home_goals": 2, "away_goals": 0},
    {"date": "2026-06-22", "stage": "Group", "group": "I", "home": "France", "away": "Iraq", "home_goals": 3, "away_goals": 0},

    # Tue 23 Jun
    {"date": "2026-06-23", "stage": "Group", "group": "I", "home": "Norway", "away": "Senegal", "home_goals": 3, "away_goals": 2},
    {"date": "2026-06-23", "stage": "Group", "group": "J", "home": "Jordan", "away": "Algeria", "home_goals": 1, "away_goals": 2},
    {"date": "2026-06-23", "stage": "Group", "group": "K", "home": "Portugal", "away": "Uzbekistan", "home_goals": 5, "away_goals": 0},
    {"date": "2026-06-23", "stage": "Group", "group": "L", "home": "England", "away": "Ghana", "home_goals": 0, "away_goals": 0},
    {"date": "2026-06-23", "stage": "Group", "group": "L", "home": "Panama", "away": "Croatia", "home_goals": 0, "away_goals": 1},

    # Wed 24 Jun
    {"date": "2026-06-24", "stage": "Group", "group": "K", "home": "Colombia", "away": "Congo DR", "home_goals": 1, "away_goals": 0},
    {"date": "2026-06-24", "stage": "Group", "group": "B", "home": "Switzerland", "away": "Canada", "home_goals": 2, "away_goals": 1},
    {"date": "2026-06-24", "stage": "Group", "group": "B", "home": "Bosnia and Herzegovina", "away": "Qatar", "home_goals": 3, "away_goals": 1},
    {"date": "2026-06-24", "stage": "Group", "group": "C", "home": "Scotland", "away": "Brazil", "home_goals": 0, "away_goals": 3},
    {"date": "2026-06-24", "stage": "Group", "group": "C", "home": "Morocco", "away": "Haiti", "home_goals": 4, "away_goals": 2},

    # Thu 25 Jun
    {"date": "2026-06-25", "stage": "Group", "group": "A", "home": "Czechia", "away": "Mexico", "home_goals": 0, "away_goals": 3},
    {"date": "2026-06-25", "stage": "Group", "group": "A", "home": "South Africa", "away": "Korea Republic", "home_goals": 1, "away_goals": 0},
    {"date": "2026-06-25", "stage": "Group", "group": "E", "home": "Curaçao", "away": "Côte d'Ivoire", "home_goals": 0, "away_goals": 2},
    {"date": "2026-06-25", "stage": "Group", "group": "E", "home": "Ecuador", "away": "Germany", "home_goals": 2, "away_goals": 1},
    {"date": "2026-06-25", "stage": "Group", "group": "F", "home": "Japan", "away": "Sweden", "home_goals": 1, "away_goals": 1},
    {"date": "2026-06-25", "stage": "Group", "group": "F", "home": "Tunisia", "away": "Netherlands", "home_goals": 1, "away_goals": 3},

    # Fri 26 Jun
    {"date": "2026-06-26", "stage": "Group", "group": "D", "home": "Türkiye", "away": "USA", "home_goals": 3, "away_goals": 2},
    {"date": "2026-06-26", "stage": "Group", "group": "D", "home": "Paraguay", "away": "Australia", "home_goals": 0, "away_goals": 0},
    {"date": "2026-06-26", "stage": "Group", "group": "I", "home": "Norway", "away": "France", "home_goals": 1, "away_goals": 4},
    {"date": "2026-06-26", "stage": "Group", "group": "I", "home": "Senegal", "away": "Iraq", "home_goals": 5, "away_goals": 0},

    # Sat 27 Jun
    {"date": "2026-06-27", "stage": "Group", "group": "H", "home": "Cabo Verde", "away": "Saudi Arabia", "home_goals": 0, "away_goals": 0},
    {"date": "2026-06-27", "stage": "Group", "group": "H", "home": "Uruguay", "away": "Spain", "home_goals": 0, "away_goals": 1},
    {"date": "2026-06-27", "stage": "Group", "group": "G", "home": "Egypt", "away": "IR Iran", "home_goals": 1, "away_goals": 1},
    {"date": "2026-06-27", "stage": "Group", "group": "G", "home": "New Zealand", "away": "Belgium", "home_goals": 1, "away_goals": 5},
    {"date": "2026-06-27", "stage": "Group", "group": "L", "home": "Panama", "away": "England", "home_goals": 0, "away_goals": 2},
    {"date": "2026-06-27", "stage": "Group", "group": "L", "home": "Croatia", "away": "Ghana", "home_goals": 2, "away_goals": 1},
    {"date": "2026-06-27", "stage": "Group", "group": "K", "home": "Colombia", "away": "Portugal", "home_goals": 0, "away_goals": 0},
    {"date": "2026-06-27", "stage": "Group", "group": "K", "home": "Congo DR", "away": "Uzbekistan", "home_goals": 3, "away_goals": 1},

    # Sun 28 Jun
    {"date": "2026-06-28", "stage": "Group", "group": "J", "home": "Algeria", "away": "Austria", "home_goals": 3, "away_goals": 3},
    {"date": "2026-06-28", "stage": "Group", "group": "J", "home": "Jordan", "away": "Argentina", "home_goals": 1, "away_goals": 3},

    # -------------------------
    # ROUND OF 32
    # -------------------------

    {"date": "2026-06-28", "stage": "R32", "home": "South Africa", "away": "Canada", "home_goals": 0, "away_goals": 1},
    {"date": "2026-06-29", "stage": "R32", "home": "Brazil", "away": "Japan", "home_goals": 2, "away_goals": 1},
    {"date": "2026-06-29", "stage": "R32", "home": "Germany", "away": "Paraguay", "home_goals": 1, "away_goals": 1, "pen_winner": "away", "home_pens": 3, "away_pens": 4},
    {"date": "2026-06-30", "stage": "R32", "home": "Netherlands", "away": "Morocco", "home_goals": 1, "away_goals": 1, "pen_winner": "away", "home_pens": 2, "away_pens": 3},
    {"date": "2026-06-30", "stage": "R32", "home": "Ivory Coast", "away": "Norway", "home_goals": 1, "away_goals": 2},
    {"date": "2026-06-30", "stage": "R32", "home": "France", "away": "Sweden", "home_goals": 3, "away_goals": 0},
    {"date": "2026-07-01", "stage": "R32", "home": "Mexico", "away": "Ecuador", "home_goals": 2, "away_goals": 0},
    {"date": "2026-07-01", "stage": "R32", "home": "England", "away": "DR Congo", "home_goals": 2, "away_goals": 1},
    {"date": "2026-07-01", "stage": "R32", "home": "Belgium", "away": "Senegal", "home_goals": 3, "away_goals": 2},
    {"date": "2026-07-02", "stage": "R32", "home": "United States", "away": "Bosnia and Herzegovina", "home_goals": 2, "away_goals": 0},
    {"date": "2026-07-02", "stage": "R32", "home": "Spain", "away": "Austria", "home_goals": 3, "away_goals": 0},
    {"date": "2026-07-02", "stage": "R32", "home": "Portugal", "away": "Croatia", "home_goals": 2, "away_goals": 1},
    {"date": "2026-07-03", "stage": "R32", "home": "Switzerland", "away": "Algeria", "home_goals": 2, "away_goals": 0},
    {"date": "2026-07-03", "stage": "R32", "home": "Australia", "away": "Egypt", "home_goals": 1, "away_goals": 1, "pen_winner": "away", "home_pens": 2, "away_pens": 4},
    {"date": "2026-07-03", "stage": "R32", "home": "Argentina", "away": "Cape Verde", "home_goals": 3, "away_goals": 2},
    {"date": "2026-07-04", "stage": "R32", "home": "Colombia", "away": "Ghana", "home_goals": 1, "away_goals": 0},

    # -------------------------
    # ROUND OF 16
    # -------------------------

# -------------------------
    # ROUND OF 16
    # -------------------------

    {"date": "2026-07-04", "stage": "R16", "home": "Paraguay", "away": "France", "home_goals": None, "away_goals": None},
    {"date": "2026-07-04", "stage": "R16", "home": "Canada", "away": "Morocco", "home_goals": None, "away_goals": None},
    {"date": "2026-07-05", "stage": "R16", "home": "Brazil", "away": "Norway", "home_goals": None, "away_goals": None},
    {"date": "2026-07-05", "stage": "R16", "home": "Mexico", "away": "England", "home_goals": None, "away_goals": None},
    {"date": "2026-07-06", "stage": "R16", "home": "Portugal", "away": "Spain", "home_goals": None, "away_goals": None},
    {"date": "2026-07-06", "stage": "R16", "home": "United States", "away": "Belgium", "home_goals": None, "away_goals": None},
    {"date": "2026-07-07", "stage": "R16", "home": "Argentina", "away": "Egypt", "home_goals": None, "away_goals": None},
    {"date": "2026-07-07", "stage": "R16", "home": "Switzerland", "away": "Colombia", "home_goals": None, "away_goals": None},

    # -------------------------
    # QUARTER-FINALS
    # -------------------------

    {"date": "2026-07-09", "stage": "QF", "home": "W89", "away": "W90", "home_goals": None, "away_goals": None},
    {"date": "2026-07-10", "stage": "QF", "home": "W93", "away": "W94", "home_goals": None, "away_goals": None},
    {"date": "2026-07-11", "stage": "QF", "home": "W91", "away": "W92", "home_goals": None, "away_goals": None},
    {"date": "2026-07-12", "stage": "QF", "home": "W95", "away": "W96", "home_goals": None, "away_goals": None},

    # -------------------------
    # SEMI-FINALS
    # -------------------------

    {"date": "2026-07-14", "stage": "SF", "home": "W97", "away": "W98", "home_goals": None, "away_goals": None},
    {"date": "2026-07-15", "stage": "SF", "home": "W99", "away": "W100", "home_goals": None, "away_goals": None},

    # -------------------------
    # THIRD-PLACE PLAY-OFF AND FINAL
    # -------------------------

    {"date": "2026-07-18", "stage": "Third", "home": "RU101", "away": "RU102", "home_goals": None, "away_goals": None},
    {"date": "2026-07-19", "stage": "Final", "home": "W101", "away": "W102", "home_goals": None, "away_goals": None},
]

# =========================================================
# 5) SCORING ENGINE
# =========================================================

def calculate_team_scores(fixtures):
    team_scores = {}

    def ensure_team(team):
        if team not in team_scores:
            team_scores[team] = 0

    for match in fixtures:
        stage = match["stage"]
        home = canonical_team(match["home"])
        away = canonical_team(match["away"])
        hg = match["home_goals"]
        ag = match["away_goals"]

        if hg is None or ag is None:
            continue

        if is_placeholder_team(home) or is_placeholder_team(away):
            continue

        ensure_team(home)
        ensure_team(away)

        if stage == "Group":
            if hg > ag:
                team_scores[home] += 3
            elif ag > hg:
                team_scores[away] += 3
            else:
                team_scores[home] += 1
                team_scores[away] += 1

        elif stage in KNOCKOUT_STAGES:
            winner, loser = get_match_winner_loser(match)

            if winner is None:
                # Protects against a knockout draw being entered without pen_winner.
                continue

            ensure_team(winner)
            team_scores[winner] += STAGE_BONUS[stage]

            if stage == "Final":
                team_scores[winner] += FINAL_WINNER_BONUS

    return team_scores

# =========================================================
# 6) TABLE BUILDERS
# =========================================================

def build_leaderboard(participants, team_scores, eliminated_teams):
    rows = []

    for person, teams in participants.items():
        canonical_teams = [canonical_team(team) for team in teams]
        current_points = sum(team_scores.get(team, 0) for team in canonical_teams)

        rows.append({
            "Name": person,
            "Points": current_points,
            "Team 1": display_team(canonical_teams[0], eliminated_teams),
            "Team 2": display_team(canonical_teams[1], eliminated_teams),
            "Team 3": display_team(canonical_teams[2], eliminated_teams),
            "Team 4": display_team(canonical_teams[3], eliminated_teams),
            "Team 5": display_team(canonical_teams[4], eliminated_teams),
        })

    df = (
        pd.DataFrame(rows)
        .sort_values(["Points", "Name"], ascending=[False, True])
        .reset_index(drop=True)
    )

    df.index = df.index + 1
    df.index.name = "Rank"

    return df

def build_team_scores(team_scores, eliminated_teams):
    if not team_scores:
        return pd.DataFrame(columns=["Team", "Points", "Status"])

    rows = []

    for team, points in team_scores.items():
        team = canonical_team(team)

        rows.append({
            "Team": display_team(team, eliminated_teams),
            "Raw Team": team,
            "Points": points,
            "Status": "Eliminated" if team in eliminated_teams else "Active",
        })

    df = pd.DataFrame(rows)

    return (
        df.sort_values(["Points", "Raw Team"], ascending=[False, True])
        .drop(columns=["Raw Team"])
        .reset_index(drop=True)
    )

def build_played_matches(fixtures, eliminated_teams):
    rows = []

    for match in fixtures:
        if match["home_goals"] is not None and match["away_goals"] is not None:
            home = canonical_team(match["home"])
            away = canonical_team(match["away"])

            rows.append({
                "Date": match["date"],
                "Stage": match["stage"],
                "Group": match.get("group", ""),
                "Home": display_team(home, eliminated_teams),
                "Away": display_team(away, eliminated_teams),
                "Score": format_score(match),
            })

    if not rows:
        return pd.DataFrame(columns=["Date", "Stage", "Group", "Home", "Away", "Score"])

    return pd.DataFrame(rows).reset_index(drop=True)

def build_upcoming_matches(fixtures, eliminated_teams):
    rows = []

    for match in fixtures:
        if match["home_goals"] is None or match["away_goals"] is None:
            home = canonical_team(match["home"])
            away = canonical_team(match["away"])

            rows.append({
                "Date": match["date"],
                "Stage": match["stage"],
                "Group": match.get("group", ""),
                "Home": display_team(home, eliminated_teams),
                "Away": display_team(away, eliminated_teams),
            })

    if not rows:
        return pd.DataFrame(columns=["Date", "Stage", "Group", "Home", "Away"])

    return pd.DataFrame(rows).reset_index(drop=True)

def person_team_breakdown(person, participants, team_scores, eliminated_teams):
    rows = []

    for team in participants[person]:
        team = canonical_team(team)

        rows.append({
            "Team": display_team(team, eliminated_teams),
            "Raw Team": team,
            "Points": team_scores.get(team, 0),
            "Status": "Eliminated" if team in eliminated_teams else "Active",
        })

    df = pd.DataFrame(rows)

    return (
        df.sort_values(["Points", "Raw Team"], ascending=[False, True])
        .drop(columns=["Raw Team"])
        .reset_index(drop=True)
    )

# =========================================================
# 7) BUILD DATA
# =========================================================

eliminated_teams = calculate_eliminated_teams(fixtures)
team_scores = calculate_team_scores(fixtures)

# Award R32 qualification points (before matches are played)
r32_teams = set()

for match in fixtures:
    if match["stage"] == "R32":
        r32_teams.add(canonical_team(match["home"]))
        r32_teams.add(canonical_team(match["away"]))

for team in r32_teams:
    if not is_placeholder_team(team):
        team_scores[team] = team_scores.get(team, 0) + STAGE_BONUS["R32"]

leaderboard = build_leaderboard(participants, team_scores, eliminated_teams)
team_scores_df = build_team_scores(team_scores, eliminated_teams)
played_matches_df = build_played_matches(fixtures, eliminated_teams)
upcoming_matches_df = build_upcoming_matches(fixtures, eliminated_teams)

# =========================================================
# 8) TOP HIGHLIGHT
# =========================================================

leader_name = leaderboard.iloc[0]["Name"] if not leaderboard.empty else "—"
leader_points = int(leaderboard.iloc[0]["Points"]) if not leaderboard.empty else 0

m1 = st.columns(1)[0]
m1.metric("🥇 Current Leader", leader_name, leader_points)

# =========================================================
# 9) LEADERBOARD TABLE WITH HIGHLIGHTS
# =========================================================

st.subheader("Leaderboard")

def highlight_leaderboard(row):
    rank = row.name

    if rank == 1:
        return ["background-color: #FFD700; color: black; font-weight: bold;"] * len(row)

    if rank == 2:
        return ["background-color: #C0C0C0; color: black; font-weight: bold;"] * len(row)

    if rank == 3:
        return ["background-color: #CD7F32; color: white; font-weight: bold;"] * len(row)

    return [""] * len(row)

styled_leaderboard = leaderboard.style.apply(highlight_leaderboard, axis=1)
st.dataframe(styled_leaderboard, use_container_width=True)

# =========================================================
# 10) TEAM SCORES / MATCHES
# =========================================================

left, right = st.columns([1, 1])

with left:
    st.subheader("Team Scores")
    st.dataframe(team_scores_df, use_container_width=True, hide_index=True)

with right:
    st.subheader("Played Matches")
    st.dataframe(played_matches_df, use_container_width=True, hide_index=True)

# =========================================================
# 11) UPCOMING MATCHES
# =========================================================

st.subheader("Upcoming Matches")
st.dataframe(upcoming_matches_df, use_container_width=True, hide_index=True)

# =========================================================
# 12) PARTICIPANT BREAKDOWN
# =========================================================

st.subheader("Participant Breakdown")

participant_names = sorted(participants.keys())
default_index = participant_names.index("Sam") if "Sam" in participant_names else 0

selected_person = st.selectbox(
    "Select participant",
    participant_names,
    index=default_index,
)

selected_breakdown = person_team_breakdown(
    selected_person,
    participants,
    team_scores,
    eliminated_teams,
)

left2, right2 = st.columns([1, 1])

with left2:
    st.markdown(f"### {selected_person}'s teams")
    st.dataframe(selected_breakdown, use_container_width=True, hide_index=True)

with right2:
    fig2, ax2 = plt.subplots(figsize=(8, 4))

    breakdown_sorted = selected_breakdown.sort_values("Points", ascending=True)

    ax2.barh(breakdown_sorted["Team"], breakdown_sorted["Points"])
    ax2.set_xlabel("Points")
    ax2.set_ylabel("Team")
    ax2.set_title(f"{selected_person} - Team Contribution")

    plt.tight_layout()
    st.pyplot(fig2)

# =========================================================
# 13) OPTIONAL LEADERBOARD CHART
# =========================================================

# st.subheader("Leaderboard Chart")
# fig, ax = plt.subplots(figsize=(10, 8))
# leaderboard_sorted = leaderboard.sort_values("Points", ascending=True)
# ax.barh(leaderboard_sorted["Name"], leaderboard_sorted["Points"])
# ax.set_xlabel("Points")
# ax.set_ylabel("Person")
# ax.set_title("Sweepstake Leaderboard")
# plt.tight_layout()
# st.pyplot(fig)
