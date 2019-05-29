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
        self.parsedquestion = None
        self.cleanedquestion = None
        self.wikiquestion = None
        self.mapquestion = None
        self.zoom = 13
    def json_answer(self):
        """Check answer and return them in the json format"""
        if self.map_answer and self.wiki_answer:
            return jsonify({'answer'     : self.answer,
                            'wiki_answer': self.wiki_answer,
                            'map_answer' : self.map_answer,
                            'answer_lat' : self.coord_lat,
                            'answer_long': self.coord_long,
                            'zoom'       : self.zoom})
        elif self.map_answer:
            return jsonify({'answer'     : self.answer,
                            'map_answer' : self.map_answer,
                            'answer_lat' : self.coord_lat,
                            'answer_long': self.coord_long,
                            'zoom': self.zoom})
        elif self.wiki_answer:
            return jsonify({'answer': self.answer, 'wiki_answer': self.wiki_answer})
        else:
            return jsonify({'answer': self.answer})

    def clean_question_from_false_spaces(self):
        self.question = self.question.replace("'", ' ')
        self.question = self.question.replace("-", ' ')

    def clean_question_from_list(self, lst):
        """clean the questions of indesirable characters"""
        list_question = self.question.split(" ")
        new_list_question = []
        for x in list_question:
            new_list_question.append(re.sub('[^A-Za-z0-9]+', '', x.lower()))
        new_list_question = [x for x in new_list_question if x.lower() not in lst]
        return ' '.join(new_list_question)

    def clean_question_for_search(self):
        questioncleaned = self.parsedquestion
        list_question = questioncleaned.split(" ")
        new_list_question = []
        for x in list_question:
            new_list_question.append(re.sub('[^A-Za-z0-9]+', '', x.lower()))
        new_list_question = [x for x in new_list_question if x.lower() not in p.adresslst]
        new_list_question = [x for x in new_list_question if x.lower() not in p.locationwords]
        new_list_question = [x for x in new_list_question if x.lower() not in p.wikilst]
        self.cleanedquestion = ' '.join(new_list_question)

    def generate_questions(self):
        self.question = unidecode(self.question)
        self.clean_question_from_false_spaces()
        self.parsedquestion = self.clean_question_from_list(p.stop_words)
        self.clean_question_for_search()

    def grandpyTalk(self):
        p.clean_countries()
        self.generate_questions()
        self.wikiquestion = Wiki(self.cleanedquestion)
        self.mapquestion = Map(self.parsedquestion, self.cleanedquestion)
        print("question = {0}, parsedquestion = {1}, cleanedquestion = {2}".format(self.question,
                                                                                   self.parsedquestion,
                                                                                   self.cleanedquestion))
        if self.check_easy_answer():
            print("easy answer find")
        elif self.check_hard_answer():
            print("hard answer find")
        else:
            self.answer = a.random_answer(Answer.answer_too_old)
        return self.json_answer()

    def check_easy_answer(self):
        if self.question.isdigit():
            self.answer = a.get_stupid_answer(0)
            return True
        elif "merci" in self.question.lower():
            self.answer = a.get_stupid_answer(5)
            return True
        elif not re.search(r'[^.]', self.question):
            self.answer = a.get_stupid_answer(1)
            return True
        elif not re.search(r'[^!]', self.question):
            self.answer = a.get_stupid_answer(2)
            return True
        elif not re.search(r'[^zZ]', self.question):
            self.answer = a.get_stupid_answer(3)
            return True
        elif not re.search('[a-zA-Z]', self.question):
            self.answer = a.get_stupid_answer(4)
            return True
    def Get_caps_for_wiki(self):
        wordslst = self.cleanedquestion.split()
        newwordslst = []
        for x in wordslst:
            newwordslst.append(x.capitalize())
        self.cleanedquestion = ' '.join(newwordslst)

    def check_hard_answer(self):
        if self.cleanedquestion in Parser.cleaned_countries:
            self.zoom = 4
            if self.question.lower() == "france":
                self.grandpy_find_location()
                self.get_wiki_for_location(" ")
            else:
                self.grandpy_find_location()
                self.get_wiki_for_location("Pays ")
            return True
        elif self.wikiquestion.exist() and self.check_wikiwords():
            self.grandpy_find_wiki()
            return True
        elif self.check_adress() and self.mapquestion.adress_exist():
            self.grandpy_find_adress()
            self.zoom = 18
            return True
        elif self.mapquestion.location_exist(" "):
            self.grandpy_find_location()
            self.get_wiki_for_location(" ")
            return True
        elif self.mapquestion.location_exist(" France"):
            self.grandpy_find_location()
            self.get_wiki_for_location(" ")
            return True
        elif self.mapquestion.location_exist(" commune"):
            self.grandpy_find_location()
            self.get_wiki_for_location("commune ")
            return True
        elif self.mapquestion.adress_exist():
            self.grandpy_find_adress()
            return True

    def grandpy_find_location(self):
        """Return an answer with the google place api"""
        self.coord_lat = self.mapquestion.response['results'][0]['geometry']['location']['lat']
        self.coord_long = self.mapquestion.response['results'][0]['geometry']['location']['lng']
        self.answer = a.random_answer(a.answer_location_find)
        self.map_answer = a.random_answer(a.answer_location_here)

    def grandpy_find_adress(self):
        """Return an answer with the google map api"""
        self.answer = a.random_answer(a.answer_location_find)
        self.map_answer = a.random_answer(a.answer_location_here)
        self.coord_lat = self.mapquestion.latitude
        self.coord_long = self.mapquestion.longitude

    def get_wiki_for_location(self, arg):
        newquestion = arg + self.cleanedquestion
        newwikiquestion = Wiki(newquestion)
        if newwikiquestion.exist():
            self.wiki_answer = newwikiquestion.getSummary()

    def grandpy_find_wiki(self):
        """Return an answer with the wiki api"""
        self.answer = a.random_answer(a.answer_wiki_find)
        if self.wikiquestion.is_location():
            self.map_answer = a.random_answer(a.answer_location_here)
            self.coord_lat = self.wikiquestion.lat
            self.coord_long = self.wikiquestion.long
            self.wiki_answer = self.wikiquestion.getSummary()
        else:
            self.wiki_answer = self.wikiquestion.getSummary()

    def check_adress(self):
        """Check if the question contain an adress type word"""
        if any(word in self.parsedquestion for word in Parser.adresslst):
            return True

    def check_location(self):
        """Check if the question contain a location type word"""
        if any(word in self.parsedquestion for word in Parser.locationwords):
            return True

    def check_wikiwords(self):
        """Check if the question contain a wiki type word"""
        if any(word in self.parsedquestion for word in Parser.wikilst):
            return True


p = Parser()
a = Answer()

