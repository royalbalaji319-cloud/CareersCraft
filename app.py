from flask import Flask, render_template
from config import Config
from database.db import mysql
from routes.auth import auth

app = Flask(__name__)

# Load configuration
app.config.from_object(Config)

# Initialize MySQL
mysql.init_app(app)

# Register Blueprints
app.register_blueprint(auth)

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Health Check (for testing)
@app.route("/health")
def health():
    return "CareersCraft is Running Successfully!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
