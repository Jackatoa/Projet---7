from flask import render_template, url_for, redirect, request, jsonify
from grand_py import app
from grand_py.forms import EntryForm
from grand_py.bot import Bot



@app.route("/")
@app.route("/home")
def home():
    form = EntryForm()
    return render_template('grandpy.html', form=form)


@app.route("/bot", methods=['POST'])
def bot():
    bot = Bot()
    return jsonify({'answer':
                    bot.testtalk(request.form['text'])})

