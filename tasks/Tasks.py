from celery import Celery, states, Task, current_task
from flask_socketio import SocketIO
#define celery app
app = Celery('tasks', broker='mongodb://localhost:27017/app', backend="mongodb://localhost:27017/app")

@app.task
def deployment():
    import time
    for x in xrange(10):
      time.sleep(2)
      currentID = current_task.request.id
      socketio = SocketIO(message_queue="redis://")
      percent = (x + 1) * 10
      string = "{0}%".format(percent)
      socketio.emit('deployment_event', {"data": currentID, "room": currentID, "percent": string }, room=currentID, namespace='/deployments') 
    return "progessiveTaskExample is done"
