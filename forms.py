from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms import FieldList, FormField, SelectMultipleField

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтверждение пароля', validators=[DataRequired(), EqualTo('password')])
    
    # Поля для чекбоксов
    politics = BooleanField('Политика')
    society = BooleanField('Общество')
    ukraine = BooleanField('Украина')
    incidents = BooleanField('Происшествия')
    economy = BooleanField('Госэкономика')
    football = BooleanField('Футбол')
    cinema = BooleanField('Кино')
    internet = BooleanField('Интернет')
    business = BooleanField('Бизнес')
    investigation = BooleanField('Следствие и суд')
    science = BooleanField('Наука')
    music = BooleanField('Музыка')
    
    submit = SubmitField('Зарегистрироваться')

    def validate_tags(self):
        tags_count = sum([
            self.politics.data,
            self.society.data,
            self.ukraine.data,
            self.incidents.data,
            self.economy.data,
            self.football.data,
            self.cinema.data,
            self.internet.data,
            self.business.data,
            self.investigation.data,
            self.science.data,
            self.music.data
        ])

        if tags_count < 3:
            raise ValidationError('Пожалуйста, выберите как минимум 3 тега.')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
