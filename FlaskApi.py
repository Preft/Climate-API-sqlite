import numpy as np
import datetime as dt
import dateutil.relativedelta
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
app = Flask(__name__)

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"See below possible paths.<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end><br>"
    )

@app.route("/api/v1.0/precipitation")
def normal():
    session = Session(engine)
    All_Records_Prcp = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    List_date = [date[0] for date in All_Records_Prcp[:]]
    List_prcp = [prcp[1] for prcp in All_Records_Prcp[:]]
    Prcp_Dict = {List_date[i]: List_prcp[i] for i in range(0, len(List_date))}
    return jsonify(Prcp_Dict)



@app.route("/api/v1.0/stations")
def saefdse():
    session = Session(engine)
    Unique_Stations = session.query(Station.name).distinct()
    session.close()
    List_Station = [station[0] for station in Unique_Stations[:]]
    return jsonify(List_Station)

@app.route("/api/v1.0/tobs")
def hrtdsgr():
    session = Session(engine)
    Max_Date_Query = session.query(Measurement).order_by(Measurement.date.desc()).first()
    Query_Date = dt.datetime.strptime(Max_Date_Query.date, '%Y-%m-%d') - dateutil.relativedelta.relativedelta(months=12)
    Max_Occurance_Station_Query = session.query(Measurement.station, func.count(Measurement.station).label('Occurances')).filter(Measurement.date >= Query_Date).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    Highest_Station = Max_Occurance_Station_Query.station
    Highest_Station_Temps = session.query(Measurement.tobs).filter(Measurement.date >= Query_Date).all()
    session.close()
    Temp_List = [item[0] for item in Highest_Station_Temps[:]]
    return jsonify(Temp_List)

@app.route("/api/v1.0/<start>")
def hsdrgdra(start):
    Date_Init = dt.datetime.strptime(start, '%Y-%m-%d')
    session = Session(engine)
    Date_Init = dt.datetime.strptime(start, '%Y-%m-%d')
    Temp_Query_List = session.query(Measurement.tobs).filter(Measurement.date >= Date_Init).all()
    Temp_List = [item[0] for item in Temp_Query_List[:]]
    session.close()
    MaxTemp = max(Temp_List)
    MinTemp = min(Temp_List)
    AvgTemp = np.mean(Temp_List)
    return (f'Max Temperature|Min Temperature| Average Temperature<br>'
            f'{MaxTemp}|{MinTemp}|{AvgTemp}')

@app.route("/api/v1.0/<start>/<end>")
def agease(start, end):
    session = Session(engine)
    Date_Init = dt.datetime.strptime(start, '%Y-%m-%d')
    Date_End = dt.datetime.strptime(end, '%Y-%m-%d')
    Temp_Query_List = session.query(Measurement.tobs).filter(Measurement.date >= Date_Init).filter(Measurement.date <= Date_End).all()
    Temp_List = [item[0] for item in Temp_Query_List[:]]
    session.close()
    MaxTemp = max(Temp_List)
    MinTemp = min(Temp_List)
    AvgTemp = np.mean(Temp_List)
    return (f'Max Temperature|Min Temperature| Average Temperature<br>'
            f'{MaxTemp}|{MinTemp}|{AvgTemp}<br>')
    
if __name__ == "__main__":
    app.run(debug=True)