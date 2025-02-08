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
route_prcp = '/api/v1.0/precipitation'
route_stations = '/api/v1.0/stations'
route_tobs = '/api/v1.0/tobs'
route_start = '/api/v1.0/<start>'
route_end = '/api/v1.0/<start>/<end>'


### Home Route
### ----------
@app.route('/')
def home():
    '''Lists all available API Routes'''
    style = (
        'body {'
            'font-family: Verdana;'
            'padding: 10px;'
        '}'
        '.route {'
            'font-weight: bold;'
        '}'
        '.route-display {'
            'font-family: monaco;'
            'border: 1px inset;'
            # 'padding: 1px;'
            # 'border-left: 3px solid black;'
            # 'border-right: 3px solid black;'
            # 'padding-left: 6px;'
            # 'padding-right: 6px;'
        '}'
        '.static-route {'
            'border-color: rgb(180, 180, 250);'
            'box-shadow: -1.5px -1.5px rgb(220, 220, 250);'
        '}'
        '.dynamic-route {'
            'border-color: rgb(250, 180, 180);'
            'box-shadow: -1.5px -1.5px rgb(250, 220, 220);'
        '}'
        '#api-desc {'
            'word-wrap: break-word;'
        '}'
        '#route-div {'
            'border-right: 1px solid gray;'
            'padding: 5px;'
        '}'
        '#static-routes-list {'
            'border-left: 5px solid blue;'
            'background-color: rgb(235, 235, 250);'
        '}'
        '#dynamic-routes-list {'
            'border-left: 5px solid red;'
            'background-color: rgb(250, 235, 235);'
        '}'
    )
    sqlite_link = (
        '"https://github.com/Neelka96/sqlalchemy-challenge/'
        'raw/refs/heads/main/SurfsUp/Resources/hawaii.sqlite"'
    )
    api_desc = (
        'Welcome to the Hawaii Climate Analysis API. There are only a few types '
        'of API calls available at this time. See "Available API Routes" for the '
        'full listing. The purposes of this API has been limited to ensure it '
        'meets the stated criteria for this project.<br>'
        '<br>'
        'For the dynamic routes, please set the <start> and/or <end> routes '
        'manually. You may also click the link and then fill in bracketed `<>` '
        'information in your browser.<br>'
        '<br>'
        'Currently, queries are performed using a local sqlite database which is '
        'a major limitation. Later updates may resolve this issue.<br>'
        '<br>'
        f'You can download a copy of the SQLite Database by <a href={sqlite_link}>clicking here!</a><br>'
        '<br>'
    )
    repo_link = 'https://github.com/Neelka96/sqlalchemy-challenge'
    profile_link = '"https://github.com/Neelka96"'
    author_info = (
        f'This GitHub Repository: <a href={repo_link}>Click here</a><br>'
        f'My GitHub Profile: <a href={profile_link}>Click here</a><br>'
    )
    static_routes = (
        '<li>'
            f'<a class="route" href="{route_prcp}">Precipitation (Inches) -- Most recent year</a>'
            '<p>'
                f'<span class="route-display static-route">{request.host}{route_prcp}'
            '</p>'
        '</li>'
        '<li>'
            f'<a class="route" href="{route_stations}">All observing Stations (with station info)</a>'
            '<p>'
                f'<span class="route-display static-route">{request.host}{route_stations}'
            '</p>'
        '</li>'
        '<li>'
            f'<a class="route" href="{route_tobs}">Temperature data -- Most recent year and most active station</a>'
            '<p>'
                f'<span class="route-display static-route">{request.host}{route_tobs}</span>'
            '</p'
        '</li>'
    )
    dynamic_routes = (
        '<li>'
            f'<a class="route" href="{route_start}">Temperature data with `START` date to EOF Range</a>'
            '<h4>URI API Syntax</h4>'
            '<p>'
                f'<span class="route-display dynamic-route">{request.host}{route_start}&lt;start&gt;</span><br>'
                'Replace &lt;start&gt; with date.<br>'
            '</p>'
        '</li>'
        '<li>'
            f'<a class="route" href="{route_end}">Temperature data with `START` date to `END` date Range</a>'
            '<h4>URI API Syntax</h4>'
            '<p>'
                f'<span class="route-display dynamic-route">{request.host}{route_start}&lt;start&gt;/&lt;end&gt;</span><br>'
                'Replace &lt;start&gt; and &lt;end&gt; with dates.<br>'
            '</p>'
        '</li>'
        '<hr>'
        '<p>'
            ' in the format of YYYY-MM-DD.<br>'
            'Note: Years by themselves and months with the year included will also suffice for a parameter, however that is the limit.'
        '</p>'
    )
    return(
        '<head>'
            '<title>Hawaii Climate Analysis</title>'
            '<meta charset="UTF-8">'
            '<meta name="author" content="Neel Agarwal">'
            '<style>'
                f'{style}'
            '</style>'
        '</head>'
        
        '<body>'
            '<h1>'
                'Hawaii Climate Analysis'
            '</h1>'
            '<p id="api-desc">'
                f'{api_desc}'
            '</p>'
        '<hr>'
            '<h2>'
            'Available API Routes:'
            '</h2>'
            '<div id="route-div">'
                '<h3><u>Static Routes</u></h3>'
                '<ul id="static-routes-list">'
                    f'{static_routes}'
                '</ul>'
                '<h3><u>Dynamic Routes</u></h3>'
                '<ul id="dynamic-routes-list">'
                    f'{dynamic_routes}'
                '</ul>'
            '</div>'
        '<hr>'
        '<br>'
            '<p>'
                f'{author_info}'
            '</p>'
        '</body>'
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
        ,desc = 'Precipitation scores for last year of data.'
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
        ,desc = 'Full list of observation stations.'
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
        ,desc = 'Last year of temperature data for most active station.'
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
    return data_nest


### Queries for User Filter in URL
### ------------------------------
@app.route(route_start)
def temp_filter_single(start):
    data_nest = temp_byDate(start)
    json_ready = json_setup(
        route_start
        ,data_nest
        ,desc = 'Basic temperature stats (min, avg, max) for a specified starting date, ends at most recent date.'
        ,params = {'start_date': start, 'end_date': None}
    )
    return jsonify(json_ready)

@app.route(route_end)
def temp_filter_double(start, end):
    data_nest = temp_byDate(start, end)
    json_ready = json_setup(
        route_end
        ,data_nest
        ,desc = 'Basic temperature stats (min, avg, max) for a specified start and end date.'
        ,params = {'start_date': start, 'end_date': end}
    )
    return jsonify(json_ready)


if __name__ == '__main__':
    app.run(debug = True)