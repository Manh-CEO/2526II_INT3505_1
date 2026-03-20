import os
import sys

# Add the root directory to the python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openapi_server.__main__ import app as connexion_app

# Vercel requires a variable named 'app' containing the WSGI application
app = connexion_app.app
