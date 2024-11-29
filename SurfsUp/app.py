# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
# Create database connection

engine = ("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session=Session(engine)

#################################################
# Flask Setup
#################################################
# Create an app, being sure to pass __name__
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# define what to do when a user hits the index route
@app.route("/")
def home(): 
    #list available routes
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>br/>"
        f"/api/v1.0/<start>/<end>br/>"

    )
    
# PARTICIPATION PAGE
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the weather data as json"""
    # query results from precipitation analysis (retrive onlt the last 12 months of data)
    last_year = dt.date(2017,8,23)-dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year).all()

    # convert results to a dictionary
    new_results = []
    for date in results:
        row = {}
        row["date"] = pcrp
        row["pcrp"] = date
        new_results.append(row)

    # return the new_results list
    return jsonify(new_results)

#---------------------------------#
# STATION PAGE
# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    active_station = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    return jsonify(active_station)

#----------------------------------#   
# TOBS PAGE /  
# Query the dates and temperature observations of the most-active station for the previous year of data.
@app.route("/api/vi.0/tobs")
def tobs():
    active_data = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= last_year).all()  

# Return a JSON list of temperature observations for the previous year
    return jsonify(active_data)

# /api/v1.0/<start>
#Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
#For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
#For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
@app.route("/api/v1.0/<start>")
def start():
    active_station2 = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.station == 'USC00519281').all() 
    #Return data
    return jsonify(active_station2)

# /api/v1.0/<start>/<end>
#Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
#For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
#For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
@app.route("/api/v1.0/<start>/<end>")
def end():
    active_station2 = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.station == 'USC00519281').all() 
    # return data
    return jsonify(active_station2)

if __name__ == '__main__':
    app.run(debug=True)