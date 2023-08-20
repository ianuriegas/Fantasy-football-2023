# Importing necessary modules for making HTTP requests, parsing HTML, and handling JSON
import json
import requests
from bs4 import BeautifulSoup
# This is likely a custom module to get a list of players.
from get_my_team import get_players_list

# BASE_URL to which we'll be appending position info to scrape player data.
BASE_URL = "https://fantasyfootballcalculator.com/rankings/"

# List of positions we're interested in.
POSITIONS = [
    "qb", "rb", "wr", "te", "kicker", "defense"
]

# Mapping of default position IDs to their respective names.
POSITION_MAP = {
    1: "qb",
    2: "rb",
    3: "wr",
    4: "te",
    5: "kicker",
    6: "defense"
    # Add more positions and IDs as needed
}


def get_players(position):
    """Fetches players for a given position from the BASE_URL."""
    players = []
    response = requests.get(f"{BASE_URL}{position}")
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', class_='table table-striped mt-3')
    rows = table.find_all('tr')[1:]

    for row in rows:
        columns = row.find_all('td')
        name_link = columns[1].find('a')
        name = name_link.get_text()
        href = name_link['href'].split('/players/')[-1]
        players.append({'name': name, 'href': href})

    return players


def fetch_all_players():
    """Fetches all players for all positions defined in POSITIONS list."""
    return {position: get_players(position) for position in POSITIONS}


def find_team_name_by_mascot(mascot, file_path='data/defenses.json'):
    """Returns the team name by matching its mascot from a predefined JSON file."""
    with open(file_path, 'r') as file:
        teams = json.load(file)
        return next((team['name'] for team in teams if team['mascot'] == mascot), None)


def find_default_position_id_by_name(full_name, json_file_path='data/all_players.json'):
    """Fetches default position ID for a given player from a predefined JSON file."""
    with open(json_file_path) as json_file:
        players = json.load(json_file)
        return next((player.get("defaultPositionId") for player in players if player.get("fullName") == full_name), None)


def find_position(default_position_id):
    """Fetches the player position name using the default position ID."""
    return POSITION_MAP.get(default_position_id, "unknown")


def find_matching_player(player_name, all_players):
    """Searches for a player in the fetched players and returns its position and details if found."""
    for position, players in all_players.items():
        matching_player = next(
            (player for player in players if player["name"] == player_name), None)
        if matching_player:
            return position, matching_player
    return None, None


# Fetch all players from the website.
all_players = fetch_all_players()
# Get the players list, likely from a local database or another source.
players_list = get_players_list()

# For each player in our list, we're trying to find more information from the fetched data.
for player_info in players_list:
    player_name = player_info["name"]
    position, matching_player = find_matching_player(player_name, all_players)

    if position:
        player_info["href"] = matching_player["href"]
        player_info["position"] = position
    elif " D/ST" in player_name:
        team_name = find_team_name_by_mascot(player_name)
        defense_href = team_name.replace(" ", "-").replace(".", "").lower()
        player_info["href"] = defense_href
        player_info["position"] = "defense"
        print(defense_href)
    else:
        default_position_id = find_default_position_id_by_name(player_name)
        position_id = find_position(default_position_id)
        unknown_player_href = player_name.replace(
            " ", "-").replace(".", "").lower()
        player_info["href"] = unknown_player_href
        player_info["position"] = position_id
        print(unknown_player_href)

# After processing, we're printing a formatted JSON output of our players list.
formatted_player_list = json.dumps(players_list, indent=4)
print(formatted_player_list)
