from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_login import login_user, LoginManager, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from quiz import Questions,Score
from forms import *
from database import db,Players
import html
from flask_bcrypt import Bcrypt
#https://opentdb.com/api.php?amount=5&category=9&difficulty=medium&type=boolean

query_manager = Questions(amount=5,difficulty='medium',question_type='boolean',category=9)
quiz_score = Score()
app = Flask(__name__)
app.config["SECRET_KEY"] = 'sDS7a!3f0FISf0f0f*(9*Rf9-D(*29xA9GAFDF*(29t8f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///players.db'
app.jinja_env.filters['unescape'] = lambda text: html.unescape(text)
bcrypt = Bcrypt(app)
Bootstrap5(app)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(Players, user_id)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login",methods=['GET','POST'])
def login():
    login_form = LogInForm()
    if login_form.validate_on_submit() and request.method == 'POST':
        name_given = request.form.get("name")
        #find user by name
        searched_user = db.session.execute(db.select(Players).where(Players.name == request.form.get("name"))).scalar()
        if searched_user and db.session.execute(db.select(Players).where(Players.email == searched_user.email)).scalar() and bcrypt.check_password_hash(searched_user.password,request.form.get("password")):
            login_user(searched_user)
            return redirect(url_for('home'))

        if not searched_user:
            flash("That name does not exist, please try again.")
            return redirect(url_for('login'))

        # if not email_is_valid:
        #     flash("That email does not exist.")
        #     return redirect(url_for('login'))

        if not bcrypt.check_password_hash(searched_user.password,request.form.get("password")):
            flash("The password does not exist, please try again.")
            return redirect(url_for('login'))

    return render_template("login.html",form=login_form)

@app.route("/register",methods=['GET','POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit() and request.method == 'POST':
        if db.session.execute(db.select(Players).where(Players.email == request.form.get("email"))).scalar():
            flash("You are already signed up with that email, log in instead.")
            return redirect(url_for('login'))

        new_player = Players(name=request.form.get("name"),
                             email=request.form.get("email"),
                             password=bcrypt.generate_password_hash(request.form.get("password"),12),
                             score=0,answered_questions=0,correct_answers=0,false_answers=0)
        db.session.add(new_player)
        db.session.commit()
        login_user(new_player)
        return redirect(url_for('home'))
    return render_template("register.html",form=register_form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/quiz_game",methods=['GET','POST'])
def game():
    quiz = query_manager.get_questions()
    if quiz["status"] == "success":
        if request.method == 'POST':
            user_answers = [request.form.get(f'answer{i}') for i in range(len(quiz["questions"]))]
            correct_answers = [x["correct_answer"] for x in quiz["questions"]]
            print(quiz_score.check_answers(user_answers,correct_answers))
            return redirect(url_for('home'))
        return render_template("game.html",questions=quiz["questions"])
    return render_template("error.html",error=quiz["error"])

if __name__ == "__main__":
    app.run(debug=True,port=5005)
