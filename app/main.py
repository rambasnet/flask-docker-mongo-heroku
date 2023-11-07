"""
This is the main file of the Flask application.
"""

import os
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def home() -> str:
    """Home page of the application.

    Returns:
        str: HTML page using Jinja2 template.
    """
    return render_template('index.html')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5555))
    app.run(debug=True, host='0.0.0.0', port=port)
