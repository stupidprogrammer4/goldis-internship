from flask import Flask, render_template, session, request, redirect, flash, jsonify
import sqlite3
import secrets
import bcrypt
from configs import ADMIN_USERNAME, DATABASE_PATH, SALT

app = Flask(__name__, template_folder='golabi', static_folder='havij')
app.secret_key = secrets.token_hex(16)


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def search_user(username: str):
    conn = get_db_connection()
    curr = conn.cursor()
    user = curr.execute("""SELECT username, password
                           FROM users WHERE username = ?""",
                        (username,)).fetchone()
    conn.close()
    return user

def is_valid_user_pass(username: str, password: str):
    is_valid = False
    data = search_user(username)
    if data:
        hashed_pass = bcrypt.hashpw(password.encode('utf-8'), SALT).decode('utf-8')
        print(hashed_pass, data[1])
        if hashed_pass == data[1]:
            is_valid = True
    return is_valid

@app.route('/')
@app.route('/index')
def index():
    is_admin = False
    if 'username' in session:
        session['authenticated'] = True
        if session['username'] == ADMIN_USERNAME:
            is_admin = True
    conn = get_db_connection()
    curr = conn.cursor()
    _, _, _, name, about, email, phonenumber = curr.execute('SELECT * from users where username = ?', (ADMIN_USERNAME,)).fetchone()
    experiences = curr.execute('SELECT * FROM experiences').fetchall()
    educations = curr.execute('SELECT * FROM educations').fetchall()
    skills = curr.execute('SELECT name, rate FROM skills').fetchall()

    conn.close()
    return render_template('index.html', name=name, about=about, email=email, 
                           phonenumber=phonenumber, experiences=experiences, 
                           educations=educations, skills=skills, is_admin=is_admin)

@app.route('/login')
def login():
    response = redirect('/dashboard')
    if 'username' not in session:
        response = render_template('login.html')
    return response

@app.post('/login-post')
def login_post():
    username = request.form['username'].strip()
    password = request.form['password'].strip()
    path = '/login'
    if is_valid_user_pass(username, password):
        session['username'] = username
        path = '/index'
    else:
        flash('invalid username or password')
    return redirect(path)

@app.get('/signup')
def signup():
    return render_template('signup.html')


@app.post('/signup-post')
def signup_post():
    if 'username' in session:
        return redirect('/index')
    path = '/signup'
    username = request.form['username'].strip()
    password = request.form['password'].strip()

    if not search_user(username):
        session['username'] = username
        path = '/index'
        conn = get_db_connection()
        curr = conn.cursor()

        curr.execute("""INSERT INTO users
                     (username, password)
                     VALUES(?, ?)
        """, (username, bcrypt.hashpw(password.encode('utf-8'), SALT).decode('utf-8')))
        conn.commit()

        conn.close()
    else:
        flash(f'username {username} already taken!')

    return redirect(path)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


"""
TODO: handle errors for apis
send errors to js and show them to user
"""
@app.post('/add-experience')
def add_experience():
    data = request.json
    conn = get_db_connection()
    curr = conn.cursor()
    curr.execute("""INSERT INTO experiences
                 (job_title, company_name, desc, start_date, end_date)
                 VALUES(?, ?, ?, ?, ?)""", (data['job_title'], data['company_name'], data['desc'], data['start_date'], data['end_date']))
    conn.commit()

    conn.close()
    return jsonify({"status": "success", "message": "Experience added successfully"})

@app.post('/add-education')
def add_education():
    data = request.json
    conn = get_db_connection()
    curr = conn.cursor()
    curr.execute("""INSERT INTO educations
                 (degree_name, institution, start_date, end_date)
                 VALUES(?, ?, ?, ?)""", (data['degree_name'], data['institution'], data['start_date'], data['end_date']))
    conn.commit()
    return jsonify({"status": "success", "message": "Education added successfully"})

@app.post('/add-skill')
def add_skill():
    data = request.json
    conn = get_db_connection()
    curr = conn.cursor()
    curr.execute("""INSERT INTO skills
                 (name, rate)
                 VALUES(?, ?)""", (data['name'], data['rate']))
    conn.commit()
    return jsonify({"status": "success", "message": "Education added successfully"})


app.run(debug=True, port=1234)