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

def find_team_name_by_mascot(mascot):
    with open('data/defenses.json', 'r') as file:
        data = json.load(file)
        
        for team in data:
            if team['mascot'] == mascot:
                return team['name']
    return None

# ==============================================
# We can use this as a universal function later
# ==============================================
players_list = get_players_list()
for player_info in players_list:
    player_name = player_info["name"]

    matching_qb_players = [
        qb_player for qb_player in qb if qb_player["name"] == player_name]
    matching_rb_players = [
        rb_player for rb_player in rb if rb_player["name"] == player_name]
    matching_wr_players = [
        wr_player for wr_player in wr if wr_player["name"] == player_name]
    matching_te_players = [
        te_player for te_player in te if te_player["name"] == player_name]
    matching_kicker_players = [
        kicker_player for kicker_player in kicker if kicker_player["name"] == player_name]
    matching_defense_players = [
        defense_player for defense_player in defense if defense_player["name"] == player_name]

    if matching_qb_players:
        for matching_qb_player in matching_qb_players:
            qb_player_href = matching_qb_player["href"]
            print(qb_player_href)
            player_info["href"] = qb_player_href
            player_info["position"] = "qb"

    elif matching_rb_players:
        for matching_rb_player in matching_rb_players:
            rb_player_href = matching_rb_player["href"]
            print(rb_player_href)
            player_info["href"] = rb_player_href
            player_info["position"] = "rb"

    elif matching_wr_players:
        for matching_wr_player in matching_wr_players:
            wr_player_href = matching_wr_player["href"]
            print(wr_player_href)
            player_info["href"] = wr_player_href
            player_info["position"] = "wr"

    elif matching_te_players:
        for matching_te_player in matching_te_players:
            te_player_href = matching_te_player["href"]
            print(te_player_href)
            player_info["href"] = te_player_href
            player_info["position"] = "te"

    elif matching_kicker_players:
        for matching_kicker_player in matching_kicker_players:
            kicker_player_href = matching_kicker_player["href"]
            print(kicker_player_href)
            player_info["href"] = kicker_player_href
            player_info["position"] = "k"

    elif " D/ST" in player_name:
        # We want to map existing defenses to a json with their city name since we need that format EX(New Orleans Defense)
        # something like this format { Saints: New Orleans Defense }
        # I have a json and will put it into "data" folder
        # we potentially want to change player_info["fullName"] with the "City + Defense"
        team_name = find_team_name_by_mascot(player_name)
        defense_href = team_name.replace(" ", "-").replace(".", "").lower()
        player_info["href"] = defense_href
        player_info["position"] = "defense"
        print(defense_href)

    else:
        # PROBLEM: some players are not in the list from ffbc.com
        # search for their name and position in some sort of other website
        # format their name to ex: (gabe-davis) | hoping this works (fingers crossed)

        print(player_name)

formatted_player_list = json.dumps(players_list, indent=4)
print(formatted_player_list)
