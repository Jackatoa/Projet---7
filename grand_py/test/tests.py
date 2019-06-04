import unittest
from grand_py.bot import Bot
from grand_py.parser import Parser


class BotTests(unittest.TestCase):

    def test_space_clean(self):
        element = b.clean_question_from_false_spaces()
        assert element == "Salut GrandPy ! Est ce que tu connaîs l adresse d OpenClassroomsé et de Saint Etienne?"

    def test_clean_from_lst(self):
        element = b.clean_question_from_list(p.stop_words)
        assert element == " connas ladresse dopenclassrooms saintetienne"

    def test_final_clean(self):
        element = b.clean_question_for_search()
        assert element == "openclassrooms saint etienne"

    def test_false_easy_answer(self):
        element = b.check_easy_answer()
        assert element is None

    def test_true_easy_answer(self):
        c = Bot("123456")
        d = Bot("zzzzzzzZZZZZzzzz")
        e = Bot("salut wesh merci pomme de terre")
        f = Bot("*!:;,?^*")
        c = c.check_easy_answer()
        d = d.check_easy_answer()
        e = e.check_easy_answer()
        f = f.check_easy_answer()
        assert c == d == e == f is True

    def test_lst_location(self):
        element = b.check_location()
        assert element is True

p = Parser
b = Bot("Salut GrandPy ! Est-ce que tu connaîs l'adresse d'OpenClassroomsé et de Saint-Etienne?")
b.answer = "Basic Answer"
b.wiki_answer = "Article extract"
b.map_answer = "Map found"
b.coord_lat = "12,12"
b.coord_long = "34,34"
b.parsed_question = "connais adresse openclassrooms saint etienne"
b.cleaned_question = "openclassrooms france"
b.wikiquestion = None
b.mapquestion = None
b.zoom = 13


