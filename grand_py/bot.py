from flask import jsonify
import re
from grand_py.wiki import Wiki
from grand_py.answer import Answer
from grand_py.map import Map
from grand_py.parser import Parser

class Bot:
    def __init__(self, question):
        self.answer = None
        self.wiki_answer = None
        self.map_answer = None
        self.coord_lat = None
        self.coord_long = None
        self.question = question

    def json_answer(self):
        if self.map_answer and self.wiki_answer:
            return jsonify({'answer': self.answer,
                            'wiki_answer': self.wiki_answer,
                            'map_answer': self.map_answer,
                            'answer_lat': self.coord_lat,
                            'answer_long': self.coord_long})
        elif self.map_answer:
            return jsonify({'answer': self.answer,
                            'map_answer': self.map_answer,
                            'answer_lat': self.coord_lat,
                            'answer_long': self.coord_long})
        elif self.wiki_answer:
            return jsonify({'answer': self.answer, 'wiki_answer': self.wiki_answer})
        else:
            return jsonify({'answer': self.answer})

    def grandpyTalk(self):
        if self.big_check():
            return self.json_answer()
        else:
            self.clean_question()
            self.grandpy_try()
            return self.json_answer()

    def clean_question(self):
        list_question = self.question.split(" ")
        new_list_question = [x for x in list_question if x not in Parser.stop_words]
        self.question = ' '.join(new_list_question)

    def big_check(self):
        self.answer = Answer()
        if self.question.isdigit():
            self.answer = self.answer.get_stupid_answer(0)
            return True
        elif "merci" in self.question.lower():
            self.answer = self.answer.get_stupid_answer(5)
            return True
        elif not re.search(r'[^.]', self.question):
            self.answer = self.answer.get_stupid_answer(1)
            return True
        elif not re.search(r'[^!]', self.question):
            self.answer = self.answer.get_stupid_answer(2)
            return True
        elif not re.search(r'[^zZ]', self.question):
            self.answer = self.answer.get_stupid_answer(3)
            return True
        elif not re.search('[a-zA-Z]', self.question):
            self.answer = self.answer.get_stupid_answer(4)
            return True
        else:
            return False

    def grandpy_try(self):
        wikianswer = Wiki(self.question)
        streetanswer = Map(self.question)
        if self.check_adress() and streetanswer.exist():
            self.grandpy_find_adress(streetanswer)
        elif any(word in self.question for word in Parser.locationwords):
            self.grandpy_find_location()
        elif wikianswer.exist():
            self.grandpy_find_wiki(wikianswer)
        else:
            self.answer = self.answer.get_old_answer(0)

    def check_adress(self):
        if any(word in self.question for word in Parser.adresslst):
            return True

    def grandpy_find_adress(self, streetanswer):
            self.answer = "Je connais cet endroit, il est juste ici :"
            self.map_answer = "INFOS OPEN STREET MAP"
            self.coord_lat = streetanswer.latitude
            self.coord_long = streetanswer.longitude
            return self.json_answer()

    def grandpy_find_wiki(self, wikianswer):
        self.answer = "Je peux te dire beaucoup sur ce sujet "
        if wikianswer.is_location():
            self.map_answer = "Voilà son emplacement :"
            self.coord_lat = wikianswer.lat
            self.coord_long = wikianswer.long
            self.wiki_answer = wikianswer.getSummary()
            return self.json_answer()
        else:
            self.wiki_answer = wikianswer.getSummary()
            return self.json_answer()

    def grandpy_find_location(self):
        pass
