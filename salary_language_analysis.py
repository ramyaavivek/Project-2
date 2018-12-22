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

app = Flask(__name__)

#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/developers.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Survey = Base.classes.survey

def salaryLanguageAnalysis():

    # find devtypes, languageworkedwith, salary
    s = [Survey.Respondent,
        Survey.DevType,
        Survey.LanguageWorkedWith,
        Survey.ConvertedSalary
        ]

    radarResults = db.session.query(*s).filter(Survey.ConvertedSalary != '').all()

    # put results into pandas
    df = pd.DataFrame(radarResults)
    df['ConvertedSalary'] = pd.to_numeric(df['ConvertedSalary'])
    df.head()

    # explode the devtype column so there's only one devtype for each row
    expdev_df = pd.DataFrame(df.DevType.str.split(';').tolist(), index=[df.Respondent, df.LanguageWorkedWith, df.ConvertedSalary]).stack()
    expdev_df = expdev_df.reset_index()
    expdev_df = expdev_df.rename(columns={0:'DevType'})
    expdev_df = expdev_df.drop(columns='level_3')

    # split the langages string delimeted wityh ';'
    expdev_df['LanguageList'] = expdev_df.LanguageWorkedWith.str.split(';')

    # hard code top 10 languages from stack ooverflow website
    topLang = ['JavaScript', 'HTML', 'CSS', 'SQL', 'Java', 'Bash/Shell', 'Python', 'C#', 'PHP', 'C++']

    # Loop through each language and see if each respondent knows the language
    for language in topLang:
        
        # dynamically create new column headers
        print('Checking for: ' + language + '...')        
        
        # Create new column to check if the respondent knows a language. If the languege is in the list of known languages, the salary of that respondent, else it gets 0
        expdev_df[language] = np.where(expdev_df.LanguageList.apply(lambda x: language in x), expdev_df['ConvertedSalary'], False)
        
        print(f'{language} done!')

    # Aggregation by mean gives the average salary for that language
    salLangDev = expdev_df.groupby('DevType').mean()
    salLangDev = salLangDev.drop(index='', columns=['Respondent', 'ConvertedSalary'])

    # Round each percent to 2 decimals
    salLangDev = salLangDev.round(decimals=2)

    # Convert df to dict to serve as json. Orient by index to make it easily searchable by devtype
    salLangDev_dict = salLangDev.to_dict(orient='index')

    return(salLangDev_dict)


