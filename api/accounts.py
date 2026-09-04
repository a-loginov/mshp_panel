from flask import render_template, redirect, url_for, request, jsonify, session
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
        if request.method == "POST":
            login_val = request.form.get("login", "").strip()
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "")

            errors = {}

            if not login_val:
                errors["login"] = "Введите логин"
            if not email or not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
                errors["email"] = "Введите корректный email"
            if len(password) < 8:
                errors["password"] = "Минимум 8 символов"

            if not errors:
                try:
                    existing = get_user_by_login(login_val)
                    if existing:
                        errors["login"] = "Пользователь с таким логином уже существует"
                except (AttributeError, NameError):
                    pass

            if not errors:
                try:
                    existing = get_user_by_email(email)
                    if existing:
                        errors["email"] = "Пользователь с таким email уже существует"
                except (AttributeError, NameError):
                    pass

            if errors:
                return render_template("register.html", errors=errors, form_data=request.form)

            try:
                hashed = bcrypt.generate_password_hash(password).decode('utf-8')
                create_user(login_val, email, hashed)
            except (AttributeError, NameError):
                pass

            return redirect(url_for("home"))

        return render_template("register.html")
