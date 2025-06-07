import requests
import html

#hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
#is_valid = bcrypt.check_password_hash(hashed_password, 'password')

resp = requests.get("https://opentdb.com/api.php?amount=10&category=9&difficulty=medium&type=boolean").json()
for i in resp["results"]:
    print(i["question"])

class Score:

    def __init__(self):
        self.correct_answers = 0 #Get From DB
        self.false_answers = 0 #Get From DB
        self.all_answers = 0 #Get From DB
        self.average = 0 #Get From DB

    def count_score(self,user_answer,correct_answer):
        self.all_answers += 1

        if user_answer == correct_answer:
            self.correct_answers += 1 #Add in DB

        self.false_answers = self.all_answers - self.correct_answers
        self.average = self.correct_answers / self.all_answers
        return {"Average: ":self.average, "Correct: ":self.correct_answers, "False: ":self.false_answers}

