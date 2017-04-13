"""
This File contains the basic configuration and funtionality changes made
to the eve.py app that power CRUD operations
"""

from eve import Eve
from tasks import Tasks


def deployment_insert_callback(documents):
  """
  Function to queue deployments when they are created in the API
  """
  # deployment arguments
  args = documents[0]['args']

  # Execute the deployment with the arguments
  deploymentResult = Tasks.deployment.apply_async(*args)

  # Update document with deployment ids
  documents[0]['_id'] = deploymentResult.id

def deployment_fetch_callback(response):
  """
  CallBack function join in data from celery when its looked up
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
