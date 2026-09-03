import config
from flask import Flask, render_template, url_for 
from flask_login import login_required, login_manager
from datetime import datetime, timedelta


app = Flask(__name__)
app.config.update(SECRET_KEY=config.SECRET_KEY)
app.permanent_session_lifetime = timedelta(days=365)


from api import accounts
from api import exit_system






if __name__ == "__main__":
    app.run(debug=True, port=4323)