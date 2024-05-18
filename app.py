from flask import Flask, render_template, request, url_for, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://user:pass@domain/database'
app.config["SECRET_KEY"] = "xxxxxxxxxxxxxxx"

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(255), unique=True, nullable=False)
   email = db.Column(db.String(255), unique=True, nullable=False)
   password = db.Column(db.String(255), nullable=False)

db.init_app(app)

with app.app_context():
	db.create_all()

@login_manager.user_loader
def loader_user(user_id):
	return User.query.get(user_id)

@app.route('/')
def index():
    if current_user.is_authenticated:
       return render_template('index.html')
    else:
       return redirect(url_for('login'))

@app.route('/sign_up', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
       username = request.form.get('user')
       email = request.form.get('email')
       password = request.form.get('pass')

       save_db = User(username=username, email=email, password=password)

       db.session.add(save_db)
       db.session.commit()
       
       return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/sign_in', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
       email= request.form.get('email')
       password = request.form.get('pass')

       user = User.query.filter_by(email=email).first()

       if user.password == password:
          login_user(user)
          return redirect(url_for('index'))
       else:
          flash('Incorrect credentials')

    return render_template('login.html')

@app.route('/log_out')
def log_out():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
   app.run(debug = True)
