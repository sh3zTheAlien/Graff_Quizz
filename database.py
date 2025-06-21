from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_login import UserMixin

class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)

class Players(UserMixin,db.Model):
    __tablename__ = "players"
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    name: Mapped[str] = mapped_column(String,nullable=False)
    email: Mapped[str] = mapped_column(String,nullable=False,unique=True)
    password: Mapped[str] = mapped_column(String,nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    answered_questions: Mapped[int] = mapped_column(Integer, nullable=False)
    correct_answers: Mapped[int] = mapped_column(Integer, nullable=False)
    false_answers: Mapped[int] = mapped_column(Integer, nullable=False)

# class QuestionsTF(db.Model):
#     __tablename__ = "questions_tf"
#     id: Mapped[int] = mapped_column(Integer,primary_key=True)
#     question : Mapped[str] = mapped_column(String,nullable=False)
#     correct_answer : Mapped[str] = mapped_column(String,nullable=False)