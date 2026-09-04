from flask import render_template, redirect, url_for, request, jsonify, session
from functools import wraps


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated


def register_admin(app, bcrypt):

    @app.route("/admin/login", methods=["GET", "POST"])
    def admin_login():
        if request.method == "POST":
            password = request.form.get("password", "")
            admin_password = app.config["ADMIN_PASSWORD"]
            if password == admin_password:
                session['admin_logged_in'] = True
                return redirect(url_for('admin_panel'))
            return render_template("admin_login.html", error="Неверный пароль")
        return render_template("admin_login.html")

    @app.route("/admin")
    @admin_required
    def admin_panel():
        return render_template("admin.html")

    @app.route("/admin/logout")
    def admin_logout():
        session.pop('admin_logged_in', None)
        return redirect(url_for('admin_login'))

    @app.route("/api/admin/users", methods=["GET"])
    @admin_required
    def admin_get_users():
        try:
            from db_manager import get_all_users
            users = get_all_users()
            return jsonify(users)
        except ImportError:
            return jsonify([])

    @app.route("/api/admin/users/<int:user_id>/confirm", methods=["POST"])
    @admin_required
    def admin_confirm_user(user_id):
        try:
            from db_manager import confirm_user
            confirm_user(user_id)
            return jsonify({"status": "success"})
        except ImportError:
            return jsonify({"status": "error", "message": "Database not available"}), 500

    @app.route("/api/admin/users/<int:user_id>/reject", methods=["POST"])
    @admin_required
    def admin_reject_user(user_id):
        try:
            from db_manager import reject_user
            reject_user(user_id)
            return jsonify({"status": "success"})
        except ImportError:
            return jsonify({"status": "error", "message": "Database not available"}), 500

    @app.route("/api/admin/stats", methods=["GET"])
    @admin_required
    def admin_stats():
        try:
            from db_manager import get_stats
            stats = get_stats()
            return jsonify(stats)
        except ImportError:
            return jsonify({"total": 0, "confirmed": 0, "pending": 0})
