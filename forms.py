# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from models import User, Department

def unique_username(form, field):
    if User.query.filter_by(name=field.data).first():
        raise ValidationError("このユーザー名はすでに使用されています。")

def unique_employee_number(form, field):
    if User.query.filter_by(employee_number=field.data).first():
        raise ValidationError("この社員番号はすでに使用されています。")

def unique_email(form, field):
    if User.query.filter_by(email=field.data).first():
        raise ValidationError("このメールアドレスはすでに使用されています。")

# ログイン用フォーム
class LoginForm(FlaskForm):
    employee_number = StringField(
        '社員番号',
        validators=[DataRequired(message="社員番号は必須です。")]
    )
    password = PasswordField(
        'パスワード',
        validators=[DataRequired(message="パスワードは必須です。")]
    )
    submit = SubmitField('ログイン')


# 社員登録フォーム
class AddEmployeeForm(FlaskForm):
    employee_number = StringField(
        '社員番号',
        validators=[DataRequired(message="社員番号は必須です。")]
    )
    department = SelectField(
        '部署',
        choices=[],
        validators=[DataRequired(message="部署は必須です。")]
    )
    name = StringField(
        '氏名',
        validators=[DataRequired(message="氏名は必須です。")]
    )
    phone = StringField(
        '電話番号',
        validators=[DataRequired(message="電話番号は必須です。")]
    )
    email = StringField(
        'メールアドレス',
        validators=[DataRequired(message="メールアドレスは必須です。"), Email()]
    )
    password = PasswordField(
        'パスワード',
        validators=[
            DataRequired(message="パスワードは必須です。"),
            Length(min=4, max=16, message="パスワードは4文字以上16文字以下です。"),
            Regexp('^(?=.*[a-z])(?=.*[0-9])', message="パスワードは小文字と数字を含む必要があります。")
        ]
    )
    confirm_password = PasswordField(
        '確認用パスワード',
        validators=[DataRequired(message="確認用パスワードは必須です。"), EqualTo('password', message="パスワードが一致しません。")]
    )
    is_admin = BooleanField('管理者権限')
    submit = SubmitField('登録')

    def __init__(self, *args, **kwargs):
        super(AddEmployeeForm, self).__init__(*args, **kwargs)
        self.department.choices = [(d.abbreviation, d.name) for d in Department.query.all()]

    def validate_employee_number(self, employee_number):
        if User.query.filter_by(employee_number=employee_number.data).first():
            raise ValidationError('その社員番号は既に使用されています。')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('このメールアドレスはすでに使用されています。')

    def validate_phone(self, phone):
        if User.query.filter_by(phone=phone.data).first():
            raise ValidationError('この電話番号はすでに使用されています。')

# パスワード変更フォーム
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(
        '現在のパスワード',
        validators=[DataRequired(message="現在のパスワードは必須です。")]
    )
    new_password = PasswordField(
        '新しいパスワード',
        validators=[DataRequired(message="新しいパスワードは必須です。")]
    )
    confirm_password = PasswordField(
        '新しいパスワード確認',
        validators=[
            DataRequired(message="新しいパスワード確認は必須です。"),
            EqualTo('new_password', message="新しいパスワードが一致しません。")
        ]
    )
    submit = SubmitField('変更')
    
# 社員変更フォーム
class EmployeeForm(FlaskForm):
    employee_id = StringField('社員番号', validators=[DataRequired(), Length(max=100)])
    department = SelectField('部署', choices=[], validators=[DataRequired()])
    name = StringField('氏名', validators=[DataRequired(), Length(max=100)])
    phone = StringField('電話番号', validators=[DataRequired(), Length(max=15)])
    email = StringField('メールアドレス', validators=[DataRequired(), Email(), Length(max=120)])
    admin_rights = BooleanField('管理者権限')
    submit = SubmitField('変更')