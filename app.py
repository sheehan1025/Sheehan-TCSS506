#!/usr/bin/python3
# Import the necessary modules

from flask import Flask, render_template, request, redirect, url_for, session, flash
from yelp import findBusiness
from forms import LoginForm, SearchForm
from flask_login import login_user, logout_user, login_required, current_user
from models import db, loginManager, UserModel

# Create a new Flask application instance
app = Flask(__name__)
app.secret_key="secret"

#database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#initialize the database
db.init_app(app)

#initialize the login manager
loginManager.init_app(app)

def addUser(email, password):
    user = UserModel()
    user.setPassword(password)
    user.email=email
    db.session.add(user)
    db.session.commit()

#handler for bad requests
@loginManager.unauthorized_handler
def authHandler():
    form=LoginForm()
    flash('Please login to access this page')
    return render_template('login.html',form=form)

# some setup code because we don't have a registration page or database
@app.before_first_request
def create_table():
    db.create_all()
    user = UserModel.query.filter_by(email = 'lhhung@uw.edu' ).first()
    if user is None:
        addUser("lhhung@uw.edu","qwerty")
    else:
        logout_user()

# Define a route for the root URL ("/") that returns "Hello World"
@app.route('/home', methods=['GET', 'POST'])
@login_required
def showBusiness():
    searchForm = SearchForm()
    if(request.args.get('city')):
        session['city']=request.args.get('city')
    if 'term' not in session:
        session['term'] = 'coffee shop'
    if request.method is 'POST' and searchForm.validate_on_submit != 0:
        session['term'] = searchForm.searchTerm.data
    if 'city' in session:
        return render_template('home.html', myData=findBusiness(city=session['city'], term=session['term']), searchForm=searchForm)
    # This function will be called when someone accesses the root URL
    return render_template('home.html', myData=findBusiness(term=session['term']), searchForm=searchForm)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Please enter a valid email and password')
            return render_template('login.html',form=form)
        user = UserModel.query.filter_by(email = form.email.data ).first()
        if user is None:
            flash('Please enter a valid email')
            return render_template('login.html',form=form)
        if not user.checkPassword(form.password.data):
            flash('Please enter a valid password')
            return render_template('login.html',form=form)
        login_user(user)
        session['email'] = form.email.data
        session['city']='Tacoma'
        return redirect(url_for('showBusiness'))
    # This function will be called when someone accesses the root URL
    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    session.pop('email', None)
    session.pop('city', None)
    session.pop('term', None)
    session.pop(session['term'], None)
    # This function will be called when someone accesses the root URL
    return redirect(url_for('login'))

# Run the application if this script is being run directly
if __name__ == '__main__':
    # The host is set to '0.0.0.0' to make the app accessible from any IP address.
    # The default port is 5000.
    app.run(host='0.0.0.0', debug='true', port=5000)
