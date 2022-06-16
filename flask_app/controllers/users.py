from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# put in routes

@app.route('/')
def index():
    return render_template('index.html')

#Create 
@app.route('/register/user', methods = ['POST'])
def register():
    if user.User.create_user(request.form):
        return redirect('/user/profile')
    return redirect('/')

#Read 
@app.route('/user/profile')
def view_profile():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('profile.html')

@app.route('/login', methods = ['POST'])
def login_user():
    if user.User.login(request.form):
        return redirect('/user/profile')
    return redirect('/')

#Update 


#Delete 
@app.route('/logout')
def logout_user():
    session.clear()
    return redirect('/')