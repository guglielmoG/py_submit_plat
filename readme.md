# Python Challenges Platform

A platform to conveniently run Python programming competitions.  
Students divide in teams to solve programming exercises, upload their code to the platform which checks correctness and assigns it a score. May the best team win!

Check out a live version at [http://81.30.3.98:4152/welcome](http://81.30.3.98:4152/welcome)!




### Init
Clone the project first. Then open the terminal when you cloned to and do the following:
* create a virtual environment `python3 -m venv venv`
* install dependencies `pip install -r requirements.txt`
* set flask app environment variable `export FLASK_APP=py_submit_plat.py` or `set FLASK_APP=py_submit_plat.py` if you are on Windows
* create the Db `flask db upgrade`
* run the app `python py_submit_plat.py`

Note that the above will create a (local) SQLite database called `app.db`, if you wish to connect to a remote Db just change the property `SQLALCHEMY_DATABASE_URI` within `config.py`, refer to [SQLAlchemy](https://docs.sqlalchemy.org/en/13/) documentation for more info. 
By default the webserver is accessible at http://127.0.0.1:5000, this is handy because it can then be accessed via a reversed proxy (e.g. [NGINX](https://www.nginx.com/)). If you wish to have it directly available to the local network, refer to [Flask](http://flask.palletsprojects.com/en/1.1.x/) and [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/) documentation.

### How It Works

After cloning the project, you need to edit `/source/challenges.py` and `/source/solutions.py`, the former contains the text and related information of each challenge. The second includes the solutions (test cases) used to check the uploaded script: the rationale is that usually just one test is not sufficient to asses the correctness of the provided script (corner cases). The bulk of the information regarding the platform's functioning is detailed in `/app/templates/welcome.html`, which is served at `/welcome` if one visits the webapp. To control the challenge, one can visit the URL `/challenge?master_pass=guglielmo` after logging in. Here we summarize the main **features**:
* tracking registration/login of users as members of teams
* data updated in real-time within teams, for instance if a team member submits some code all the other members see the new score 
* real-time scoreboard showing top three teams for each challenge
* possibility to prevent access to Python functions and modules (default setting)
* automated system for submitted code evaluation 
* possibility to set max running time for each test case (default 1 sec)
* ability to (forcefully) end challenge and show final results/ranking (can be undone)

### Security Considerations
Due to the nature of the project, which is that to execute and test arbitrary Python code, numerous security issues are raised. The principal one is without doubt the use of `exec()`. The first step is that of preventing access to builtins, by passing `{'__builtins__':None}` as globals. Unfortunately that is not enough (as detailed [here](https://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html)), so to address this new issue, the platform won't run any code containing '__', which basically is explicitly revoking access to Python internal constructs. It is just a slight limitation, as in most of the cases these are not needed especially in the scope of a challenge. That should be enough. 
Note also that, given the nature of data exchanged between client and server and more abstractly the goal of the platform, the communication over the web is not crypted. Also, password are stored as they are in the Db instead of recording just an hash. The person interested will find the latter pretty easy to implement (edit Users class within `app.models.py`), regarding the former one could setup NGINX to do that for you, paying close attention that this application makes use of WebSockets.

### Further Steps
The platform is fully working as is. Useful features which may come in the future are:
* Add password hashing
* Add code validation function, with the idea of checking user code for specific constructs whose usage wants to be prevented (e.g. list comprehensions, ifs, loops, etc..)
* Integrate reading of test cases from text files, to address bigger input/output processing 
* Create different exercise types, such as classic (no constraints), timed (time limit on test cases), etc
* Add max overall challenge time, expired which the teams won't be able to upload code any longer and the final scores will be published

### Branch Description
There are three branches. I know the git workflow is to usually merge them quite quickly, however I am not planning on doing that anytime soon, therefore it's best to leave a short description.
* **master**: contains a stable version of the platform in its minimal form. It runs on SQLite.
* **pymysql**: it is the same as **master** but can run with a MySQL server. The reason why these two branches are separated is that for some reason SQLAlchemy experiences problems when working with the db from within a thread (the SQLAlchemy object wrapped by Flask-SQLAlchemy should already be thread-safe). It was faster to move to pymysql module instead of debug it. This is dev branch where improvements are (eventually) merged back.
