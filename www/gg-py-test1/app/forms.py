from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SelectField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, Account


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class CreateAccountForm(FlaskForm):
    nickname = StringField('Nickname', validators=[DataRequired(), Length(min=4, max=64, message='Must be at least 4 characters and no more than 64')])
    rank = IntegerField('Rank')
    clanname = StringField('Clanname', validators=[Length(max=64, message='Must be no more than 64 characters')])
    accounttype = SelectField('Account type', choices=[(1, 'User'), (2, 'Moderator'), (3, 'Administrator')])
    submit = SubmitField('Create account')

    def validate_nickname(self, nickname):
        account = Account.query.filter_by(nickname=nickname.data).first()
        if account is not None:
            raise ValidationError('Please use a different nickname.')


class SearchForm(FlaskForm):
    search = StringField('Search')
