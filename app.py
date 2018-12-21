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
    
    majorList = []
   
    for result in results:
        majorDict = {}
        majorDict['category'] = result[0]
        majorDict['amount'] = result[1]
        print(majorDict)
        majorList.append(majorDict)

    # df = pd.read_sql_query(results, db.session.bind)
    # df_degrees = dfYoung[['UndergradMajor','ConvertedSalary']]
    # df_degrees=df_degrees.groupby('UndergradMajor').max()
    # Return a list of the column names (sample names)
    return jsonify(majorList)


@app.route("/metadata/<sample>")
def sample_metadata(sample):
    """Return the MetaData for a given sample."""
    sel = [
        Samples_Metadata.sample,
        Samples_Metadata.ETHNICITY,
        Samples_Metadata.GENDER,
        Samples_Metadata.AGE,
        Samples_Metadata.LOCATION,
        Samples_Metadata.BBTYPE,
        Samples_Metadata.WFREQ,
    ]

    results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()

    # Create a dictionary entry for each row of metadata information
    sample_metadata = {}
    for result in results:
        sample_metadata["sample"] = result[0]
        sample_metadata["ETHNICITY"] = result[1]
        sample_metadata["GENDER"] = result[2]
        sample_metadata["AGE"] = result[3]
        sample_metadata["LOCATION"] = result[4]
        sample_metadata["BBTYPE"] = result[5]
        sample_metadata["WFREQ"] = result[6]

    print(sample_metadata)
    return jsonify(sample_metadata)

@app.route("/freq/<sample>")
def sample_freq(sample):
    """Return the MetaData for a given sample."""
    print("inside the loop")
    sel = [
        Samples_Metadata.sample,
        Samples_Metadata.WFREQ,
    ]

    results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()

    # Create a dictionary entry for each row of metadata information
    sample_metadata = {}
    for result in results:
        sample_metadata["sample"] = result[0]
        
        sample_metadata["WFREQ"] = result[1]

    print(sample_metadata)
    return jsonify(sample_metadata)

@app.route("/samples/<sample>")
def samples(sample):
    """Return `otu_ids`, `otu_labels`,and `sample_values`."""
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Filter the data based on the sample number and
    # only keep rows with values above 1
    sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]
    print(df[sample])
    sample_data=sample_data.sort_values(by=[sample],ascending=False)
    print(sample_data.head(4))
    # Format the data to send as json
    data = {
        "otu_ids": sample_data.otu_id.values.tolist(),
        "sample_values": sample_data[sample].values.tolist(),
        "otu_labels": sample_data.otu_label.tolist(),
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run()
