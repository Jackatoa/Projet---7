import random

class Answer():
    """Contains all the answer"""
    answer_stupid = ["Tu es bon en algèbre mon petit !", "Tu es bien silencieux mon petit !",
                     "Ne soit pas interloqué mon petit !", "Réveille toi mon petit !",
                     "Arrête de grommeler mon petit !", "Mais de rien mon petit !"]
    answer_wiki_find = ["J'en ai déjà entendu parler.", "Je connais parfaitement ce sujet !",
                        "Je l'ai vu à la télé."]
    answer_location_find = ["C'est un endroit magnifique !", "J'y ai été quand j'étais jeune.",
                            "J'y passe tout mes dimanches !"]
    answer_too_old = ["Tu sais je suis un peu dépassé avec les termes que vous employez vous " \
                      "les jeunes. Ne voudrais pas tu partager un werther's original plutôt ?",
                      "Je suis trés impréssionné par ta maîtrise de ce langage, mais je n'y "
                      "comprends rien.", "Ce n'est pas avec ça qu'on invoque Cthulu ?"]
    answer_location_here = ["Ca se trouve juste ici :", "Ca se trouve juste là :"]

    def get_stupid_answer(self, number):
        """Return a classic answer"""
        return Answer.answer_stupid[number]

    def random_answer(self, list):
        """Return a random answer"""
        return random.choice(list)
