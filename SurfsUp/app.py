# Import the dependencies.
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

from flask import Flask, jsonify

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
@app.route('/')
def index():
    '''Lists all available API Routes'''
    return(
        '<h1>Hawaii Weather Analysis</h1><br>'
        '<h2>Available API Routes:</h2><br>'
        '<a href="/api/v1.0/precipitation"></a><br>'
        '<a href=""></a><br>'
        '<a href=""></a><br>'
    )

@app.route('/api/v1.0/precipitation')
def precipitation_query():
    '''Precipitation query results for last year'''
    index()
    with Session() as session:  # Find the most recent date in the data set.
        first_date = session.query(
            func.max(measurement.date)
            ).scalar()
    first_date = dt.datetime.strptime(first_date, '%Y-%m-%d')
    last_date = first_date - dt.timedelta(days = 365)

    # Perform a query to retrieve the data and precipitation scores
    sel = [
        measurement.date
        ,measurement.prcp
    ]
    with Session() as session:
        data = session.query(*sel
            ).filter(measurement.date <= first_date
            ).filter(measurement.date >= last_date
            ).all()
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug = True)