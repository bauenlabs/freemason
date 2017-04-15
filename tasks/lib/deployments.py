from git import Git, Repo
from flask_socketio import SocketIO

class Deployment(object):
  """
  This Class represents a Deployment object, and contains the attributes and 
  methods needed for sucessfully executing a deployment
  """
  def __init__(self, **kwargs):
    """
    The Initialization Function
    """
    print
    self.repository = kwargs['repository']
    self.path = kwargs['path']
    self.branch = kwargs['branch']
    self.app_name = kwargs['app_name']
    self.tag = "{0}:{1}".format(self.app_name, self.branch)
    self.task_id = kwargs['task_id']
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
  def deploy(self):
    """
    This function is what is envoked by celery itself when a deployment task is
    executed.
    """
    import time
    for x in xrange(10):
      time.sleep(2)
      currentID = self.task_id
      socketio = SocketIO(message_queue="redis://")
      percent = (x + 1) * 10
      string = "{0}%".format(percent)
      socketio.emit('deployment_event', {"data": currentID, "room": currentID, "percent": string }, room=currentID, namespace='/deployments') 
    return "progessiveTaskExample is done"
