from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '56b82bea9531852b03bcc074e967a446'
from grand_py import routes
