
import json

#read the json config file

# the file 'complete_config.json' is in the config_files folder
with open('heuristic_examinations/config_files/complete_config.json') as f:
    test_dict = json.load(f)

print(test_dict['config2']['variable_step_size'])
