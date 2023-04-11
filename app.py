from db import get_connection
from flask import Flask, redirect, jsonify, render_template
from flask import request
from flask import url_for
from config import DevelopmentConfig


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)


@app.route('/login', methods = ['GET', 'POST'])
def index():
    print('Hola mi gente')
    return render_template('login.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            return redirect(url_for('home'))
        else:
            return redirect(url_for('index'))
    return render_template('login.html')


if __name__ == '__main__':
    app.run(port=3000)