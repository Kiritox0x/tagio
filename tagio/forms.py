from flask_wtf import Form
from wtforms import PasswordField, TextField, HiddenField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_security import LoginForm  # noqa

from tagio.models.user import User


class LoginForm(Form):
    next = HiddenField()
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me', default=False)
    submit = SubmitField('Submit')


    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()
        if not self.user:
            self.username.errors.append('Invalid username or password!')
            return False

        if not self.user.check_password(self.password.data):
            self.username.errors.append('Invalid username or password!')
            return False

        if not self.user.active:
            self.username.errors.append('User not activated')
            return False
        return True
