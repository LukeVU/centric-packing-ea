
import json

#read the json config file

# the file 'complete_config.json' is in the config_files folder
with open('heuristic_examinations/config_files/complete_config.json') as f:
    test_dict = json.load(f)

for key in test_dict:
    print(key)
    print(test_dict[key])
