# config.py
import os

class Config:
    SECRET_KEY = os.urandom(24)  # 秘密鍵
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'data.sqlite')}"  # データベースURI
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 変更追跡を無効化