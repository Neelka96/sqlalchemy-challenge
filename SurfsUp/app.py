# Import the dependencies.
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

from flask import Flask, jsonify, request

import datetime as dt


#################################################
# Database Setup
#################################################
# Create engine for DataBase queries
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
Session = sessionmaker(bind = engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# Variable Route Listings for Index
route_home = '/'
route_prcp = '/api/v1.0/precipitation'
route_stations = '/api/v1.0/stations'
route_tobs = '/api/v1.0/tobs'
# route_start = '/api/v1.0/'

### Home Route
### ----------
@app.route(route_home)
def home():
    '''Lists all available API Routes'''
    return(
        '<h1>Hawaii Weather Analysis</h1></br>'
        '<h2>Available API Routes:</h2></br>'
        f'<a href="{route_prcp}">Precipitation (Inches) - Most recent year in hawaii.sqlite</a></br>'
        f'<a href="{route_stations}">List of all observing Stations</a></br>'
        f'<a href="{route_tobs}">Temperature observations for most recent year at most active station</a></br>'
        '<a href="#"></a></br>'
    )


### Precipitation Query Route
### -------------------------
@app.route(route_prcp)
def precipitation_query(last_date):
    '''Query for precipitation scores for last year of db'''
    with Session() as session: # Finding `first_date`
        first_date = session.query(
            func.max(measurement.date)
            ).scalar()
    first_date = dt.datetime.strptime(first_date, '%Y-%m-%d')
    last_date = first_date - dt.timedelta(days = 365)
    sel = [
        measurement.date
        ,measurement.prcp
    ]
    with Session() as session: # Precipitation Scores
        data = session.query(*sel
            ).filter(measurement.date >= last_date
            ).all()
        
    json_api = {}
    queryData = []
    for date, prcp in data:
        add_dict = {date: prcp}
        queryData.append(add_dict)

    metaData = {
        'current_route': route_prcp
        ,'home_route': request.host 
        ,'data_points': len(queryData)
    }
    json_api['metadata'] = metaData
    json_api['query_data'] = queryData

    return jsonify(json_api)


### All Stations Query Route
### ------------------------
@app.route(route_stations)
def stations_query():
    '''Query for full list of stations'''
    sel = [
        station.station
        ,station.name
        ,station.latitude
        ,station.longitude
        ,station.elevation
    ]
    with Session() as session:
        data = session.query(*sel).all()
    json_api = []
    for id, name, latitude, longitude, elevation in data:
        add_dict = {}
        add_dict['id'] = id
        add_dict['name'] = name
        add_dict['lat'] = latitude
        add_dict['lng'] = longitude
        add_dict['elevation'] = elevation
        json_api.append(add_dict)
    return jsonify(json_api)


### Most Active Station Temperatures Query Route
### --------------------------------------------
@app.route(route_tobs)
def tobs_query():
    '''Query for last year of temp data for most active station'''
    with Session() as session: # Finding `first_date`
        first_date = session.query(
            func.max(measurement.date)
            ).scalar()
    first_date = dt.datetime.strptime(first_date, '%Y-%m-%d')
    last_date = first_date - dt.timedelta(days = 365)
    station_count = func.count(measurement.station)
    sel = [
        measurement.station
        ,station_count
    ]
    with Session() as session:
        data = session.query(*sel
            ).group_by(measurement.station
            ).order_by(station_count.desc()
            ).first()
    most_active = data[0]

    sel = [
        measurement.date
        ,measurement.tobs
    ]
    with Session() as session:
        data = session.query(*sel
            ).filter(measurement.station == most_active
            ).filter(measurement.date >= last_date
            ).all()
    json_api = []
    for date, tobs in data:
        add_dict = {}
        add_dict['date'] = date
        add_dict['tobs'] = tobs
        json_api.append(add_dict)
    return jsonify(json_api)



if __name__ == '__main__':
    app.run(debug = True)