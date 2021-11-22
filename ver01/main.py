from flask import *
app = Flask(__name__)
#import functions.py
import collections
import nltk
from nltk import ngrams
import csv
import pprint
import random
from nltk.corpus import wordnet as wn
nltk.download('wordnet')
nltk.download('punkt')

def create_n_gram(seq,n):
    return list(ngrams(seq,n))

def test_function():
    return "return text from test_function()"



@app.route('/')
def hello():
    name = "Hoge"
    #return name
    return render_template('hello.html', title='flask test', name=name)

@app.route('/good')
def good():
    name = test_function()
    return name

@app.route('/user/<username>')
def show_user_profile(username):
    return 'User %s' % username

@app.route('/input')
def input_values():
    #return "input test"
    return render_template('input.html', title="input test", name="input_values")

@app.route('/show', methods=["post"])
def show_text():
    #input_values=request.form.get("value")
    input_name=request.form.get("name")
    input_month_list=request.form.getlist("month")
    input_value_list=request.form.getlist("value")
    print(input_name)
    print(input_month_list)
    print(input_value_list)

    input_text = request.form.get("test_a")
    
    n = 2
    morph = nltk.word_tokenize(input_text)
    result = create_n_gram(morph, n)
    #return "show test"
    return render_template('show.html', title="show test", name="show_name", result=result)
    #return 'input_text: %s' % input_text

if __name__ == "_main_":
    app.run(debug=True)