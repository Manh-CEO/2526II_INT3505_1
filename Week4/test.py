from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from pathlib import Path
import sys

print(Path(__file__).parent)