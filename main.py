import config
from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from datetime import timedelta


app = Flask(__name__)
app.config.update(SECRET_KEY=config.SECRET_KEY)
app.permanent_session_lifetime = timedelta(days=365)

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


from api.accounts import register_accounts
from api.exit_system import register_exit_system

register_accounts(app, bcrypt, login_manager)
register_exit_system(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403


@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500


@app.errorhandler(503)
def service_unavailable(e):
    return render_template("503.html"), 503


if __name__ == "__main__":
    app.run(debug=True, port=4323)
