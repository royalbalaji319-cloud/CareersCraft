from flask import Flask, render_template
from config import Config
from database.db import mysql
from routes.auth import auth

app = Flask(__name__)

# Load Configuration
app.config.from_object(Config)

# Secret Key
app.secret_key = app.config["SECRET_KEY"]

# MySQL Configuration
app.config["MYSQL_HOST"] = Config.MYSQL_HOST
app.config["MYSQL_PORT"] = Config.MYSQL_PORT
app.config["MYSQL_USER"] = Config.MYSQL_USER
app.config["MYSQL_PASSWORD"] = Config.MYSQL_PASSWORD
app.config["MYSQL_DB"] = Config.MYSQL_DB

# Debug (Temporary - Remove Later)
print("MYSQL_HOST =", app.config["MYSQL_HOST"])
print("MYSQL_USER =", app.config["MYSQL_USER"])
print("MYSQL_PASSWORD =", app.config["MYSQL_PASSWORD"])
print("MYSQL_DB =", app.config["MYSQL_DB"])

# Initialize MySQL
mysql.init_app(app)

# Register Blueprint
app.register_blueprint(auth)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/test")
def test():
    return "Render Working Successfully!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
