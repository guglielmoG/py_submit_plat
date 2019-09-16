from app import flask_app, db
from flask import redirect, url_for, render_template, flash
from app.forms import WelcomeForm, SignupForm, LoginForm
from app.models import Groups

@flask_app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #check credentials
        group = Groups.query.filter_by(group_name=form.group_name.data).first()
        if group is None or group.group_psw != form.group_psw.data:
            flash('Invalid group name or password.')
            return redirect(url_for('login'))
        else:
            #login user
            return redirect(url_for('challenge'))
    return render_template('login.html', form=form)
    
@flask_app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        #save data to Db
        new_group = Groups(group_name=form.group_name.data, group_psw=form.group_psw.data)
        db.session.add(new_group)
        db.session.commit()
        #login user
        return redirect(url_for('challenge'))
    return render_template('signup.html', form=form)
    
@flask_app.route('/challenge')
def challenge():
    return render_template('challenge.html', room='test-room', n_users='1', text=sample_challenge['text'])

@flask_app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    form = WelcomeForm()
    if form.validate_on_submit():
        create = form.create.data
        if create:
            return redirect(url_for('signup'))
        else:
            return redirect(url_for('login'))
    return render_template('welcome.html', form=form)

@flask_app.route('/')
def index():
    return redirect(url_for('welcome'))
    

@flask_app.route('/change_room')
def change_room():
    #logout user
    return redirect(url_for('welcome'))

sample_challenge = {"text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.", 
                    "hints": ["Lorem ipsum dolor sit amet",
                    "Ut enim ad minim veniam"]
                    }