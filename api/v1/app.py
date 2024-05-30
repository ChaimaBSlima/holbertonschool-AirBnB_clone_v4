#!/usr/bin/python3
"""
Importing necessary libraries and modules
and creating the Flask web application
"""
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
import os
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close(exception):
    """Teardown function to close the storage
    after the application context is destroyed"""
    storage.close()


@app.errorhandler(404)
def error404(error):
    """This code defines a 404 error handler for a Flask application."""
    errorjson = {"error": "Not found"}
    return jsonify(errorjson), 404


if __name__ == "__main__":
    port = int(os.environ.get("HBNB_API_PORT", 5000))
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    app.run(host=host, port=port, threaded=True)
