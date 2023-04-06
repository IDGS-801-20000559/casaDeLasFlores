from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
#from .models import Product
from sqlalchemy import engine, MetaData
from sqlalchemy.schema import Table
from sqlalchemy.orm import sessionmaker
from flask_security.decorators import roles_required

main = Blueprint('main', __name__)

@main.route("/")
def inicio():
    return render_template('index.html', user=current_user)

@main.route('/login', methods = ['GET', 'POST'])
def index():
    return render_template('login.html')

@main.route('/register', methods = ['GET', 'POST'])
def register():
    return render_template('register.html')