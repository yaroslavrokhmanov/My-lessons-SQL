# fily konfiguracii podkluczenia k  baze danych
import os

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:242187@localhost/postwall_db"  # Podkluczenie k baze dannych
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    