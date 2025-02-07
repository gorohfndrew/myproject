
"""
WSGI config for myproject project.

This file serves as an entry point for the WSGI server to run your Django project.

For more information on this file, see:
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

# Step 1: Import necessary modules
import os
from django.core.wsgi import get_wsgi_application

# Step 2: Set the default settings module for the 'myproject' project
# This tells Django which settings file to use for the project.
# Make sure the 'myproject.settings' corresponds to the actual path of your settings module.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Step 3: Get the WSGI application for your Django project
# This creates the application object that the WSGI server will use to communicate with Django.
application = get_wsgi_application()

# This variable 'application' will be used by the WSGI server to handle incoming HTTP requests.
# In production, the WSGI server (e.g., Gunicorn or uWSGI) will import and use this file to run the app.