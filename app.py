from flask import Flask, render_template, request
from flask.json import jsonify
import pickle
from os import path
from create_pickle import save_data
import uuid


# function to filter dictionary based on list of fields
def filter_list_of_dicts(list_of_dicts, fields):
  filtered_dicts = []
  for x in list_of_dicts:

    x_copy = x.copy()

    for elem in x:
      if elem not in fields:
        dict(filter(lambda x: x[0] != elem, x_copy.items()))
        x_copy.pop(elem)

    filtered_dicts.append(x_copy)

  return filtered_dicts


app = Flask(__name__)

# transform project list from json to pickle - needed only at initializetion when no project.pickle file. Or can run create.pickle.py separately to create first project.pickle file from the project.json input file
# transform_json_to_pickle()

# load project list from pickle
current_path = path.dirname(__file__)
with open(path.join(current_path, 'projects.pickle'), 'rb') as file:
  projects = pickle.load(file)

# define resources...


# home page from template
@app.route('/')
def home():
  name = "Kristof"
  return render_template('index.html', user_name=name)


# get list of projects, with specific fields
@app.route('/project')
def get_projects():
  try:
    request_data = request.get_json()
    fields = request_data['fields']
    # print(fields)
    # print(projects)
    return jsonify({'projects': filter_list_of_dicts(projects, fields)})
  except:
    return jsonify({'projects': projects})


# get project details by project_id
@app.route('/project/<string:project_id>')
def get_project(project_id):
  for project in projects:
    if project['project_id'] == project_id:
      return jsonify(project)
  return jsonify({'message': 'project such id does not exists'})


# get project tasks, with specific fields
@app.route('/project/<string:project_id>/task')
def get_all_tasks_in_project(project_id):

  for project in projects:
    if project['project_id'] == project_id:

      try:
        request_data = request.get_json()
        tfields = request_data['fields']
        tasks = {}
        # print(tfields)
        tasks = project['tasks']
        # print(tasks)
        return jsonify({'tasks': filter_list_of_dicts(tasks, tfields)})

      except:
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

  # id creation for project
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


# add task to project
@app.route('/project/<string:project_id>/task', methods=['POST'])
def add_task_to_project(project_id):
  request_data = request.get_json()
  for project in projects:
    if project['project_id'] == project_id:
      new_task = {
          'name': request_data['name'],
          "task_id": "",
          'completed': request_data['completed'],
          'checklist': request_data['checklist']
      }

      # task id creation
      new_task_id = uuid.uuid4().hex[:24]
      new_task['task_id'] = new_task_id

      # add task to task list
      project['tasks'].append(new_task)

      # save project data in pickle file
      save_data(projects)
      return jsonify({'message': f'task created with id: {new_task_id}'})

  return jsonify({'message': 'project not found'})


# set project complete
@app.route('/project/<string:project_id>/complete', methods=['POST'])
def set_project_to_complete(project_id):
  for project in projects:
    print(project_id, project['project_id'])
    if project['project_id'] == project_id:
      if project['completed'] == "true":
        return {'message': f'project already completed'}, 200
      else:
        project['completed'] = "true"
        return jsonify(project)
  return {'message': f'no project exists with such id'}, 404


# run app on all ports
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)