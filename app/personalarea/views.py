from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from .models import User
from .forms import LoginForm, SignUpForm, AddServiceForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from app.database import db

personalarea = Blueprint('personalarea', __name__)

@personalarea.route("/", methods=['GET', 'POST'])
def main():
    return render_template("index.html")

@personalarea.route("/personal", methods=['POST', 'GET'])
@personalarea.route("/personal/<ip>")
def personal(ip=None):
    form = AddServiceForm()
    services = current_user.get_last_scan_date()
    if form.validate_on_submit():
        new_service_ip = form.ip.data
        db.add_target(current_user._name, new_service_ip)
        return redirect(url_for('personalarea.personal'))
    if ip:
        db.del_target(current_user._name, ip)
        return redirect(url_for('personalarea.personal'))
    return render_template("personal.html", form=form, services=services)

@personalarea.route("/signup", methods=['POST', 'GET'])
def sign_up():

    if current_user.is_authenticated:
        return redirect(url_for('personalarea.personal'))

    form = SignUpForm()

    if form.validate_on_submit():
        name = form.name.data
        form.validate_username(name)
        email = form.email.data
        password = form.password.data
        hash_pwd = generate_password_hash(password)
        db.add_client(name, hash_pwd, email)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('personalarea.login'))
    return render_template("signup.html", form=form)

@personalarea.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('personalarea.personal'))

    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User(form.name.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or bad password.')
            return redirect(url_for('personalarea.login'))
        login_user(user)
        return redirect(url_for('personalarea.personal'))
    return render_template("login.html", form=form)

@personalarea.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
