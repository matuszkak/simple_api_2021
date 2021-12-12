import json
import pickle
from os import path


def transform_json_to_pickle():
  current_path = path.dirname(__file__)
  # open JSON file

  file_name = 'projects.json'

  f = open(path.join(current_path, file_name), 'r')

  # returns JSON object as a dictionary
  data = json.load(f)['projects']

  # dump into pickle
  with open(path.join(current_path, 'projects.pickle'), 'wb') as file:
    pickle.dump(data, file)

  # close file
  f.close()
