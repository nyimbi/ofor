#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#vi: set ai sta et ts=8 sts=4 sw=4 tw=79 wm=0 cc=+1 lbr fo=croq :
# Copyright (C) Nyimbi Odero,2022

"""A one line summary of the dashb

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
__date__ = "07/02/2022"
__created__ = "Monday Feb 07, 2022 22:08:35 EAT"
__deprecated__ = False
__email__ =  "nyimbi@gmail.com"
__license__ = "MIT"
__maintainer__ = "nyimbi"
__status__ = "Production" # "Prototype", "Development", or "Production".
__version__ = "0.0.1"

import pandas as pd
import numpy as np
import geoviews as gv
from geoviews import opts, dim
import geoviews.tile_sources as gvts
import param, panel as pn
gv.extension('bokeh')
import sqlite3
from bokeh.models import HoverTool


states = ['ABIA','ADAMAWA','AKWA IBOM','ANAMBRA','BAUCHI','BAYELSA','BENUE',
'BORNO','CROSS RIVER','DELTA','EBONYI','EDO','EKITI','ENUGU','FCT','GOMBE','IMO','JIGAWA','KADUNA','KANO','KATSINA','KEBBI','KOGI','KWARA','LAGOS','NASARAWA','NIGER','OGUN','ONDO','OSUN','OYO','PLATEAU','RIVERS','SOKOTO','TARABA','YOBE','ZAMFARA']

tooltips = [
    ('State', @state),
    ('LGA', @lga),
    ('PU', @pu),
    ('Longitude', @lng),
    ('Latitude', @lat)
]

topts = dict(width=1100, height=680, xaxis=None, yaxis=None, show_grid=False)




con = sqlite3.connect("pus.db")
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
    pu_loc_desc text);
 """)



for state in states:
    print(state)
    st = pd.read_excel('pu1.xlsx', header=0, sheet_name=state)
    st.to_sql('pu', con, if_exists='append', index=False)

df = pd.read_sql_query("SELECT * from pu", con)
print(df.head())




