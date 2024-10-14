from __init__ import db
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, RadioField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class Task(db.Model):
    __tablename = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    importance: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=True)
    status: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)


class TaskForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()],
                       render_kw={"placeholder": "Enter task name", "class": "form-control"})
    importance = RadioField('Importance', choices=[('5', '5'), ('4', '4'), ('3', '3'), ('2', '2'), ('1', '1')],
                            default='0', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()],
                                render_kw={"placeholder": "Enter task description", "class": "form-control", "rows": 3})
    submit = SubmitField('Submit', render_kw={"class": "btn btn-primary btn-block mb-2"})


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],
                           render_kw={"placeholder": "Enter your username", "class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"placeholder": "Enter your password", "class": "form-control"})
    submit = SubmitField('Login', render_kw={"class": "btn btn-primary btn-block"})


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],
                           render_kw={"placeholder": "Enter your username", "class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"placeholder": "Enter your password", "class": "form-control"})
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match.')],
                                     render_kw={"placeholder": "Confirm your password", "class": "form-control"})
    submit = SubmitField('Register', render_kw={"class": "btn btn-primary"})
