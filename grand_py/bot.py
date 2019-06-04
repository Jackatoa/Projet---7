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
        self.parsed_question = None
        self.cleaned_question = None
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
        """clean and return a string without separating special chars"""
        newquestion = self.question
        newquestion = newquestion.replace("'", ' ')
        newquestion = newquestion.replace("-", ' ')
        return newquestion

    def clean_question_from_list(self, lst):
        """clean the questions of indesirable characters"""
        list_question = self.question.split(" ")
        new_list_question = []
        for x in list_question:
            new_list_question.append(re.sub('[^A-Za-z0-9]+', '', x.lower()))
        new_list_question = [x for x in new_list_question if x.lower() not in lst]
        return ' '.join(new_list_question)

    def clean_question_for_search(self):
        """return the final searched words"""
        questioncleaned = self.parsed_question
        list_question = questioncleaned.split(" ")
        new_list_question = []
        for x in list_question:
            new_list_question.append(re.sub('[^A-Za-z0-9]+', '', x.lower()))
        new_list_question = [x for x in new_list_question if x.lower() not in p.adresslst]
        new_list_question = [x for x in new_list_question if x.lower() not in p.locationwords]
        new_list_question = [x for x in new_list_question if x.lower() not in p.wikilst]
        return ' '.join(new_list_question)

    def generate_questions(self):
        self.question = unidecode(self.question)
        self.question = self.clean_question_from_false_spaces()
        self.parsed_question = self.clean_question_from_list(p.stop_words)
        self.cleaned_question = self.clean_question_for_search()
        self.wikiquestion = Wiki(self.cleaned_question)
        self.mapquestion = Map(self.parsed_question, self.cleaned_question)

    def grandpyTalk(self):
        """main function of answer"""
        p.clean_countries()
        self.generate_questions()
        self.check_easy_answer()
        if self.answer is None:
            self.check_hard_answer()
            if self.answer is None:
                self.answer = a.random_answer(Answer.answer_too_old)
        return self.json_answer()

    def check_easy_answer(self):
        """check if the answer deserve a simple answer"""
        if self.question.isdigit():
            self.answer = a.get_stupid_answer(0)
        elif "merci" in self.question.lower():
            self.answer = a.get_stupid_answer(5)
        elif "bonjour" in self.question.lower():
            self.answer = a.random_answer(a.answer_hello)
        elif not re.search(r'[^.]', self.question):
            self.answer = a.get_stupid_answer(1)
        elif not re.search(r'[^!]', self.question):
            self.answer = a.get_stupid_answer(2)
        elif not re.search(r'[^zZ]', self.question):
            self.answer = a.get_stupid_answer(3)
        elif not re.search('[a-zA-Z]', self.question):
            self.answer = a.get_stupid_answer(4)
        elif self.cleaned_question == "":
            self.answer = a.random_answer(Answer.answer_too_old)


    def check_hard_answer(self):
        """check if the answer deserve a real search"""
        if self.cleaned_question in Parser.continentslst:
            self.zoom = 2
            self.mapquestion.location_exist(" continent")
            self.grandpy_find_location()
            self.get_wiki_for_location("continent ")
        elif self.cleaned_question in Parser.cleaned_countries:
            self.zoom = 4
            if self.question.lower() == "france":
                self.grandpy_find_location()
                self.get_wiki_for_location(" ")
            else:
                self.grandpy_find_location()
                self.get_wiki_for_location("Pays ")
        elif self.wikiquestion.exist() and self.check_wikiwords():
            self.wikiquestion.get_data()
            self.grandpy_find_wiki()
        elif self.check_adress() and self.mapquestion.adress_exist():
            self.grandpy_find_adress()
            self.zoom = 18
        elif self.mapquestion.location_exist(" "):
            self.grandpy_find_location()
            self.get_wiki_for_location(" ")
        elif self.mapquestion.location_exist(" France"):
            self.grandpy_find_location()
            self.get_wiki_for_location(" ")
        elif self.mapquestion.location_exist(" commune"):
            self.grandpy_find_location()
            self.get_wiki_for_location("commune ")
        elif self.mapquestion.adress_exist():
            self.grandpy_find_adress()

    def grandpy_find_location(self):
        """Set an answer with the google place api"""
        self.coord_lat = self.mapquestion.response.json()['results'][0]['geometry']['location'][
                                                            'lat']
        self.coord_long = self.mapquestion.response.json()['results'][0]['geometry']['location'][
            'lng']
        self.answer = a.random_answer(a.answer_location_find)
        self.map_answer = a.random_answer(a.answer_location_here)

    def grandpy_find_adress(self):
        """Set an answer with the google map api"""
        self.answer = a.random_answer(a.answer_location_find)
        self.map_answer = a.random_answer(a.answer_location_here)
        self.coord_lat = self.mapquestion.latitude
        self.coord_long = self.mapquestion.longitude

    def get_wiki_for_location(self, arg):
        """return a wiki answer with special arguments"""
        newquestion = arg + self.cleaned_question
        newwikiquestion = Wiki(newquestion)
        if newwikiquestion.exist():
            newwikiquestion.get_data()
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
        if any(word in self.parsed_question for word in Parser.adresslst):
            return True

    def check_location(self):
        """Check if the question contain a location type word"""
        if any(word in self.parsed_question for word in Parser.locationwords):
            return True

    def check_wikiwords(self):
        """Check if the question contain a wiki type word"""
        if any(word in self.parsed_question for word in Parser.wikilst):
            return True

p = Parser()
a = Answer()

