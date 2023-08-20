import requests

"""
Gets players from my team and puts them into a list
"""

def get_players_list():
    url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2023/segments/0/leagues/1923771045?rosterForTeamId=6&view=mDraftDetail&view=mLiveScoring&view=mMatchupScore&view=mPendingTransactions&view=mPositionalRatings&view=mRoster&view=mSettings&view=mTeam&view=modular&view=mNav"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        entries = data["schedule"][0]["away"]["rosterForCurrentScoringPeriod"]["entries"]

        player_list = []

        for entry in entries:
            player_info = {
                "name": entry["playerPoolEntry"]["player"]["fullName"],
                "id": entry["playerPoolEntry"]["player"]["id"]
            }
            player_list.append(player_info)

        return player_list

    else:
        print("Failed to fetch data from the URL")
        return []


if __name__ == "__main__":
    players_list = get_players_list()
    for player in players_list:
        print(player)
