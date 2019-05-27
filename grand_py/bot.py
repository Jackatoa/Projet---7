from flask import jsonify
import re
from grand_py.wiki import Wiki
from grand_py.answer import Answer
from grand_py.map import Map
from grand_py.parser import Parser
from unidecode import unidecode

class Bot:
    """Contains main algorithms for the application"""
    def __init__(self, question):
        self.answer = None
        self.wiki_answer = None
        self.map_answer = None
        self.coord_lat = None
        self.coord_long = None
        self.question = question
        self.wikiquestion = None
        self.mapquestion = None

    def json_answer(self):
        """Check answer and return them in the json format"""
        if self.map_answer and self.wiki_answer:
            return jsonify({'answer'     : self.answer,
                            'wiki_answer': self.wiki_answer,
                            'map_answer' : self.map_answer,
                            'answer_lat' : self.coord_lat,
                            'answer_long': self.coord_long})
        elif self.map_answer:
            return jsonify({'answer'     : self.answer,
                            'map_answer' : self.map_answer,
                            'answer_lat' : self.coord_lat,
                            'answer_long': self.coord_long})
        elif self.wiki_answer:
            return jsonify({'answer': self.answer, 'wiki_answer': self.wiki_answer})
        else:
            return jsonify({'answer': self.answer})

    def grandpyTalk(self):
        """Main function for grandpy answer"""
        if self.big_check():
            return self.json_answer()
        else:
            self.question = unidecode(self.question)
            self.question = self.clean_question(Parser.stop_words)
            self.wikiquestion = Wiki(self.clean_question(Parser.locationwords))
            self.mapquestion = Map(self.question, self.clean_question(Parser.locationwords))
            print(self.question)
            self.grandpy_try()
            return self.json_answer()

    def clean_question(self, lst):
        """clean the questions of indesirable characters"""
        self.question = self.question.replace("'", ' ')
        list_question = self.question.split(" ")
        new_list_question = []
        for x in list_question:
            new_list_question.append(re.sub('[^A-Za-z0-9]+', '', x.lower()))
        new_list_question = [x for x in new_list_question if x.lower() not in lst]
        return ' '.join(new_list_question)

    def big_check(self):
        """Check if the user input deserve a simple answer"""
        self.answer = Answer()
        print("big check question {0}".format(self.question))
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
        print(self.question)
        """Check which style of answer should be choosen"""
        if self.check_adress() and self.mapquestion.adress_exist():
            print("check adresse + adress_exist")
            self.grandpy_find_adress()
        elif any(word in self.question.split() for word in Parser.locationwords) and \
                self.mapquestion.location_exist():
            print("locationwords + location_exist")
            self.grandpy_find_location()
        elif self.wikiquestion.exist():
            print("wiki exist")
            self.grandpy_find_wiki()
        else:
            self.answer = self.answer.get_old_answer()

    def check_adress(self):
        """Check if the question contain an adress type word"""
        if any(word in self.question for word in Parser.adresslst):
            return True

    def grandpy_find_adress(self):
        """Return an answer with the google map api"""
        self.answer = a.random_answer(a.answer_location_find)
        self.map_answer = a.random_answer(a.answer_location_here)
        self.coord_lat = self.mapquestion.latitude
        self.coord_long = self.mapquestion.longitude
        return self.json_answer()

    def grandpy_find_wiki(self):
        """Return an answer with the wiki api"""
        self.answer = a.random_answer(a.answer_wiki_find)
        if self.wikiquestion.is_location():
            print("wiki + LOCATION")
            self.map_answer = a.random_answer(a.answer_location_here)
            self.coord_lat = self.wikiquestion.lat
            self.coord_long = self.wikiquestion.long
            self.wiki_answer = self.wikiquestion.getSummary()
            return self.json_answer()
        else:
            print("WIKI SANS LOCATION")
            self.wiki_answer = self.wikiquestion.getSummary()
            return self.json_answer()

    def grandpy_find_location(self):
        """Return an answer with the google place api"""
        self.coord_lat = self.mapquestion.response['results'][0]['geometry']['location'][
            'lat']
        self.coord_long = self.mapquestion.response['results'][0]['geometry']['location'][
            'lng']
        self.answer = a.random_answer(a.answer_location_find)
        self.map_answer = a.random_answer(a.answer_location_here)
        if self.wikiquestion.exist():
            self.wiki_answer = self.wikiquestion.getSummary()
        return self.json_answer()

a = Answer()
