import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("⚽ World Cup Sweepstake Dashboard")

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
    "Balas": ["Austria", "Turkey", "Qatar", "Algeria", "Switzerland"]
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
# 4) PREVIOUS SNAPSHOT FOR "BIGGEST MOVERS"
#    Update this manually when you want a new baseline.
#    Example: yesterday's points by person
# =========================================================

previous_points = {
    "Audrey": 3,
    "Esperanza": 3,
    "Anna": 0,
    "Becky": 1,
    "Anne-Sophie": 0,
    "Sophie": 1,
    "Anil": 0,
    "Enrique": 0,
    "Sam": 3,
    "Chris": 0,
    "Akhil": 1,
    "Scott": 0,
    "Sonam": 1,
    "Zoey": 0,
    "Pavan": 0,
    "Spyros": 3,
    "Rajiv": 3,
    "Kash": 0,
    "Salima": 0,
    "Balas": 1
}

# =========================================================
# 5) FIXTURES
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
    {"date": "2026-06-13", "stage": "Group", "group": "B", "home": "Qatar", "away": "Switzerland", "home_goals": None, "away_goals": None},
    {"date": "2026-06-13", "stage": "Group", "group": "C", "home": "Brazil", "away": "Morocco", "home_goals": None, "away_goals": None},

    # Sun 14 Jun
    {"date": "2026-06-14", "stage": "Group", "group": "C", "home": "Haiti", "away": "Scotland", "home_goals": None, "away_goals": None},
    {"date": "2026-06-14", "stage": "Group", "group": "D", "home": "Australia", "away": "Türkiye", "home_goals": None, "away_goals": None},
    {"date": "2026-06-14", "stage": "Group", "group": "E", "home": "Germany", "away": "Curaçao", "home_goals": None, "away_goals": None},
    {"date": "2026-06-14", "stage": "Group", "group": "F", "home": "Netherlands", "away": "Japan", "home_goals": None, "away_goals": None},
    {"date": "2026-06-14", "stage": "Group", "group": "E", "home": "Côte d'Ivoire", "away": "Ecuador", "home_goals": None, "away_goals": None},

    # Mon 15 Jun
    {"date": "2026-06-15", "stage": "Group", "group": "F", "home": "Sweden", "away": "Tunisia", "home_goals": None, "away_goals": None},
    {"date": "2026-06-15", "stage": "Group", "group": "H", "home": "Spain", "away": "Cabo Verde", "home_goals": None, "away_goals": None},
    {"date": "2026-06-15", "stage": "Group", "group": "G", "home": "Belgium", "away": "Egypt", "home_goals": None, "away_goals": None},
    {"date": "2026-06-15", "stage": "Group", "group": "H", "home": "Saudi Arabia", "away": "Uruguay", "home_goals": None, "away_goals": None},

    # Tue 16 Jun
    {"date": "2026-06-16", "stage": "Group", "group": "G", "home": "IR Iran", "away": "New Zealand", "home_goals": None, "away_goals": None},
    {"date": "2026-06-16", "stage": "Group", "group": "I", "home": "France", "away": "Senegal", "home_goals": None, "away_goals": None},
    {"date": "2026-06-16", "stage": "Group", "group": "I", "home": "Iraq", "away": "Norway", "home_goals": None, "away_goals": None},

    # Wed 17 Jun
    {"date": "2026-06-17", "stage": "Group", "group": "J", "home": "Argentina", "away": "Algeria", "home_goals": None, "away_goals": None},
    {"date": "2026-06-17", "stage": "Group", "group": "J", "home": "Austria", "away": "Jordan", "home_goals": None, "away_goals": None},
    {"date": "2026-06-17", "stage": "Group", "group": "K", "home": "Portugal", "away": "Congo DR", "home_goals": None, "away_goals": None},
    {"date": "2026-06-17", "stage": "Group", "group": "L", "home": "England", "away": "Croatia", "home_goals": None, "away_goals": None},
    {"date": "2026-06-17", "stage": "Group", "group": "L", "home": "Ghana", "away": "Panama", "home_goals": None, "away_goals": None},
]

# =========================================================
# 6) SCORING ENGINE
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
# 7) TABLE BUILDERS
# =========================================================

def build_leaderboard(participants, team_scores, previous_points):
    rows = []
    for person, teams in participants.items():
        current_points = sum(team_scores.get(team, 0) for team in teams)
        previous = previous_points.get(person, 0)
        delta = current_points - previous

        rows.append({
            "Name": person,
            "Points": current_points,
            "Delta": delta,
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
    return pd.DataFrame(rows).sort_values(["Date", "Stage"]).reset_index(drop=True)

def person_team_breakdown(person, participants, team_scores):
    rows = []
    for team in participants[person]:
        rows.append({
            "Team": team,
            "Points": team_scores.get(team, 0)
        })
    return pd.DataFrame(rows).sort_values(["Points", "Team"], ascending=[False, True]).reset_index(drop=True)

# =========================================================
# 8) BUILD DATA
# =========================================================

team_scores = calculate_team_scores(fixtures)
leaderboard = build_leaderboard(participants, team_scores, previous_points)
team_scores_df = build_team_scores(team_scores)
played_matches_df = build_played_matches(fixtures)

# =========================================================
# 9) TOP HIGHLIGHTS
# =========================================================

leader_name = leaderboard.iloc[0]["Name"] if not leaderboard.empty else "—"
leader_points = int(leaderboard.iloc[0]["Points"]) if not leaderboard.empty else 0

biggest_riser_row = leaderboard.sort_values(["Delta", "Points"], ascending=[False, False]).iloc[0] if not leaderboard.empty else None
biggest_faller_row = leaderboard.sort_values(["Delta", "Points"], ascending=[True, False]).iloc[0] if not leaderboard.empty else None

biggest_riser_name = biggest_riser_row["Name"] if biggest_riser_row is not None else "—"
biggest_riser_delta = int(biggest_riser_row["Delta"]) if biggest_riser_row is not None else 0

biggest_faller_name = biggest_faller_row["Name"] if biggest_faller_row is not None else "—"
biggest_faller_delta = int(biggest_faller_row["Delta"]) if biggest_faller_row is not None else 0

m1, m2, m3 = st.columns(3)
m1.metric("🥇 Current Leader", leader_name, leader_points)
m2.metric("📈 Biggest Riser", biggest_riser_name, biggest_riser_delta)
m3.metric("📉 Biggest Faller", biggest_faller_name, biggest_faller_delta)

# =========================================================
# 10) LEADERBOARD TABLE WITH HIGHLIGHTS
# =========================================================

st.subheader("Leaderboard")

def highlight_leaderboard(row):
    rank = row.name
    if rank == 1:
        return ["background-color: #FFD700; color: black; font-weight: bold;"] * len(row)   # Gold
    elif rank == 2:
        return ["background-color: #C0C0C0; color: black; font-weight: bold;"] * len(row)   # Silver
    elif rank == 3:
        return ["background-color: #CD7F32; color: white; font-weight: bold;"] * len(row)   # Bronze
    return [""] * len(row)

styled_leaderboard = leaderboard.style.apply(highlight_leaderboard, axis=1).format({"Delta": "{:+d}"})
st.dataframe(styled_leaderboard, use_container_width=True)

left, right = st.columns([1, 1])

with left:
    st.subheader("Team Scores")
    st.dataframe(team_scores_df, use_container_width=True)

with right:
    st.subheader("Played Matches")
    st.dataframe(played_matches_df, use_container_width=True)

# =========================================================
# 11) LEADERBOARD CHART
# =========================================================

st.subheader("Leaderboard Chart")
fig, ax = plt.subplots(figsize=(10, 8))
leaderboard_sorted = leaderboard.sort_values("Points", ascending=True)
ax.barh(leaderboard_sorted["Name"], leaderboard_sorted["Points"])
ax.set_xlabel("Points")
ax.set_ylabel("Person")
ax.set_title("Sweepstake Leaderboard")
plt.tight_layout()
st.pyplot(fig)

# =========================================================
# 12) PARTICIPANT BREAKDOWN
# =========================================================

st.subheader("Participant Breakdown")
default_index = sorted(participants.keys()).index("Sam") if "Sam" in participants else 0
selected_person = st.selectbox("Select participant", sorted(participants.keys()), index=default_index)
selected_breakdown = person_team_breakdown(selected_person, participants, team_scores)

left2, right2 = st.columns([1, 1])

with left2:
    st.markdown(f"### {selected_person}'s teams")
    st.dataframe(selected_breakdown, use_container_width=True)

with right2:
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    breakdown_sorted = selected_breakdown.sort_values("Points", ascending=True)
    ax2.barh(breakdown_sorted["Team"], breakdown_sorted["Points"])
    ax2.set_xlabel("Points")
    ax2.set_ylabel("Team")
    ax2.set_title(f"{selected_person} - Team Contribution")
    plt.tight_layout()
    st.pyplot(fig2)
