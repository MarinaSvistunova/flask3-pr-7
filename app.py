import csv
import datetime
import os.path
import sqlite3

from flask import Flask, url_for, g, make_response
from flask import render_template, session, redirect
from flask import request, flash

from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from FDataBase import FDataBase

from wtforms import Form, BooleanField, StringField, PasswordField, IntegerField, validators

from werkzeug.security import generate_password_hash, check_password_hash

from UserLogin import UserLogin


# config
DATABASE = '/tmp/iito.db'
DEBUG = True
SECRET_KEY = 'jvnp[oasmf#4jlavn%$!3]6;fdljvaoiubvcqwu'


app = Flask(__name__)
app.config['SECRET_KEY'] = 'a36021ba723815fd92c4913d4978d2698ee53e48680281bc2f7afae1e068b5cc82e4bfa91bcc0a70'
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'iito.db')))
app.permanent_session_lifetime = datetime.timedelta(days=10)




class ReviewForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=50)])
    email = StringField('Email', [validators.Length(min=4, max=50)])
    review = StringField('Review', [validators.Length(min=6, max=500)])

class UserForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=50)])
    email = StringField('Email', [validators.Length(min=4, max=50)])
    psw = PasswordField('Password')
    psw2 = PasswordField('Repeat password')
    time = IntegerField('Time')

class LoginForm(Form):
    email = StringField('Email', [validators.Length(min=4, max=50)])
    psw = PasswordField('Password')



login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, dbase)

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row # not tuple, is dict
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as file:
        db.cursor().executescript(file.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.sq_db = connect_db()
    return g.sq_db

dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.iito.close()

@app.route('/', methods=['GET', 'POST'])
def main_route():
    if 'visits' in session:
        session.permanent = True
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1

    form = ReviewForm(request.form)
    reviews = []
    reviews = dbase.getReviews()

    if request.method == 'POST':
        if len(request.form['name']) > 3 and len(request.form['review']) > 3:
            res = dbase.addReview(request.form['name'], request.form['email'], request.form['review'])
            if not res:
                flash('Fall', category="error")
            else:
                flash('OK', category="success")
        else:
            flash('Fall', category="error")

    return render_template('layout.html', form=form, reviews=reviews)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            userlogin = UserLogin().create(user)
            rm = True if request.form['remainme'] else False
            login_user(userlogin, remember=rm)
            return redirect(url_for('main_route'))
        
        flash('False email/password', 'error')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm(request.form)
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['psw']) > 4 \
            and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['name'], request.form['email'], hash)
            if res:
                flash('Registration is succesfull', 'success')
                return redirect(url_for('login'))
            else:
                flash('Registration faild', 'error')
        else:
            flash('Problems with fields', 'error')
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You logout", "success")
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    return f"""<p><a href="{url_for('logout')}">Logout</a>
                <p>user info: {current_user.get_id()}"""


@app.route('/hash')
def r():
    h = generate_password_hash('PROG-7#1')
    resp_dict = {'name': str(h)}
    d = {'code': 200}
    r = make_response(resp_dict, d['code'])
    r.headers['Content-Type'] = 'text/json;charset=utf-8'
    r.headers['Server'] = 'Flask/0.0.1'
    return r

if __name__ == '__main__':
    app.run(debug=True)


