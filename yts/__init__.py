#!/usr/bin/env python3

import os
from flask import Flask, render_template


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def main():
        return(
            render_template('index.html')
        )

    from . import movie
    app.register_blueprint(movie.bp)

    from . import api
    app.register_blueprint(api.bp)

    return(app)
