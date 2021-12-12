import json
import pickle
from os import path

current_path = path.dirname(__file__)


def transform_json_to_pickle():

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


# save data to pickle
def save_data(list):

  with open(path.join(current_path, 'projects.pickle'), 'wb') as file:
    pickle.dump(list, file)