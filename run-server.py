#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#vi: set ai sta et ts=8 sts=4 sw=4 tw=79 wm=0 cc=+1 lbr fo=croq :
# Copyright (C) Nyimbi Odero,2022

"""A one line summary of the run-server

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

  Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""

__author__ = "nyimbi"
__contact__ = "nyimbi@gmail.com"
__copyright__ = "Copyright (c) 2022, nyimbi"
__date__ = "17/02/2022"
__created__ = "Thursday Feb 17, 2022 12:57:09 EAT"
__deprecated__ = False
__email__ =  "nyimbi@gmail.com"
__license__ = "MIT"
__maintainer__ = "nyimbi"
__status__ = "Production" # "Prototype", "Development", or "Production".
__version__ = "0.0.1"

from flask import Flask, render_template, send_from_directory, send_file
import folium
import pandas as pd
import sqlite3
from flask_htmlmin import HTMLMIN

app = Flask(__name__)
app.config['MINIFY_HTML'] = True
htmlmin = HTMLMIN(app)

# @app.route("/<state>")
# def index(state):
#      folium_map = init_map(str(state))
#      return folium_map._repr_html_()


@app.route("/<state>")
def review(state):
     print("rendering previously saved map")
     return send_file("pu_map_" + str(state)[0:4].upper() + ".html")


if __name__ == "__main__":
     app.run(debug=True)


