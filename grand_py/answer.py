

class Answer():
    answer_stupid = ["Tu es bon en algèbre mon petit !", "Tu es bien silencieux mon petit !",
                     "Ne soit pas interloqué mon petit !", "Réveille toi mon petit !", "Arrête de grommeler mon petit !"]
    answer_error = ["reponse erreur"]
    answer_wiki_find = ["page wiki trouvee"]
    answer_location_find = ["endroit trouvé"]

    def __init__(self):
        pass

    def get_stupid_answer(self, number):
        return Answer.answer_stupid[number]

    def get_error_answer(self):
        return Answer.answer_error[0]

    def get_wiki_answer(self):
        return Answer.answer_wiki_find[0]

    def get_location_answer(self):
        return Answer.answer_location_find[0]
