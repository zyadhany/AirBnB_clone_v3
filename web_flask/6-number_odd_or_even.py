#!/usr/bin/python3

""" Start with flask """

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def root():
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_fun(text):
    text = text.replace('_', ' ')
    return "C {}".format(text)


@app.route("/python/", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_cool(text='is cool'):
    text = text.replace('_', ' ')
    return "Python {}".format(text)


@app.route("/number/<int:n>", strict_slashes=False)
def n_number(n):
    return "{} is a number".format(n)


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    return render_template("5-number.html", num=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def number_odd_or_even(n):
    if n % 2 is 0:
        txt = 'even'
    else:
        txt = 'odd'

    return render_template("6-number_odd_or_even.html", num=n, type=txt)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
