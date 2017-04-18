from git import Git, Repo
from flask_socketio import SocketIO
import time
class Deployment(object):
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
    self.app_name = kwargs['app_name']
    self.tag = "{0}:{1}".format(self.app_name, self.branch)
    self.task_id = kwargs['task_id']
    self.socketio = SocketIO(message_queue="redis://")
  def cloneRepo(self):
    """
    This function clones a repository, pulls the needed branch then sets that as 
    the HEAD in the repo
    """
    try:
      # Use the Git binary to clone the repo at the set temp path
      Git().clone(self.repository.encode('utf-8'), self.path.encode('utf-8'))
      # Emit sucessful clone event
      self.socketio.emit('deployment_event', {"data": "Repo Cloned", 
        "room": self.task_id, "progress_percent": "25%" }, 
        room=self.task_id, namespace='/deployments'
      )
    except Exception as e:
      # Emit failure event
      self.socketio.emit('deployment_event', {"data": "failed to clone repo: {0}".format(e), 
        "room": self.task_id, "progress_percent": "0%" }, 
        room=self.task_id, namespace='/deployments'
      )
      # Return Failure message and exception
      return "failed to clone repo"
    try:
      # Instantiate a Repo object for the newly cloned repo
      r = Repo(self.path.encode('utf-8'))
      # Emit sucessful instantiation event
      self.socketio.emit('deployment_event', {"data": "Repo Instantiation complete", 
        "room": self.task_id, "progress_percent": "50%" }, 
        room=self.task_id, namespace='/deployments'
      )
    except Exception as e:
      # Emit failure event
      self.socketio.emit('deployment_event', {"data": "failed to instatiate repo: {0}".format(e), 
        "room": self.task_id, "progress_percent": "0%" }, 
        room=self.task_id, namespace='/deployments'
      )
      # Return Failure message and exception
      return "failed to instantiate repo"
    try: 
      # Ensure that the cloned repo is up-to-date
      r.remotes.origin.pull()
      # Emit sucessful pull  event
      self.socketio.emit('deployment_event', {"data": "Repo is up to date with origin", 
        "room": self.task_id, "progress_percent": "75%" }, 
        room=self.task_id, namespace='/deployments'
      )
    except Exception as e:
      # Emit failure event
      self.socketio.emit('deployment_event', {"data": "failed to pull remote origin: {0}".format(e), 
        "room": self.task_id, "progress_percent": "0%" }, 
        room=self.task_id, namespace='/deployments'
      )
      # Return Failure message and exception
      return "failed to bring repo up to date"
    try:
      # Checkout the correct branch
      r.create_head(self.branch.encode('utf-8'), 'HEAD')
      r.heads[0].checkout()
      # Emit sucessful pull  event
      self.socketio.emit('deployment_event', {"data": "Sucessfully checkedout {0}".format(self.branch),
        "room": self.task_id, "progress_percent": "100%" }, 
        room=self.task_id, namespace='/deployments'
      )
    except Exception as e:
      # Emit failure event
      self.socketio.emit('deployment_event', {"data": "failed to checkout {1}: {0}".format(e,self.branch), 
        "room": self.task_id, "progress_percent": "0%" }, 
        room=self.task_id, namespace='/deployments'
      )
      # Return Failure message and exception
      return "failed to checkout {0}".format(self.branch)

  def emitEvent(self, data, errors, meta):
    meta['timestampe'] = time.time()
    self.socketio.emit('deployment_event', 
        {"data": data, "errors": errors, "meta": meta},
         room=self.task_id, namespace='/deployments'
    )

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
    #test = self.cloneRepo()
    data = {"msg": "this is a deployment event"}
    errors = "no error"
    meta = {"task_id": "someid"}
    self.emitEvent(data, errors, meta)
    return "lol"
