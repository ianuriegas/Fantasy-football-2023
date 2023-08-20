import json

def find_default_position_id_by_name(full_name, json_file_path):
    with open(json_file_path) as json_file:
        data = json.load(json_file)

    for person in data:
        if person.get("fullName") == full_name:
            default_position_id = person.get("defaultPositionId")
            return default_position_id

    return None  # If the person is not found

# Replace '../data/all_players.json' with the actual path to your JSON file
json_file_path = '../data/all_players.json'
full_name_to_search = "A.J. Brown"

default_position_id = find_default_position_id_by_name(full_name_to_search, json_file_path)
if default_position_id is not None:
    print(f"{full_name_to_search}'s defaultPositionId:", default_position_id)
else:
    print(f"{full_name_to_search} not found in the JSON.")
