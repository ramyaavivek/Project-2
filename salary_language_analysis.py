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

        cName = 'salary'+language      
        
        # Create new column to check if the respondent knows a language. If the languege is in the list of known languages, the salary of that respondent, else it gets 0
        expdev_df[language] = np.where(expdev_df.LanguageList.apply(lambda x: language in x), 1, 0)
        expdev_df[cName] = np.where(expdev_df.LanguageList.apply(lambda x: language in x), expdev_df['ConvertedSalary'], 0)
        
        print(f'{language} done!')

    # Aggregate by sum. This will get both the number of coders for a language but also the total salary for that language
    totals = expdev_df.groupby('DevType').sum()
    # drop unnecessary colums
    totals = totals.drop(columns=['Respondent', 'ConvertedSalary'], index='')

    counts = totals[topLang]

    # empty list to hold column names
    salaryList = []

    # concat salery to each language so it matches the column names like in the prev for loop
    for l in topLang:
        c = 'salary' + l
        salaryList.append(c)

    sals = totals[salaryList]

    # rename colums to their original
    sals.columns = topLang

    # divide salaries by count. Thsi oonly takes into accuont people whoo said they knew the language
    salLangDev = sals/counts

    # Round each percent to 2 decimals
    salLangDev = salLangDev.round(decimals=2)

    # Convert df to dict to serve as json. Orient by index to make it easily searchable by devtype
    salLangDev_dict = salLangDev.to_dict(orient='index')

    return(salLangDev_dict)


