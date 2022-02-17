from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import User

from app import app, db, bcrypt


class SignUpForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=50)]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "The username is taken. Please choose a different username."
            )


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=50)]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError(
                "Could not find a user with this username. Please try again.")

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(user.password, password.data):
            raise ValidationError("Password does not match. Please try again.")
