from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from models import db, User, Menu, init_sample_data
from config import settings

app = Flask(__name__)
app.secret_key = settings.secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coffee_shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# with app.app_context():
    # db.drop_all()
    # db.create_all()
    # init_sample_data()

@app.route('/')
def home():
    menu_items = Menu.query.filter_by(active=True).all()
    print(f"Знайдено {len(menu_items)} активних позицій меню")
    return render_template('home.html', menu_items=menu_items)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        phone = request.form.get('phone', '')
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')

        if User.query.filter_by(username=username).first():
            flash("Користувач з таким ім'ям вже існує!")
            return render_template('signup.html')

        user = User(
            username=username,
            email=email,
            phone_number=phone,
            first_name=first_name,
            last_name=last_name
        )
        user.password = password

        db.session.add(user)
        db.session.commit()

        flash('Реєстрація успішна! Тепер ви можете увійти.')
        return redirect(url_for('signin'))

    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.is_verify_password(password):
            login_user(user)
            flash('Успішний вхід!')
            return redirect(url_for('home'))
        else:
            flash('Невірне ім\'я користувача або пароль!')
    return render_template('signin.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return redirect(url_for('signup'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    return redirect(url_for('signin'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Ви вийшли з системи.')
    return redirect(url_for('home'))

@app.route('/menu')
def menu():
    menu_items = Menu.query.filter_by(active=True).all()
    print(f"На сторінці меню знайдено {len(menu_items)} активних позицій")
    return render_template('menu.html', menu_items=menu_items)

@app.route('/debug/menu')
def debug_menu():
    all_items = Menu.query.all()
    active_items = Menu.query.filter_by(active=True).all()

    debug_info = {
        'total_items': len(all_items),
        'active_items': len(active_items),
        'items': [{'type': item.type, 'active': item.active, 'price': item.price} for item in all_items]
    }

    return f"<pre>{debug_info}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
