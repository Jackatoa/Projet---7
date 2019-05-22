from flask import jsonify
import re

class Bot:
    def __init__(self, question):
        self.answer = None
        self.wiki_answer = None
        self.map_answer = None
        self.question = question

    def json_answer(self):
        if self.wiki_answer and self.map_answer:
            return jsonify({'answer': self.answer, 'wiki_answer': self.wiki_answer,
                            'map_answer': self.map_answer})
        elif self.wiki_answer:
            return jsonify({'answer': self.answer, 'wiki_answer': self.wiki_answer})
        else:
            return jsonify({'answer': self.answer})

    def grandpyTalk(self):
        if self.big_check():
            return self.json_answer()
        else:
            self.answer = "Ce message est passé"
            return self.json_answer()

    def big_check(self):
        if self.question.isdigit():
            self.answer = "Tu es bon en algèbre mon petit !"
            return True
        elif not re.search(r'[^.]', self.question):
            self.answer = "Tu es bien silencieux mon petit !"
            return True
        elif not re.search(r'[^zZ]', self.question):
            self.answer = "Réveille toi mon petit !"
            return True
        elif not self.question.isupper() and not self.question.islower():
            self.answer = "Arrête de grommeler mon petit !"
            return True
        else:
            self.search_question()

    def search_question(self):
        pass

