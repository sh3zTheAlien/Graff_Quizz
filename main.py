from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_login import login_user, LoginManager, current_user, logout_user
from sqlalchemy import desc
from quiz import Score,Questions
from forms import *
from database import db,Players
import html
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
load_dotenv()
#https://opentdb.com/api.php?amount=5&category=9&difficulty=medium&type=boolean

query_manager = Questions(amount=5,difficulty='medium',question_type='boolean',category=9)
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.jinja_env.filters['unescape'] = lambda text: html.unescape(text)
bcrypt = Bcrypt(app)
Bootstrap5(app)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(Players, user_id)

@app.route("/")
def home():
    result = db.session.execute(db.select(Players).order_by(desc(Players.score)))
    players = result.scalars()
    return render_template("index.html",players=players)

@app.route("/login",methods=['GET','POST'])
def login():
    login_form = LogInForm()
    if login_form.validate_on_submit() and request.method == 'POST':
        #find user by name
        searched_user = db.session.execute(db.select(Players).where(Players.name == request.form.get("name"))).scalar()
        if searched_user and db.session.execute(db.select(Players).where(Players.email == searched_user.email)).scalar() and bcrypt.check_password_hash(searched_user.password.encode('utf-8'),request.form.get("password").encode('utf-8')):
            login_user(searched_user)
            return redirect(url_for('home'))

        if not searched_user:
            flash("That name does not exist, please try again.")
            return redirect(url_for('login'))

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
                             password=bcrypt.generate_password_hash(request.form.get("password"),12).decode('utf-8'),
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
    if request.method == 'POST': #First request can't be POST so that way we escape questions from doing 2 requests.
        user_answers = [request.form.get(f'answer{i}') for i in range(query_manager.amount)]
        correct_answers = [request.form.get(f"corrected_answer{z}") for z in range(query_manager.amount)]
        session_correct_answers = len([i for i in range(query_manager.amount) if user_answers[i] == correct_answers[i]])
        print(user_answers)
        print(correct_answers)
        if current_user.is_authenticated: #add answers in database and give back results
            quiz_score = Score(player_id=current_user.id, database=Players)
            quiz_score.update_db_answers(user_answers, session_correct_answers)
        return redirect(url_for('score',session=session_correct_answers,questions_amount=query_manager.amount))

    questions = query_manager.get_questions(type="cooking") # replace with
    return render_template("game.html", questions=questions)


@app.route("/player_score")
def score():
    return render_template("score.html",session=request.args.get("session"),ques_amount= request.args.get("questions_amount"))
