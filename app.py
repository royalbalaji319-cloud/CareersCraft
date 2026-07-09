from flask import Flask, render_template
from config import Config
from database.db import mysql
from routes.auth import auth

app = Flask(__name__)

app.config.from_object(Config)

mysql.init_app(app)

app.register_blueprint(auth)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/test")
def test():
    return "Render Working Successfully!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
