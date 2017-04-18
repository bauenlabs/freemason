"""
This File contains the basic configuration and funtionality
of the eve.py app that powers CRUD operations
"""

from eve import Eve
from tasks import Tasks


def deployment_insert_callback(documents):
  """
  Function to queue deployments when they are created in the API
  """
  # Pull arguemnts for deployment task from the document
  kwargs = {
    "repository": documents[0]['repository'],
    "path": documents[0]['path'],
    "branch": documents[0]['branch'],
    "app_name": documents[0]['app_name'],
  }
   
  # Register deployment task
  deploymentResult = Tasks.deploy.delay(**kwargs)

  # Update document with deployment ids
  documents[0]['_id'] = deploymentResult.id

def deployment_fetch_callback(response):
  """
  CallBback function to join in data from celery when a deployment is 
  looked up
  """
  # Instantiate Task object from celery
  deployment = Tasks.app.AsyncResult(response['_id'])

  # Lookup Deployments current status in celery
  response['status'] = deployment.status

  # Build the results attribute in the response
  response['result'] = {
      "output" : deployment.result,
      "error" : deployment.traceback
  }

"""
Define and configure App
"""

#Define app
app = Eve()

# Add the callbacks to on_insert and on_fetched
app.on_insert_deployments += deployment_insert_callback
app.on_fetched_item_deployments += deployment_fetch_callback

"""
Start App
"""
if __name__ == '__main__':
  app.run(port=8080)
