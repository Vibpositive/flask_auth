# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/error')
def error():
    return render_template('error.html')

@main.route('/form')
def form():
    return render_template('form.html')
