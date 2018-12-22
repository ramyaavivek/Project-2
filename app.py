import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func,desc

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

from language_analysis import languageAnalysis

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


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/degrees")
def degrees():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query

    results = db.session.query(Survey.UndergradMajor, func.max(Survey.ConvertedSalary)).filter(Survey.UndergradMajor != '').filter(Survey.Currency.contains('U.S. dollars ($)')).filter(Survey.Employment=='Employed full-time').filter(Survey.Student=='No').filter(Survey.YearsCoding=='0-2 years').group_by(Survey.UndergradMajor).order_by(func.max(Survey.ConvertedSalary)).all()
    
    list1=[]
    list2=[]
    majorList = []
    majorDict = {}
    for result in results:
        
        list1.append(result[0])
        list2.append(result[1])
       
    majorDict['label']=list1
    majorDict['data']=list2    
    #majorList.append(majorDict)

    # df = pd.read_sql_query(results, db.session.bind)
    # df_degrees = dfYoung[['UndergradMajor','ConvertedSalary']]
    # df_degrees=df_degrees.groupby('UndergradMajor').max()
    # Return a list of the column names (sample names)
    return jsonify(majorDict)


@app.route("/jobsatisfaction")
def getjob():
    """Return the MetaData for a given sample."""
    results = db.session.query(Survey.JobSatisfaction, func.count(Survey.JobSatisfaction)).group_by(Survey.JobSatisfaction).all()
    label1=[]
    data1=[]
    jobdict = {}
    for result in results:
        if(result[0]==''):
            label1.append("Others")
        else:
            label1.append(result[0])
        data1.append(result[1])
       
    jobdict['label']=label1
    jobdict['data']=data1    
    print(jobdict)
    return jsonify(jobdict)

@app.route("/gender")
def getGender():
    """Return the MetaData for a given sample."""
    print("inside the loop")
    label2=[]
    data2=[]
    gender = {}
    results = db.session.query(Survey.Gender, func.count(Survey.Gender)).group_by(Survey.Gender).all()
    results1=db.session.query(func.count(Survey.Respondent)).all()
    label2.append('Total')
    data2.append(results1[0][0])
   # Create a dictionary entry for each row of metadata information
    for result in results:
            
            label2.append(result[0])
            data2.append(result[1])

    gender['label']=label2
    gender['data']=data2  
    
    print(results)
    return jsonify(gender)

@app.route('/codinglanguages')
def codingLanguages():
    '''
    Serves a JSON dictionary of coding language usage by devtype
    '''
    languageData = languageAnalysis()
    return jsonify(languageData)


@app.route("/countries")
def countries():
    """Return `otu_ids`, `otu_labels`,and `sample_values`."""
    label3=[]
    data3=[]
    countries = {}
    results = db.session.query(Survey.Country,func.count(Survey.Country)).group_by(Survey.Country).order_by(desc(func.count(Survey.Country))).all()
    # Create a dictionary entry for each row of metadata information
    for result in results:
            
            label3.append(result[0])
            data3.append(result[1])

    countries['label']=label3
    countries['data']=data3 
    
    print(results)
    return jsonify(countries)


if __name__ == "__main__":
    app.run()
