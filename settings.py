"""
This file contains detailed configuration of the eve.py app that powers
CRUD operations
"""

# Global Config
XML = False
DEBUG = True
X_DOMAINS = ["http://127.0.0.1:5000"]
X_HEADERS = ["Origin", "X-Requested-With", "Content-Type", "Accept", "Authorization", "If-Match"]

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH), replacements (PUT) and deletes of
# individual items
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

# Database Settings
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DBNAME = 'app'


# Deployment Schema Definition
DeploymentSchema = {
    '_id': {
        'type': 'string'
    },
    'repository': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 100,
        'required': True
    },
    'path': {
      'type': 'string'
    },
    'status': {
      'type': 'string'
    },
    'branch': {
      'type': 'string'
    },
    'app': {
      'type': 'string'
    }
}

# Dictionary containing configuration information for the deployments endpoint
deployments  = {
    'item_title': 'deployment',
    'item_url': 'regex("[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}")',
  
    # We choose to override global cache-control directives for this resource.
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,
  
    # Most global settings can be overridden at resource level
    'resource_methods': ['POST' ],
    'item_methods': ['GET', 'PATCH'],
    'schema': DeploymentSchema
}

# The main config for the global DOMAIN dictionary 
DOMAIN = {'deployments': deployments}
