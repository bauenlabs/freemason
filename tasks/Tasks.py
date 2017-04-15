from celery import Celery, states, Task, current_task
from flask_socketio import SocketIO
from git import Repo, Git

# Instantiate Celery app
app = Celery('tasks', broker='mongodb://localhost:27017/app', backend="mongodb://localhost:27017/app")

@app.task
def deploy(**kwargs):
  """
  Fuction executed by celery for a deployment
  """
  
  # Import deployments module
  from lib import deployments

  # Append current task ID to kwargs to be passed deployment object
  kwargs['task_id'] = current_task.request.id

  # Instantiate Deployment Object
  d = deployments.Deployment(**kwargs)

  # Execute Deployment.deploy() and return results
  return d.deploy()

