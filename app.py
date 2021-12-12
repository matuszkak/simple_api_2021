from flask import Flask, render_template, request
from flask.json import jsonify
import pickle
from os import path
from create_pickle import transform_json_to_pickle

app = Flask(__name__)

# transform project list from json to pickle
transform_json_to_pickle()

# load project list from pickle
current_path = path.dirname(__file__)

with open(path.join(current_path, 'projects.pickle'), 'rb') as file:
  projects = pickle.load(file)


# define resources
# home page from template
@app.route('/')
def home():
  name = "Kristof"
  return render_template('index.html', user_name=name)


# get list of projects
@app.route('/project')
def get_projects():
  return jsonify({'projects': projects})


# get project details by project name
@app.route('/project/<string:name>')
def get_project(name):
  for project in projects:
    if project['name'] == name:
      return jsonify(project)
  return jsonify({'message': 'project not found'})


# get project tasks by project name
@app.route('/project/<string:name>/task')
def get_all_tasks_in_project(name):
  for project in projects:
    if project['name'] == name:
      return jsonify({'tasks': project['tasks']})
  return jsonify({'message': 'project not found'})


# create project
@app.route('/project', methods=['POST'])
def create_project():
  # lekérdezzük a http request body-ból a JSON adatot:
  request_data = request.get_json()
  new_project = {'name': request_data['name'], 'tasks': request_data['tasks']}
  projects.append(new_project)
  return jsonify(new_project)


# add task to a project
@app.route('/project/<string:name>/task', methods=['POST'])
def add_task_to_project(name):
  request_data = request.get_json()
  for project in projects:
    if project['name'] == name:
      new_task = {
          'name': request_data['name'],
          'completed': request_data['completed']
      }
      project['tasks'].append(new_task)
      return jsonify(new_task)
  return jsonify({'message': 'project not found'})


# run app on all ports
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)