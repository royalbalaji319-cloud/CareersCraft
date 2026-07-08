from flask import Flask, render_template
from config import Config
from database.db import mysql
from routes.auth import auth

app = Flask(__name__)

app.secret_key = "AI_HIRE_SECRET_KEY"

app.config.from_object(Config)

mysql.init_app(app)

app.register_blueprint(auth)

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)