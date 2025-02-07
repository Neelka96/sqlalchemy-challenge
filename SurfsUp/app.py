# Import the dependencies.
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

from flask import Flask, jsonify, request, abort

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

# Automatic Metadata Creation
# ---------------------------
def metadata_json(route, nest, desc, params):
    metadata = {
        'current_route': route
        ,'home_route': request.host 
        ,'data_points': len(nest)
        ,'info': desc
        ,'params': params
        ,'format': 'json'
    }
    return metadata

# JSON Template Wrapper for metadata_json()
# -----------------------------------------
def json_setup(route, nest, desc = 'None', params = 'None'):
    json_api = {
        'metadata': metadata_json(route, nest, desc, params)
        ,'result': nest
    }
    return json_api


# Query for Globally Used Data 
# ----------------------------
with Session() as session: # Finding `first_date`
    first_date = session.query(
        func.max(measurement.date)
        ).scalar()
first_date = dt.datetime.strptime(first_date, '%Y-%m-%d')
last_date = first_date - dt.timedelta(days = 365)
app.config['LAST_YEAR_DATE'] = last_date


#################################################
# Flask Routes
#################################################
# Variable Route Listings for Index
route_home = '/'
route_prcp = '/api/v1.0/precipitation'
route_stations = '/api/v1.0/stations'
route_tobs = '/api/v1.0/tobs'
route_start = '/api/v1.0/<start>'
route_end = route_start + '/<end>'


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
def precipitation_query():
    '''Query for precipitation scores for last year of db'''
    last_date = app.config['LAST_YEAR_DATE']
    sel = [
        measurement.date
        ,measurement.prcp
    ]
    with Session() as session: # Precipitation Scores
        data = session.query(*sel
            ).filter(measurement.date >= last_date
            ).all()
    data_nest = []
    for date, prcp in data:
        data_nest.append({date: prcp})
    json_ready = json_setup(
        route_prcp
        ,data_nest
        ,desc = 'Precipitation scores for last year of data'
    )
    return jsonify(json_ready)


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
    data_nest = []
    for id, name, latitude, longitude, elevation in data:
        data_dict = {}
        data_dict['id'] = id
        data_dict['name'] = name
        data_dict['lat'] = latitude
        data_dict['lng'] = longitude
        data_dict['elevation'] = elevation
        data_nest.append(data_dict)
    json_ready = json_setup(
        route_stations
        ,data_nest
        ,desc = 'Full list of observation stations'
    )
    return jsonify(json_ready)


### Most Active Station Temperatures Query Route
### --------------------------------------------
@app.route(route_tobs)
def tobs_query():
    '''Query for last year of temp data for most active station'''
    last_date = app.config['LAST_YEAR_DATE']
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
    data_nest = []
    for date, tobs in data:
        data_dict = {}
        data_dict['date'] = date
        data_dict['tobs'] = tobs
        data_nest.append(data_dict)
    json_ready = json_setup(
        route_tobs
        ,data_nest
        ,desc = 'Last year of temperature data for most active station'
    )
    return jsonify(json_ready)


### Function to be used for Multiple API Calls
### ------------------------------------------
def temp_byDate(start = None, end = None):
    sel = [
        func.min(measurement.tobs)
        ,func.avg(measurement.tobs)
        ,func.max(measurement.tobs)
    ]
    if start and (not end):
        with Session() as session:
            data = session.query(*sel
                ).filter(measurement.date >= start)
    elif start and end:
        with Session() as session:
            data = session.query(*sel
                ).filter(measurement.date >= start
                ).filter(measurement.date <= end)
    else:
        print('Sorry, this API call is not supported yet. ERROR 404')
        abort(404)
    data = data.first()
    data_nest = {
        'TMIN': data[0]
        ,'TAVG': data[1]
        ,'TMAX': data[2]
    }
    json_ready = json_setup(
        route_start
        ,data_nest
        ,desc = 'Basic temperature stats (min, average, and max) for a specified start or start date'
        ,params = {'start_date': start, 'end_date': end}
    )
    return jsonify(json_ready)


### Queries for User Filter in URL
### ------------------------------
@app.route(route_start)
def temp_filter_single(start):
    return temp_byDate(start)

@app.route(route_end)
def temp_filter_double(start, end):
    return temp_byDate(start, end)


if __name__ == '__main__':
    app.run(debug = True)