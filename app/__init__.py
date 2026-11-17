import os
import sqlite3

from flask import Flask, jsonify, render_template


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-only-change-me"),
        DATABASE=os.environ.get("DATABASE_PATH", os.path.join(app.instance_path, "sms.sqlite")),
        APP_VERSION=os.environ.get("APP_VERSION", "local"),
    )
    if test_config:
        app.config.update(test_config)
    os.makedirs(app.instance_path, exist_ok=True)

    from . import db
    db.init_app(app)

    @app.route("/")
    def index():
        return render_template("index.html", version=app.config["APP_VERSION"])

    @app.route("/health")
    def health():
        try:
            db.get_db().execute("SELECT 1")
            status = "ok"
        except sqlite3.Error:
            return jsonify(status="db_error"), 500
        return jsonify(status=status, version=app.config["APP_VERSION"])

    return app
