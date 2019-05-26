from flask import render_template, url_for, request
from grand_py import app
from grand_py.forms import EntryForm
from grand_py.bot import Bot



@app.route("/")
@app.route("/home")
def home():
    #Main page with chat
    form = EntryForm()
    return render_template('grandpy.html', form=form)


@app.route("/bot", methods=['POST'])
def bot():
    #Used for bot questionning
    bot = Bot(request.form['text'])
    return bot.grandpyTalk()


