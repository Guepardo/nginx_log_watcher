from flask import Flask, request, jsonify

app = Flask(__name__)

from routes import ingest_controller