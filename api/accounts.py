from main import *
from db_manager import *
import requests
import re
import json
from flask import jsonify, render_template, request, redirect
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager, current_user




#Контроль доступа
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'




#-----------------------------------   FRONTEND   -----------------------------------

@app.route("/home")
@login_required
def home():
    if not current_user.is_confirmed: return render_template("not_dostup.html")
    return render_template("home1.html")