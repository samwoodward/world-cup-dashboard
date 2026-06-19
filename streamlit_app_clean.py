import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from zoneinfo import ZoneInfo

#st.image("https://upload.wikimedia.org/wikipedia/en/1/17/2026_FIFA_World_Cup_emblem.svg")
st.image("FIFA-world-cup-2026-752x440.png")
st.set_page_config(layout="wide")
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
    "Cabo Verde": "Cape Verde"
}

def canonical_team(name):
    return TEAM_ALIASES.get(name, name)

# =========================================================
# 3) SCORING RULES
# =========================================================

STAGE_BONUS = {
    "R32": 5,
    "R16": 5,
    "QF": 5,
    "SF": 5,
    "Final": 10
}

FINAL_WINNER_BONUS = 10

# =========================================================
# 4) FIXTURES
#    Update scores manually by replacing None with integers
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
    {"date": "2026-06-19", "stage": "Group", "group": "D", "home": "USA", "away": "Australia", "home_goals": None, "away_goals": None},
    {"date": "2026-06-19", "stage": "Group", "group": "C", "home": "Scotland", "away": "Morocco", "home_goals": None, "away_goals": None},

    # Sat 20 Jun
    {"date": "2026-06-20", "stage": "Group", "group": "C", "home": "Brazil", "away": "Haiti", "home_goals": None, "away_goals": None},
    {"date": "2026-06-20", "stage": "Group", "group": "D", "home": "Türkiye", "away": "Paraguay", "home_goals": None, "away_goals": None},
    {"date": "2026-06-20", "stage": "Group", "group": "F", "home": "Netherlands", "away": "Sweden", "home_goals": None, "away_goals": None},
    {"date": "2026-06-20", "stage": "Group", "group": "E", "home": "Germany", "away": "Côte d'Ivoire", "home_goals": None, "away_goals": None},

    # Sun 21 Jun
    {"date": "2026-06-21", "stage": "Group", "group": "E", "home": "Ecuador", "away": "Curaçao", "home_goals": None, "away_goals": None},
    {"date": "2026-06-21", "stage": "Group", "group": "F", "home": "Tunisia", "away": "Japan", "home_goals": None, "away_goals": None},
    {"date": "2026-06-21", "stage": "Group", "group": "H", "home": "Spain", "away": "Saudi Arabia", "home_goals": None, "away_goals": None},
    {"date": "2026-06-21", "stage": "Group", "group": "G", "home": "Belgium", "away": "IR Iran", "home_goals": None, "away_goals": None},
    {"date": "2026-06-21", "stage": "Group", "group": "H", "home": "Uruguay", "away": "Cabo Verde", "home_goals": None, "away_goals": None},

    # Mon 22 Jun
    {"date": "2026-06-22", "stage": "Group", "group": "G", "home": "New Zealand", "away": "Egypt", "home_goals": None, "away_goals": None},
    {"date": "2026-06-22", "stage": "Group", "group": "J", "home": "Argentina", "away": "Austria", "home_goals": None, "away_goals": None},
    {"date": "2026-06-22", "stage": "Group", "group": "I", "home": "France", "away": "Iraq", "home_goals": None, "away_goals": None},

    # Tue 23 Jun
    {"date": "2026-06-23", "stage": "Group", "group": "I", "home": "Norway", "away": "Senegal", "home_goals": None, "away_goals": None},
    {"date": "2026-06-23", "stage": "Group", "group": "J", "home": "Jordan", "away": "Algeria", "home_goals": None, "away_goals": None},
    {"date": "2026-06-23", "stage": "Group", "group": "K", "home": "Portugal", "away": "Uzbekistan", "home_goals": None, "away_goals": None},
    {"date": "2026-06-23", "stage": "Group", "group": "L", "home": "England", "away": "Ghana", "home_goals": None, "away_goals": None},
    {"date": "2026-06-23", "stage": "Group", "group": "L", "home": "Panama", "away": "Croatia", "home_goals": None, "away_goals": None},

    # Wed 24 Jun
    {"date": "2026-06-24", "stage": "Group", "group": "K", "home": "Colombia", "away": "Congo DR", "home_goals": None, "away_goals": None},
    {"date": "2026-06-24", "stage": "Group", "group": "B", "home": "Switzerland", "away": "Canada", "home_goals": None, "away_goals": None},
    {"date": "2026-06-24", "stage": "Group", "group": "B", "home": "Bosnia and Herzegovina", "away": "Qatar", "home_goals": None, "away_goals": None},
    {"date": "2026-06-24", "stage": "Group", "group": "C", "home": "Scotland", "away": "Brazil", "home_goals": None, "away_goals": None},
    {"date": "2026-06-24", "stage": "Group", "group": "C", "home": "Morocco", "away": "Haiti", "home_goals": None, "away_goals": None},

    # Thu 25 Jun
    {"date": "2026-06-25", "stage": "Group", "group": "A", "home": "Czechia", "away": "Mexico", "home_goals": None, "away_goals": None},
    {"date": "2026-06-25", "stage": "Group", "group": "A", "home": "South Africa", "away": "Korea Republic", "home_goals": None, "away_goals": None},
    {"date": "2026-06-25", "stage": "Group", "group": "E", "home": "Curaçao", "away": "Côte d'Ivoire", "home_goals": None, "away_goals": None},
    {"date": "2026-06-25", "stage": "Group", "group": "E", "home": "Ecuador", "away": "Germany", "home_goals": None, "away_goals": None},
    {"date": "2026-06-25", "stage": "Group", "group": "F", "home": "Japan", "away": "Sweden", "home_goals": None, "away_goals": None},
    {"date": "2026-06-25", "stage": "Group", "group": "F", "home": "Tunisia", "away": "Netherlands", "home_goals": None, "away_goals": None},

    # Fri 26 Jun
    {"date": "2026-06-26", "stage": "Group", "group": "D", "home": "Türkiye", "away": "USA", "home_goals": None, "away_goals": None},
    {"date": "2026-06-26", "stage": "Group", "group": "D", "home": "Paraguay", "away": "Australia", "home_goals": None, "away_goals": None},
    {"date": "2026-06-26", "stage": "Group", "group": "I", "home": "Norway", "away": "France", "home_goals": None, "away_goals": None},
    {"date": "2026-06-26", "stage": "Group", "group": "I", "home": "Senegal", "away": "Iraq", "home_goals": None, "away_goals": None},

    # Sat 27 Jun
    {"date": "2026-06-27", "stage": "Group", "group": "H", "home": "Cabo Verde", "away": "Saudi Arabia", "home_goals": None, "away_goals": None},
    {"date": "2026-06-27", "stage": "Group", "group": "H", "home": "Uruguay", "away": "Spain", "home_goals": None, "away_goals": None},
    {"date": "2026-06-27", "stage": "Group", "group": "G", "home": "Egypt", "away": "IR Iran", "home_goals": None, "away_goals": None},
    {"date": "2026-06-27", "stage": "Group", "group": "G", "home": "New Zealand", "away": "Belgium", "home_goals": None, "away_goals": None},
    {"date": "2026-06-27", "stage": "Group", "group": "L", "home": "Panama", "away": "England", "home_goals": None, "away_goals": None},
    {"date": "2026-06-27", "stage": "Group", "group": "L", "home": "Croatia", "away": "Ghana", "home_goals": None, "away_goals": None},
    {"date": "2026-06-27", "stage": "Group", "group": "K", "home": "Colombia", "away": "Portugal", "home_goals": None, "away_goals": None},
    {"date": "2026-06-27", "stage": "Group", "group": "K", "home": "Congo DR", "away": "Uzbekistan", "home_goals": None, "away_goals": None},

    # Sun 28 Jun
    {"date": "2026-06-28", "stage": "Group", "group": "J", "home": "Algeria", "away": "Austria", "home_goals": None, "away_goals": None},
    {"date": "2026-06-28", "stage": "Group", "group": "J", "home": "Jordan", "away": "Argentina", "home_goals": None, "away_goals": None},

    # -------------------------
    # KNOCKOUT DUMMY LINES
    # -------------------------

    {"date": "2026-06-28", "stage": "R32", "home": "2A", "away": "2B", "home_goals": None, "away_goals": None},
    {"date": "2026-06-29", "stage": "R32", "home": "1C", "away": "2F", "home_goals": None, "away_goals": None},
    {"date": "2026-06-29", "stage": "R32", "home": "1E", "away": "3ABCDF", "home_goals": None, "away_goals": None},
    {"date": "2026-06-30", "stage": "R32", "home": "1F", "away": "2C", "home_goals": None, "away_goals": None},
    {"date": "2026-06-30", "stage": "R32", "home": "2E", "away": "2I", "home_goals": None, "away_goals": None},
    {"date": "2026-06-30", "stage": "R32", "home": "1I", "away": "3CDFGH", "home_goals": None, "away_goals": None},
    {"date": "2026-07-01", "stage": "R32", "home": "1A", "away": "3CEFHI", "home_goals": None, "away_goals": None},
    {"date": "2026-07-01", "stage": "R32", "home": "1L", "away": "3EHIJK", "home_goals": None, "away_goals": None},
    {"date": "2026-07-01", "stage": "R32", "home": "1G", "away": "3AEHIJ", "home_goals": None, "away_goals": None},
    {"date": "2026-07-02", "stage": "R32", "home": "1D", "away": "3BEFIJ", "home_goals": None, "away_goals": None},
    {"date": "2026-07-02", "stage": "R32", "home": "1H", "away": "2J", "home_goals": None, "away_goals": None},
    {"date": "2026-07-02", "stage": "R32", "home": "2K", "away": "2L", "home_goals": None, "away_goals": None},
    {"date": "2026-07-03", "stage": "R32", "home": "1B", "away": "3EFGIJ", "home_goals": None, "away_goals": None},
    {"date": "2026-07-03", "stage": "R32", "home": "2D", "away": "2G", "home_goals": None, "away_goals": None},
    {"date": "2026-07-03", "stage": "R32", "home": "1J", "away": "2H", "home_goals": None, "away_goals": None},
    {"date": "2026-07-04", "stage": "R32", "home": "1K", "away": "3DEIJL", "home_goals": None, "away_goals": None},

    {"date": "2026-07-04", "stage": "R16", "home": "W73", "away": "W75", "home_goals": None, "away_goals": None},
    {"date": "2026-07-04", "stage": "R16", "home": "W74", "away": "W77", "home_goals": None, "away_goals": None},
    {"date": "2026-07-05", "stage": "R16", "home": "W76", "away": "W78", "home_goals": None, "away_goals": None},
    {"date": "2026-07-06", "stage": "R16", "home": "W79", "away": "W80", "home_goals": None, "away_goals": None},
    {"date": "2026-07-06", "stage": "R16", "home": "W83", "away": "W84", "home_goals": None, "away_goals": None},
    {"date": "2026-07-07", "stage": "R16", "home": "W81", "away": "W82", "home_goals": None, "away_goals": None},
    {"date": "2026-07-07", "stage": "R16", "home": "W86", "away": "W88", "home_goals": None, "away_goals": None},
    {"date": "2026-07-07", "stage": "R16", "home": "W85", "away": "W87", "home_goals": None, "away_goals": None},

    {"date": "2026-07-09", "stage": "QF", "home": "W89", "away": "W90", "home_goals": None, "away_goals": None},
    {"date": "2026-07-10", "stage": "QF", "home": "W93", "away": "W94", "home_goals": None, "away_goals": None},
    {"date": "2026-07-11", "stage": "QF", "home": "W91", "away": "W92", "home_goals": None, "away_goals": None},
    {"date": "2026-07-12", "stage": "QF", "home": "W95", "away": "W96", "home_goals": None, "away_goals": None},

    {"date": "2026-07-14", "stage": "SF", "home": "W97", "away": "W98", "home_goals": None, "away_goals": None},
    {"date": "2026-07-15", "stage": "SF", "home": "W99", "away": "W100", "home_goals": None, "away_goals": None},

    {"date": "2026-07-18", "stage": "Third", "home": "RU101", "away": "RU102", "home_goals": None, "away_goals": None},
    {"date": "2026-07-19", "stage": "Final", "home": "W101", "away": "W102", "home_goals": None, "away_goals": None},
]

# =========================================================
# 5) SCORING ENGINE
# =========================================================

def is_placeholder_team(name):
    return (
        name.startswith("1") or
        name.startswith("2") or
        name.startswith("3") or
        name.startswith("W") or
        name.startswith("RU")
    )

def calculate_team_scores(fixtures):
    team_scores = {}

    def ensure_team(team):
        if team not in team_scores:
            team_scores[team] = 0

    for m in fixtures:
        stage = m["stage"]
        home = canonical_team(m["home"])
        away = canonical_team(m["away"])
        hg = m["home_goals"]
        ag = m["away_goals"]

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

        elif stage in ["R32", "R16", "QF", "SF", "Final"]:
            winner = home if hg > ag else away
            ensure_team(winner)
            team_scores[winner] += STAGE_BONUS[stage]

            if stage == "Final":
                team_scores[winner] += FINAL_WINNER_BONUS

    return team_scores

# =========================================================
# 6) TABLE BUILDERS
# =========================================================

def build_leaderboard(participants, team_scores):
    rows = []
    for person, teams in participants.items():
        current_points = sum(team_scores.get(team, 0) for team in teams)
        rows.append({
            "Name": person,
            "Points": current_points,
            "Team 1": teams[0],
            "Team 2": teams[1],
            "Team 3": teams[2],
            "Team 4": teams[3],
            "Team 5": teams[4],
        })

    df = pd.DataFrame(rows).sort_values(["Points", "Name"], ascending=[False, True]).reset_index(drop=True)
    df.index = df.index + 1
    df.index.name = "Rank"
    return df

def build_team_scores(team_scores):
    if not team_scores:
        return pd.DataFrame(columns=["Team", "Points"])
    return pd.DataFrame(
        [{"Team": k, "Points": v} for k, v in team_scores.items()]
    ).sort_values(["Points", "Team"], ascending=[False, True]).reset_index(drop=True)

def build_played_matches(fixtures):
    rows = []
    for m in fixtures:
        if m["home_goals"] is not None and m["away_goals"] is not None:
            rows.append({
                "Date": m["date"],
                "Stage": m["stage"],
                "Group": m.get("group", ""),
                "Home": canonical_team(m["home"]),
                "Away": canonical_team(m["away"]),
                "Score": f"{m['home_goals']}-{m['away_goals']}"
            })
    if not rows:
        return pd.DataFrame(columns=["Date", "Stage", "Group", "Home", "Away", "Score"])
    return pd.DataFrame(rows).reset_index(drop=True)

def person_team_breakdown(person, participants, team_scores):
    rows = []
    for team in participants[person]:
        rows.append({
            "Team": team,
            "Points": team_scores.get(team, 0)
        })
    return pd.DataFrame(rows).sort_values(["Points", "Team"], ascending=[False, True]).reset_index(drop=True)

# =========================================================
# 7) BUILD DATA
# =========================================================

team_scores = calculate_team_scores(fixtures)
leaderboard = build_leaderboard(participants, team_scores)
team_scores_df = build_team_scores(team_scores)
played_matches_df = build_played_matches(fixtures)

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
    elif rank == 2:
        return ["background-color: #C0C0C0; color: black; font-weight: bold;"] * len(row)
    elif rank == 3:
        return ["background-color: #CD7F32; color: white; font-weight: bold;"] * len(row)
    return [""] * len(row)

styled_leaderboard = leaderboard.style.apply(highlight_leaderboard, axis=1)
st.dataframe(styled_leaderboard, use_container_width=True)

# =========================================================
# 11) PARTICIPANT BREAKDOWN
# =========================================================

left, right = st.columns([1, 1])

with left:
    st.subheader("Team Scores")
    st.dataframe(team_scores_df, use_container_width=True, hide_index=True)

with right:
    st.subheader("Played Matches")
    st.dataframe(played_matches_df, use_container_width=True, hide_index=True)
    
st.subheader("Participant Breakdown")
default_index = sorted(participants.keys()).index("Sam") if "Sam" in participants else 0
selected_person = st.selectbox("Select participant", sorted(participants.keys()), index=default_index)
selected_breakdown = person_team_breakdown(selected_person, participants, team_scores)

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
# 10) LEADERBOARD CHART
# =========================================================

#st.subheader("Leaderboard Chart")
#fig, ax = plt.subplots(figsize=(10, 8))
#leaderboard_sorted = leaderboard.sort_values("Points", ascending=True)
#ax.barh(leaderboard_sorted["Name"], leaderboard_sorted["Points"])
#ax.set_xlabel("Points")
#ax.set_ylabel("Person")
#ax.set_title("Sweepstake Leaderboard")
#plt.tight_layout()
#st.pyplot(fig)


