# import dependencies
from flask import Flask, jsonify
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


# create index route
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/<start><br/>"
            f"/api/v1.0/<start>/<end>"
        )

# create precipitation route
@app.route("/api/v1.0/precipitation")
def prcp():
    # create session 
    session = Session(engine)

    # query database for summed precipitation data
    precip = session.query(Measurement.date, func.sum(Measurement.prcp)).filter(Measurement.prcp>=0).group_by(Measurement.date).all()

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

    # query database for summed precipitation data
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

    # query database for summed precipitation data
    year_temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>='2016-08-23').filter(Measurement.station == 'USC00519281').all()

    # create empty dictionary
    temps_dict = {}

    # turn list of tuples into dictionary
    for temp in year_temps:
        temps_dict[temp[0]] = temp[1]

    # close session
    session.close()

    return jsonify(temps_dict)

# create date search route
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def date_search(start, end='2017-08-23'):

    # create session 
    session = Session(engine)

    # query database for summed precipitation data
    date_range = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).\
        all()

    # create empty dictionary
    stats_dict = {}

    # turn list of tuples into dictionary
    for stat in date_range:
        stats_dict["Start Date"] = start
        stats_dict["End Date"] = end
        stats_dict["Min Temp"] = stat[0]
        stats_dict["Avg Temp"] = round(stat[2],2)
        stats_dict["Max Temp"] = stat[1]

    # close session
    session.close()

    return jsonify(stats_dict)

# run in debug mode
if __name__ == "__main__":
    app.run(debug=True)