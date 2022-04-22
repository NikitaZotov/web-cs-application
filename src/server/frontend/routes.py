"""
    Author Zotov Nikita
"""

from flask import render_template, request, flash, redirect, url_for

from server.frontend.app import Application
from server.frontend.configurator import Configurator

configurator = Configurator()
app = Application(configurator)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/input', methods=('GET', 'POST'))
def input_text():
    if request.method == 'POST':
        article = request.form['title']
        text = request.form['content']

        if not article:
            flash('Article is required!')
        else:
            return redirect(url_for('index'))

    return render_template('input.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html", error=error), 500

