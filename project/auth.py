# auth.py

from sqlalchemy.dialects.postgresql import UUID
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

from .utils import deactivate_invite_code
from .models import Code, User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    input_invite_code = request.form.get('invite-code')
    
    invite_code = Code.query.filter_by(token=input_invite_code).first()

    if not invite_code or invite_code.active == 0:
        flash('Invalid code', 'is-danger')
        return redirect(url_for('auth.signup', error="Invalid invite code"), )
    else:
        # flash('You were successfully logged in')
        flash('Registered successfully', 'is-success')
        deactivate_invite_code(invite_code)

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again  
        flash('You cannot use this email to register')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), active=0)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/uuid_generate')
def uuid_generate():

    # email = request.form.get('email')
    # name = request.form.get('name')
    # password = request.form.get('password')
    # invite_code = request.form.get('invite-code')
    
    # user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    # if user: # if a user is found, we want to redirect back to signup page so user can try again  
    #     flash('Email address already exists')
    #     return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    uuid_generated = Code(active=1)

    # add the new user to the database
    db.session.add(uuid_generated)
    db.session.commit()

    return render_template('uuid_generate.html', uuid_generated=uuid_generated)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))