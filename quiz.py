from database import db
import json
from random import *

class Questions:

    def __init__(self,amount,difficulty,question_type,category):
        """ type: 'bool' or 'multiple'
            difficulty: 'easy' or 'medium' or 'hard'
            amount: a number between 1 - 40
            (questions)category: a number (video-games:15,sports:21,computers:18,general:9)"""
        self.amount = amount
        self.difficulty = difficulty
        self.question_type = question_type
        self.category = category

    def get_questions(self):
        with open('data.json', 'r') as data_file:
            questions = []
            data = json.load(data_file)
            # 401 is the len() of questions the json file has and 5 the questions presented.
            # In future it will be estimated by amount of questions that the user has chosen to answer
            random_nums = sample(range(0, 180), 5)
            for index, num in enumerate(random_nums):
                question = data["general"][num]["question"]
                correct_answer = data["general"][num]["correct_answer"]
                questions.append({"question": question,
                                  "correct_answer": correct_answer})
            return questions

#input for class score: current_player.id and db(Players)
class Score:

    def __init__(self,player_id,database):
        self.player_id = player_id
        self.database = database
        self.player = db.session.execute(db.select(self.database).where(self.database.id == self.player_id)).scalar()
        self.score = self.player.score
        self.correct_answers = self.player.correct_answers
        self.answered_questions = self.player.answered_questions
        self.false_answers = self.player.false_answers

    def update_db_answers(self,user_ans,session_correct_ans):

        self.correct_answers += session_correct_ans
        self.answered_questions += len(user_ans)
        #score is depended on the NEW values of answered_questions and correct_answers
        self.score = (self.correct_answers/self.answered_questions) * 100
        self.false_answers += self.answered_questions - self.correct_answers

        player_to_update = self.player
        player_to_update.score = round(self.score,2)
        player_to_update.answered_questions = self.answered_questions
        player_to_update.correct_answers = self.correct_answers
        player_to_update.false_answers = self.false_answers
        return db.session.commit()