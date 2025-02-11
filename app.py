from flask import *

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html", username="Worthy")


@app.route('/about')
def about():
    return render_template("about.html")


app.run()
