class Answer():
    answer_stupid = ["Tu es bon en algèbre mon petit !", "Tu es bien silencieux mon petit !",
                     "Ne soit pas interloqué mon petit !", "Réveille toi mon petit !",
                     "Arrête de grommeler mon petit !", "Mais de rien mon petit !"]
    answer_error = ["reponse erreur"]
    answer_wiki_find = ["page wiki trouvee"]
    answer_location_find = ["endroit trouvé"]
    answer_too_old = ["Tu sais je suis un peu dépassé avec les termes que vous employez vous " \
                      "les jeunes. Ne voudrais pas tu partager un werther's original plutôt ?"]

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

    def get_old_answer(self):
        return Answer.answer_too_old[0]
