from flask import Flask, render_template, request
from flask.json import jsonify
import pickle
from os import path
from create_pickle import save_data
import uuid

app = Flask(__name__)

# transform project list from json to pickle
# transform_json_to_pickle()

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


# get project details by project_id
@app.route('/project/<string:project_id>')
def get_project(project_id):
  for project in projects:
    if project['project_id'] == project_id:
      return jsonify(project)
  return jsonify({'message': 'project such id does not exists'})


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
  new_project = {
      'name': request_data['name'],
      "creation_date": request_data['creation_date'],
      "project_id": "",
      "completed": request_data['completed'],
      'tasks': request_data['tasks']
  }

  # id creation
  new_project_id = uuid.uuid4().hex[:24]
  new_project_name = new_project['name']
  new_project['project_id'] = new_project_id

  # add project to list and save list in pickle file
  projects.append(new_project)

  save_data(projects)
  return jsonify({
      'message':
      f'project {new_project_name} created with id: {new_project_id}'
  })


# add task to a project
@app.route('/project/<string:name>/task', methods=['POST'])
def add_task_to_project(name):
  request_data = request.get_json()
  for project in projects:
    if project['name'] == name:
      new_task = {
          'name': request_data['name'],
          'task_id': request_data['task_id'],
          'completed': request_data['completed'],
          'checklist': request_data['check list']
      }
      project['tasks'].append(new_task)
      return jsonify(new_task)
  return jsonify({'message': 'project not found'})


# run app on all ports
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)