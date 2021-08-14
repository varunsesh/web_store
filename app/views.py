from flask import Blueprint, json, request, jsonify, redirect
from flask_session import Session
from flask.helpers import url_for
from app.auth import session

views = Blueprint("views", __name__)


@views.route("/", methods=["GET"])
def index():
    return f"<h1>Welcome to the Web Store. Please Login."



