def find_path_by_key(data, target_key, current_path=None):
    if current_path is None:
        current_path = []

    if isinstance(data, dict):
        for key, value in data.items():
            new_path = current_path + [key]
            if key == target_key:
                return new_path
            result = find_path_by_key(value, target_key, new_path)
            if result:
                return result
    elif isinstance(data, list):
        for index, item in enumerate(data):
            new_path = current_path + [index]
            result = find_path_by_key(item, target_key, new_path)
            if result:
                return result

    return None


import requests
import json

url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2023/segments/0/leagues/1923771045?rosterForTeamId=6&view=mDraftDetail&view=mLiveScoring&view=mMatchupScore&view=mPendingTransactions&view=mPositionalRatings&view=mRoster&view=mSettings&view=mTeam&view=modular&view=mNav"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    target_key = "fullName"
    key_path = find_path_by_key(data, target_key)

    if key_path:
        print(f"Key '{target_key}' found at path: {' -> '.join(map(str, key_path))}")
        target_value = data
        for key in key_path:
            target_value = target_value[key]

        pretty_json = json.dumps(target_value, indent=4)
        print(pretty_json)
    else:
        print(f"Key '{target_key}' not found in the JSON data.")
else:
    print("Failed to fetch data from the URL")
