#!/usr/bin/python3
"""
Module to start a Flask web application
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    """Displays a HTML page with a list of states or cities of a spec state"""
    states = storage.all(State).values()
    if id:
        state = None
        for s in states:
            if s.id == id:
                state = s
                break
        if not state:
            return render_template('9-not_found.html')
        return render_template('9-state.html', state=state)
    return render_template('9-states.html', states=states)


@app.teardown_appcontext
def teardown_db(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
