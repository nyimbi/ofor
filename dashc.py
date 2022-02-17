#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vi: set ai sta et ts=8 sts=4 sw=4 tw=79 wm=0 cc=+1 lbr fo=croq :
# Copyright (C) Nyimbi Odero,2022

"""A one line summary of the dashc

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
__date__ = "08/02/2022"
__created__ = "Tuesday Feb 08, 2022 10:13:58 EAT"
__deprecated__ = False
__email__ = "nyimbi@gmail.com"
__license__ = "MIT"
__maintainer__ = "nyimbi"
__status__ = "Prototype"  # , "Development", or "Production".
__version__ = "0.0.1"

from flask import Flask, render_template, send_from_directory, send_file
import folium
import pandas as pd
import sqlite3
from flask_htmlmin import HTMLMIN

states = [
    "ABIA",
    "ADAMAWA",
    "AKWA IBOM",
    "ANAMBRA",
    "BAUCHI",
    "BAYELSA",
    "BENUE",
    "BORNO",
    "CROSS RIVER",
    "DELTA",
    "EBONYI",
    "EDO",
    "EKITI",
    "ENUGU",
    "FCT",
    "GOMBE",
    "IMO",
    "JIGAWA",
    "KADUNA",
    "KANO",
    "KATSINA",
    "KEBBI",
    "KOGI",
    "KWARA",
    "LAGOS",
    "NASARAWA",
    "NIGER",
    "OGUN",
    "ONDO",
    "OSUN",
    "OYO",
    "PLATEAU",
    "RIVERS",
    "SOKOTO",
    "TARABA",
    "YOBE",
    "ZAMFARA",
]


abv_coords = (9.083587, 7.467892)
con = sqlite3.connect("pu.db")
cur = con.cursor()
cur.execute("select * from pu")

app = Flask(__name__)
app.config['MINIFY_HTML'] = True
htmlmin = HTMLMIN(app)

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def load_excel(workbook):
    try:
        con = sqlite3.connect("pu.db")
        cur = con.cursor()

        cur.execute(
            """
            create table pu(
             pu_loc_id text,
             state text,
             lga text,
             ra text,
             pu text,
             bld_type text,
             lat text,
             lng text,
             plna text,
             pu_loc_desc text
             state_name text);
          """
        )

        for state in states:
            print(state)
            st = pd.read_excel(workbook, header=0, sheet_name=state)
            st["state_name"] = state  # we add the state_name to the datase
            st1 = st.dropna()
            st1.to_sql("pu", con, if_exists="append", index=False)
    finally:
        con.close()


def init_map(s_name):
    i = 0
    print(s_name)
    con = sqlite3.connect("npu.db")
    cur = con.cursor()
    s = (
        "select avg(lat),avg(lng) from pu where state_name like "
        + s_name[0:4].upper()
        + "%"
    )
    cur.execute(
        "select avg(lat),avg(lng) from pu where state_name like :state",
        {"state": s_name[0:4].upper() + "%"},
    )
    (glat, glng) = cur.fetchone()
    map = folium.Map(location=(glat, glng), zoom_start=10, tiles="Stamen Terrain")
    try:
        for row in cur.execute(
            "select * from pu where state_name like :state",
            {"state": s_name[0:4].upper() + "%"},
        ).fetchall():
            i = i + 1
            if i > 10000:
                break
            # print(row[6], row[7])
            if isfloat(row[6]) and isfloat(row[7]):
                folium.Circle(
                    radius=10,
                    color="#3186cc",
                    fill=False,
                    location=[row[6], row[7]],
                    popup=row[9],
                    tooltip=f"<b>{row[0]}</b> <br> {row[1]}, {row[2]}, {row[3]}",
                ).add_to(map)
            else:
                print(row)
    finally:
        print(i)
        map.save("pu_map_" + s_name[0:4] + ".html")
        con.close()
    return map


@app.route("/make_maps")
def make_maps():
    for state in states:
        init_map(state)


@app.route("/<state>")
def index(state):
    folium_map = init_map(str(state))
    return folium_map._repr_html_()


@app.route("/review/<state>")
def review(state):
    print("rendering previously saved map")
    return send_file("pu_map_" + str(state)[0:4].upper() + ".html")


if __name__ == "__main__":
    app.run(debug=True)
