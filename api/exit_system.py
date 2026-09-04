from flask import redirect, url_for


def register_exit_system(app):

    @app.route("/exit")
    def exit_system():
        return redirect(url_for("login"))
