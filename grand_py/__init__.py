from flask import Flask
from grand_py.config import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
from grand_py import routes
