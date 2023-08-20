import json
import requests
from bs4 import BeautifulSoup
from get_team import get_players_list


def get_players(url):
    position_list = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', class_='table table-striped mt-3')
    rows = table.find_all('tr')[1:]

    for row in rows:
        columns = row.find_all('td')
        name_link = columns[1].find('a')
        name = name_link.get_text()
        href = name_link['href'].split('/players/')[-1]

        player_info = {
            'name': name,
            'href': href
        }

        position_list.append(player_info)

    return position_list


qb = get_players("https://fantasyfootballcalculator.com/rankings/qb")
rb = get_players("https://fantasyfootballcalculator.com/rankings/rb")
wr = get_players("https://fantasyfootballcalculator.com/rankings/wr")
te = get_players("https://fantasyfootballcalculator.com/rankings/te")
kicker = get_players("https://fantasyfootballcalculator.com/rankings/kicker")
defense = get_players("https://fantasyfootballcalculator.com/rankings/defense")

# print(json.dumps(qb, indent=4))
# print(json.dumps(rb, indent=4))
# print(json.dumps(wr, indent=4))
# print(json.dumps(te, indent=4))
# print(json.dumps(kicker, indent=4))
# print(json.dumps(defense, indent=4))

# ==============================================
# We can use this as a universal function later
# ==============================================
players_list = get_players_list()
for player_info in players_list:
    player_name = player_info["name"]

    matching_wr_players = [wr_player for wr_player in wr if wr_player["name"] == player_name]

    if matching_wr_players:
        for matching_wr_player in matching_wr_players:
            wr_player_href = matching_wr_player["href"]
            player_info["href"] = wr_player_href


formatted_player_list = json.dumps(players_list, indent=4)
print(formatted_player_list)
