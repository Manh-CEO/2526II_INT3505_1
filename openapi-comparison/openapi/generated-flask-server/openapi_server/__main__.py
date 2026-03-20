#!/usr/bin/env python3

import os
import connexion

from openapi_server import encoder

# Use absolute path for specification_dir to avoid issues when running on Vercel
spec_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'openapi')
app = connexion.App(__name__, specification_dir=spec_dir)
app.app.json_encoder = encoder.JSONEncoder
app.add_api('openapi.yaml',
            arguments={'title': 'Library Management API'},
            pythonic_params=True)

def main():
    app.run(port=8080)

if __name__ == '__main__':
    main()
