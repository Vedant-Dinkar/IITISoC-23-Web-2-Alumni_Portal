from flask import Flask, render_template, g, request
from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def compiled():
    return render_template('compiled.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)