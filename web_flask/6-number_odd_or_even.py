#!/usr/bin/python3
"""Starts a Flask web application.

The application listens on 0.0.0.0, port 5000.
Routes:
/: display “Hello HBNB!”
/hbnb: display “HBNB”
/c/<text>: display “C ” followed by the value of the text variable
(replace underscore _ symbols with a space)
/python/(<text>): display “Python ” followed by the value of the text
variable (replace underscore _ symbols with a space). The default
value of text is “is cool”
/number/<n>: display “n is a number” only if n is an integer
/number_template/<n>: display a HTML page only if n is an integer
/number_odd_or_even/<n>: display a HTML page only if n is an integer:
H1 tag: “Number: n is even|odd” inside the tag BODY
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Displays 'Hello HBNB!'"""
    return ("Hello HBNB!")


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Displays 'HBNB'"""
    return ("HBNB")


@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text):
    """Displays 'C ' followed by the value of the text variable."""
    return ("C " + text.replace('_', ' '))


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_is_cool(text):
    """Displays 'Python ' followed by the value of the text variable."""
    return ("Python " + text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """Displays 'n is a number' only if n is an integer."""
    return ("{} is a number".format(n))


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """Displays a HTML page only if n is an integer."""
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """Displays a HTML page only if n is an integer."""
    odd_or_even = "even" if n % 2 == 0 else "odd"
    return render_template(
        '6-number_odd_or_even.html', n=n, odd_or_even=odd_or_even)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
