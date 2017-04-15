from celery import Celery, states, Task, current_task
from flask_socketio import SocketIO
from git import Repo, Git

# Instantiate Celery app
app = Celery('tasks', broker='mongodb://localhost:27017/app', backend="mongodb://localhost:27017/app")

class Deployment(app.Task):
  """
  This Class represents a Deployment object, and contains the attributes and 
  methods needed for sucessfully executing a deployment
  """
  def __init__(self, **kwargs):
    """
    The Initialization Function
    """
    self.repository = kwargs['repository']
    self.path = kwargs['path']
    self.branch = kwargs['branch']
    self.app_name = kwargs['name']
    self.tag = "{0}:{1}".format(self.name, self.branch)
    self.socketio = SocketIO(message_queue="redis://")
  def cloneRepo(self):
    """
    This function clones a repository, pulls the needed branch then sets that as 
    the HEAD in the repo
    """
    # Use the Git binary to clone the repo at the set temp path
    Git().clone(self.repository, self.path)
  
    # Instantiate a Repo objet for the newly cloned repo
    r = Repo(self.path)
    
    # Ensure that the cloned repo is up-to-date
    r.remotes.origin.pull()
  
    # Checkout the correct branch
    r.create_head(self.branch, 'HEAD')
    r.heads[0].checkout()
  def buildImage(self):
    """
    This function builds a docker image based on the Dockerfile in the directory 
    defined in the `path` attribute
    """
    # Instantial a docker client
    client = docker.from_env()

    # Build an image with the correct tag
    client.images.build(path=self.path, tag=self.tag)
  def run(self, source):
    """
    This function is what is envoked by celery itself when a deployment task is
    executed.
    """
    self.source = source
    import time
    for x in xrange(10):
      time.sleep(2)
      currentID = current_task.request.id
      socketio = SocketIO(message_queue="redis://")
      percent = (x + 1) * 10
      string = "{0}%".format(percent)
      socketioemit('deployment_event', {"data": currentID, "room": currentID, "percent": string }, room=currentID, namespace='/deployments') 
    return "progessiveTaskExample is done"


