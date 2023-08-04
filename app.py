# Import the dependencies.
from flask import Flask
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route('/')
def home():
    return f'''
        <h1>Climate App</h1>
        
        <h3>Use the following paths for data:</h3>
        <ul>
            <li>/api/v1.0/precipitation</li>
            <li>/api/v1.0/station</li>
            <li>/api/v1.0/tobs</li>
            <li>/api/v1.0/[startDate]</li>
            <li>/api/v1.0/[starDate]/[endDate]</li>
        </ul>'''

@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    return dict(session.query(measurement.date,measurement.prcp).all())

@app.route('/api/v1.0/station')
def location():
    session = Session(engine)
    return dict(session.query(station.station, station.name).all())

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    return dict(session.query(measurement.date, measurement.tobs).all())

@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def dateRange(start,end='2017-08-23'):
    session = Session(engine)

    low,avg,high = session.query(func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)).first()

    return {'Min':low, 'Avg':avg, 'Max':high}


if __name__ == '__main__':
    app.run(debug=True)