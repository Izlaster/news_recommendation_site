import pandas as pd

from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm
from models import db, User, Log

app = Flask(__name__)
app.config.from_object('config.Config')

# Инициализация базы данных и менеджера авторизации
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Указываем, куда перенаправлять неавторизованных пользователей

news_df = pd.read_csv('dataset/lenta-ru-news-likes.csv', low_memory=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Загружаем пользователя по ID

@app.route('/')
@login_required
def home():
    tags = current_user.tags.split(', ') if current_user.tags else []

    # Отфильтровываем новости по интересам пользователя
    filtered_news = news_df[news_df['tags'].isin(tags)]

    # Проверяем, есть ли у нас данные
    if not filtered_news.empty:
        # Преобразуем колонку 'date' в datetime, если это еще не сделано
        filtered_news['date'] = pd.to_datetime(filtered_news['date'], errors='coerce')
        
        # Удаляем строки с недопустимыми датами
        filtered_news = filtered_news.dropna(subset=['date'])

        # Получаем последние 10 новостей по дате
        latest_news = filtered_news.nlargest(10, 'date')
    else:
        latest_news = pd.DataFrame()  # или [] если хотите вернуть пустой список

    return render_template('home.html', tags=tags, news=latest_news)

def log_action(email, article_title, action):
    with 
    new_log = Log(username=email, article_title=article_title, action=action)
    db.session.add(new_log)
    db.session.commit()

@app.route('/track_click/<path:url>')
def track_click(url):
    email = current_user.email if current_user.is_authenticated else 'Гость'
    log_action(email, url, 'view')
    return redirect(url)

@app.route('/like_news/<path:url>', methods=['POST'])
def like_news(url):
    news_df[news_df["url"] == url]["likes"] += 1   # Получите статью по индексу

    email = current_user.email if current_user.is_authenticated else 'Гость'
    log_action(email, url, 'like')

    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Проверка на существование пользователя
        existing_user = User.query.filter(
            (User.username == form.username.data) | 
            (User.email == form.email.data)
        ).first()
        
        if existing_user:
            flash('Пользователь с таким именем или email уже существует.', 'danger')
            return redirect(url_for('register'))

        # Хешируем пароль
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        
        # Сохраняем выбранные теги
        selected_tags = []
        if form.politics.data:
            selected_tags.append('Политика')
        if form.society.data:
            selected_tags.append('Общество')
        if form.ukraine.data:
            selected_tags.append('Украина')
        if form.incidents.data:
            selected_tags.append('Происшествия')
        if form.economy.data:
            selected_tags.append('Госэкономика')
        if form.football.data:
            selected_tags.append('Футбол')
        if form.cinema.data:
            selected_tags.append('Кино')
        if form.internet.data:
            selected_tags.append('Интернет')
        if form.business.data:
            selected_tags.append('Бизнес')
        if form.investigation.data:
            selected_tags.append('Следствие и суд')
        if form.science.data:
            selected_tags.append('Наука')
        if form.music.data:
            selected_tags.append('Музыка')

        # Проверка на минимальное количество тегов
        if len(selected_tags) < 3:
            flash('Пожалуйста, выберите как минимум 3 тега.', 'danger')
            return redirect(url_for('register'))

        # Создаем нового пользователя
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            tags=', '.join(selected_tags)  # Сохраняем теги как строку, разделенную запятыми
        )
        
        # Сохраняем пользователя в базе данных
        db.session.add(new_user)
        db.session.commit()
        
        flash('Регистрация прошла успешно!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Неверные данные для входа.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта.', 'info')
    return redirect(url_for('login'))

@app.route('/create_db')
def create_db():
    db.create_all()
    return "База данных успешно создана!"

if __name__ == '__main__':
    app.run(debug=True)
