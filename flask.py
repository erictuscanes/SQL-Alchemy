
# coding: utf-8

# In[1]:


#Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import numpy as np


# In[2]:


from flask import Flask, jsonify, json
import datetime as dt


# In[3]:


#Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)


# In[4]:


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# In[5]:


#Save references
Measurement = Base.classes.measurement
Station = Base.classes.station


# In[6]:


# Create session engine from Python to the DB
session = Session(engine)


# In[7]:


#Set up the Flask app
app = Flask(__name__)


# In[8]:


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        "Hawaii Precipitation and Weather Data<br/><br/>"
        "Pick from the available routes below:<br/><br/>"
        "Precipiation from 2016-08-23 to 2017-08-23.<br/>"
        "/api/v1.0/precipitation<br/><br/>"
        "A list of all the weather stations in Hawaii.<br/>"
        "/api/v1.0/stations<br/><br/>"
        "The Temperature Observations (tobs) from 2016-08-23 to 2017-08-23.<br/>"
        "/api/v1.0/tobs<br/><br/>"
        "Type in a date (i.e., 2013-09-26) to see the min, max and avg temperature since that date.<br/>"
        "/api/v1.0/temp/<start><br/><br/>"
        "Type in a date range (anywhere between 2010-01-01/2017-08-23) to see the min, max and avg temperature for that range.<br/>"
        "/api/v1.0/temp/<start>/<end><br/>"
    )


# In[9]:


#Last twelve months of precipitation
begin_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    results = session.query(Measurement.date, Measurement.prcp).                        filter(Measurement.date > begin_date).                        order_by(Measurement.date).all()

    # Create a dictionary from the row data and append to a list of for the precipitation data
    precipitation_data = []
    for prcp_data in results:
        prcp_data_dict = {}
        prcp_data_dict["Date"] = prcp_data.date
        prcp_data_dict["Precipitation"] = prcp_data.prcp
        precipitation_data.append(prcp_data_dict)
        

    return jsonify(precipitation_data)


# In[10]:


#Return stations in JSON format
@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    
    # Query all the stations
    results = session.query(Station).all()

    # Create a dictionary to append the station data
    stations_info = []
    for stations in results:
        stations_dict = {}
        stations_dict["Station"] = stations.station
        stations_dict["Station Name"] = stations.name
        stations_dict["Latitude"] = stations.latitude
        stations_dict["Longitude"] = stations.longitude
        stations_dict["Elevation"] = stations.elevation
        all_stations.append(stations_dict)
    
    return jsonify(stations_info)


# In[11]:


#Return TOB info in JSON format
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of Temperature Observations (tobs) for the previous year."""
    # Query all the stations and for the given date. 
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).                    group_by(Measurement.date).                    filter(Measurement.date > begin_date).                    order_by(Measurement.station).all()
                    
    # Create a dictionary from the row data and append to a list of for the temperature data.
    tob_data = []
    for tobs_data in results:
        tobs_dict = {}
        tobs_dict["Station"] = tobs_data.station
        tobs_dict["Date"] = tobs_data.date
        tobs_dict["Temperature"] = tobs_data.tobs
        tob_data.append(tobs_dict)
    
    return jsonify(tob_data)


# In[12]:


#Return start date info
@app.route("/api/v1.0/temp/<start>")
def start_date(start=None):
    """Return a json list of the minimum temperature, the average temperature, and the
    max temperature for a given start date"""
    # Query all the stations and for the given date. 
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).    filter(Measurement.date >= start).all()

    # Create a dictionary from the row data and append to a list of for the temperature data.
    start_date_dict = []
    
    for Tmin, Tmax, Tavg in results:
        start_dict = {}
        start_dict["Minimum Temp"] = Tmin
        start_dict["Maximum Temp"] = Tmax
        start_dict["Average Temp"] = Tavg
        start_date_dict.append(start_dict)
    
    return jsonify(start_date_dict)


# In[13]:


#Start and end date info
@app.route("/api/v1.0/temp/<start>/<end>")
def calc_stats(start=None, end=None):
    """Return a JSON list of the minimum temperature, the average temperature, 
    and the max temperature for a given start or start-end range."""
    
    # Query all the stations and for the given range of dates. 
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).    filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Create a dictionary from the row data and append to a list of for the temperature data.
    start_end_dict = []
    
    for Tmin, Tmax, Tavg in results:
        start_end = {}
        start_end["Minimum Temp"] = Tmin
        start_end["Maximum Temp"] = Tmax
        start_end["Average Temp"] = Tavg
        start_end_dict.append(start_end)
    
    return jsonify(start_end_dict)


# In[16]:


if __name__ == '__main__':

    app.run

