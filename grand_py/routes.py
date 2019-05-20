from flask import render_template, url_for, redirect, request
from grand_py import app
from grand_py.forms import EntryForm



@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = EntryForm()
    return render_template('grandpy.html', form=form)


@app.route("/about")
def about():
    return render_template('grandpy.html', title='About')

