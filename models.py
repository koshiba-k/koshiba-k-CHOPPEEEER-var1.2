# models.py
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from pytz import timezone

# ユーザーテーブル
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    employee_number = db.Column(db.String(100), unique=True, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# 体調テーブル
class HealthRecord(db.Model):
    __tablename__ = 'health_record'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    throat = db.Column(db.String(100))
    fever = db.Column(db.String(100))
    cough = db.Column(db.String(100))
    selected_parts = db.Column(db.JSON)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone('Asia/Tokyo')))  # 日本の標準時間でのデフォルト値
    flag = db.Column(db.Integer, default=0) # 不調フラグ
    def __repr__(self):
        return f'<HealthRecord {self.id} by User {self.user_id}>'

# 部署名テーブル
class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)  # 部署名
    abbreviation = db.Column(db.String(10), unique=True, nullable=False)  # 部署の略称

    def __repr__(self):
        return f'<Department {self.name}>'

# お知らせテーブル
class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone('Asia/Tokyo')))  # 日本の標準時間でのデフォルト値