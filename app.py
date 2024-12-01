#app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # セキュリティキーを設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # 適切なデータベースを設定
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

# ルーティングのインポート
from routes import *

# アプリケーションの実行
if __name__ == '__main__':
    debug = False
    app.run(host='0.0.0.0', port=8080, debug=debug)

