import os

class Config:
    SECRET_KEY = os.getenv("balaji123")

    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("826412")
    MYSQL_DB = os.getenv("MYSQL_DB")

    ADZUNA_APP_ID = os.getenv("e233a6d7")
    ADZUNA_APP_KEY = os.getenv("14b5d769fb00f54b274d57b2486fdb06")
