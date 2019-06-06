# GrandPy - Bot

Grandpy-Bot est un bot qui émule un chat avec un grand-père qui s'y connaît à fond en géographie et en culture générale, n'hésitez pas à lui parler ou lui demander des adresses il a beaucoup voyagé !

### Prérequis

Tout les dépendances sont dans le fichier requirements.txt.

```
$ pip install -r requirements.txt
```

### Utilisation

Vous pouvez questionner GrandPy ici : https://grandpapy-bot.herokuapp.com

GrandPy utilise un algorithme qui tente de comprendre au mieux votre message, cependant il parle principalement un français correct sans trop de fautes d'orthographe et aura donc du mal avec votre langage SMS habituel ! Il a beau savoir utiliser un ordinateur comme un chef il préfererait que vous utiliser un langage correct !

```
Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms ?
```

Retournera des informations sur OpenClassrooms venant de wikipedia et une carte affichant sa position !

```
Sais tu où se trouve le Louvre ?
```

Retournera des informations sur le Louvre venant de wikipedia et une carte affichant sa position !

## Faire tourner le code soi même

Pour pouvoir utiliser GrandPy depuis un autre site que Heroku vous aurez besoin d'une clé Google Api.
Créez un fichier config.py dans le dossier grand_py/ spécifiant une clé api Google et une clé secrète pour Flask.

```
config.py

GOOGLE_API_KEY = 'YOUR_GOOGLE_API_KEY'
SECRET_KEY = 'YOUR_SECRET_KEY'
```

## Créé avec

* [Flask](http://flask.pocoo.org) - A Python Microframework
* [GoogleMaps](https://www.google.com/maps/) - Google Maps & Google Place
* [MediaWiki](https://www.mediawiki.org/wiki/MediaWiki/fr) - Wikimedia Collaboration Platform

## Auteur

* **Xavier Endres** 



