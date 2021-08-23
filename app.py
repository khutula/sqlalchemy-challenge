# import dependencies
from flask import Flask, jsonify
import numpy as np
from datetime import datetime, timedelta
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

# create app instance
app = Flask(__name__)

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# create session 
session = Session(engine)

# query database for last date
last_date_str = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]

# calculate one year prior
last_date = datetime.strptime(last_date_str, '%Y-%m-%d').date()
year_prior = last_date - timedelta(days=365)
year_prior_str = year_prior.strftime("%Y-%m-%d")

# find most active station info
most_active_station = session.query(Measurement.station, func.count(Measurement.station), Station.id).\
    filter(Station.station==Measurement.station).\
    group_by(Measurement.station).\
    order_by(desc(func.count(Measurement.station))).first()

# close session
session.close()

# create index route
@app.route("/")
def home():

    return (
        f"Available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"Where 2016-08-23 represents a start date: /api/v1.0/2016-08-23<br/>"
            f"Where 2010-01-01 represents a start date and 2017-08-23 represents an end date: /api/v1.0/2010-01-01/2017-08-23"
        )

# create precipitation route
@app.route("/api/v1.0/precipitation")
def prcp():
    # create session 
    session = Session(engine)

    # query database for max precipitation data on given date
    precip = session.query(Measurement.date, func.max(Measurement.prcp)).\
        filter(Measurement.prcp>=0).\
        filter(Measurement.date>=year_prior_str).\
        group_by(Measurement.date).all()

    # create empty dict
    precip_dict = {}

    # turn list of tuples into dictionary
    for entry in precip:
        precip_dict[entry[0]] = round(entry[1],2)

    # close session
    session.close()

    return jsonify(precip_dict)

# create stations route
@app.route("/api/v1.0/stations")
def stns():
    # create session 
    session = Session(engine)

    # query database for all stations
    stations = session.query(Station.station, Station.name, Station.id, Station.elevation, Station.longitude, Station.latitude).all()

    # create empty list
    stations_list = []

    # turn list of tuples into dictionary and add to list
    for entry in stations:
        station_dict = {}
        station_dict["station"] = entry[5]
        station_dict["name"] = entry[1]
        station_dict["id"] = entry[2]
        station_dict["elevation"] = entry[3]
        station_dict["longitude"] = entry[0]
        station_dict["latitude"] = entry[4]
        stations_list.append(station_dict)

    # close session
    session.close()

    return jsonify(stations_list)

# create tobs route
@app.route("/api/v1.0/tobs")
def temps():

    # create session 
    session = Session(engine)

    # query database for temp data using most active station over last year
    year_temps = session.query(Measurement.tobs).\
        filter(Station.station==Measurement.station).\
        filter(Measurement.date>=year_prior_str).\
        filter(Station.id == most_active_station[2]).all()

    # create empty dictionary
    temps_list = list(np.ravel(year_temps))

    # close session
    session.close()

    return jsonify(temps_list)

# create date search route
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def date_search(start, end=last_date_str):

    # create session 
    session = Session(engine)

    # query database for temp calcualted data
    date_range = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).\
        all()

    # create empty dictionary
    stats_dict = {}

    # turn list of tuples into dictionary
    for stat in date_range:
        stats_dict["Min Temp"] = stat[0]
        stats_dict["Avg Temp"] = round(stat[2],2)
        stats_dict["Max Temp"] = stat[1]

    # close session
    session.close()

    return jsonify(stats_dict)

# run in debug mode
if __name__ == "__main__":
    app.run(debug=True)