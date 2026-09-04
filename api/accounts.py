from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user, login_user
import requests as http_requests
import re
import json
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from db_manager import *


def register_accounts(app, bcrypt, login_manager):

    @login_manager.user_loader
    def load_user(user_id):
        return None

    @app.route("/")
    def index():
        return redirect(url_for("login"))

    @app.route("/home")
    @login_required
    def home():
        if not current_user.is_confirmed:
            return render_template("not_dostup.html")
        return render_template("home1.html", name=current_user.login)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        return render_template("login.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        return render_template("register.html")
