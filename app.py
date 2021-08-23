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
            f"/api/v1.0/precipitation"
            f"/api/v1.0/stations"
            f"/api/v1.0/tobs"
            f"/api/v1.0/<start>"
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
    stations = session.query(Station).all()

    # create empty list
    stations_list = []

    # turn list of tuples into dictionary and add to list
    for station in stations:
        station_dict = {}
        station_dict["station"] = station[5]
        station_dict["name"] = station[1]
        station_dict["id"] = station[2]
        station_dict["elevation"] = station[3]
        station_dict["longitude"] = station[0]
        station_dict["latitude"] = station[4]
        stations_list.append(station_dict)

    # close session
    session.close()

    return jsonify(stations_list)

# run in debug mode
if __name__ == "__main__":
    app.run(debug=True)