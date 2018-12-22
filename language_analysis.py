
# coding: utf-8

# Import dependencies
import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

from pprint import pprint

# data base setup from main file
#################################################
# Database Setup
#################################################
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/developers.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Survey = Base.classes.survey

def languageAnalysis():

    # find devtypes, languageworkedwith, databaseworkedwith, frameworkWorkededWith
    s = [Survey.Respondent,
        Survey.DevType,
        Survey.LanguageWorkedWith,
        Survey.DatabaseWorkedWith,
        Survey.FrameworkWorkedWith
        ]

    radarResults = db.session.query(*s).all()

    # put results into pandas
    df = pd.DataFrame(radarResults)
    df.head()

    # explode the devtype column so there's only one devtype for each row
    expdev_df = pd.DataFrame(df.DevType.str.split(';').tolist(), index=[df.Respondent, df.LanguageWorkedWith, df.DatabaseWorkedWith, df.FrameworkWorkedWith]).stack()

    expdev_df = expdev_df.reset_index()

    expdev_df = expdev_df.rename(columns={0:'DevType'})
    expdev_df = expdev_df.drop(columns='level_4')

    expdev_df.head()

    expdev_df['LanguageList'] = expdev_df.LanguageWorkedWith.str.split(';')
    expdev_df.head()

    # hard code top 10 languages from stack ooverflow website
    topLang = ['JavaScript', 'HTML', 'CSS', 'SQL', 'Java', 'Bash/Shell', 'Python', 'C#', 'PHP', 'C++']

    expdev_df.head()

    # Loop through languages and count when a developer knows them
    for language in topLang:
        
        # dynamically create new column headers
        print('Checking for: ' + language + '...')        
        
        # Create new column to check if the respondent knows a language. If the languege is in the list of known languages, it gets 1, else it gets 0
        expdev_df[language] = np.where(expdev_df.LanguageList.apply(lambda x: language in x), 1, 0)
        
        print(f'{language} done!')

    # Aggregation by mean gives a fraction of dev types who know each skill
    langByDev = expdev_df.groupby('DevType').mean()
    langByDev = langByDev.drop(index='', columns='Respondent')

    # multiply all columns by 100 to make it a percntage
    langByDev.loc[:] *= 100

    # Round each percent to 2 decimals
    langByDev = langByDev.round(decimals=2)

    # Print to verify
    langByDev

    # Convert df to dict to serve as json. Orient by index to make it easily searchable by devtype
    langByDev_dict = langByDev.to_dict(orient='index')

    return(langByDev_dict)

