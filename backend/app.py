from flask import Flask, render_template
from flask import Response

app = Flask(__name__)

from flask import request

import json
import requests
import joblib
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pymysql.cursors
from datetime import datetime

loaded_rf = joblib.load("whole_dataset.joblib")
needed_cols = None
with open('model_cols', 'rb') as fp:
    needed_cols = pickle.load(fp)

### API STUFF

@app.route('/api/v1/predictsale', methods=['GET'])
def api_predictsale():
    if request.method == 'GET':

        param_names = [
            'BOROUGH',
            'BUILDING CLASS CATEGORY',
            'ZIP CODE',
            'RESIDENTIAL_UNITS',
            'COMMERCIAL UNITS',
            'TOTAL UNITS',
            'LAND_SQUARE_FEET',
            'GROSS_SQUARE_FEET',
            'YEAR BUILT',
            'TAX CLASS AT TIME OF SALE',
            'BUILDING CLASS AT TIME OF SALE',
            'SALE DATE'
        ]

        params_supplied = request.json['params']

        for k in params_supplied:
            if k not in param_names:
                return Response(json.dumps({'reason':f'illegal prediction param {k}'}), status=404, mimetype='application/json')

        query_dict = {name:[params_supplied[name]] for name in params_supplied}


        # use the database averages or modes to clean up any missing parameters for prediction
        connection = pymysql.connect(
                        host='6893.stephenshanko.com',
                        user='db_reader',
                        password='&3QTLyJo6jwA2,.1u{Zy',
                        db='6893_project',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                missing = set(param_names) - set(params_supplied.keys())
                for name in missing:
                    if name in ['BOROUGH', 'BUILDING CLASS CATEGORY', 'ZIP CODE','TAX CLASS AT TIME OF SALE', 'BUILDING CLASS AT TIME OF SALE']:
                        # use the mode since these are categorical
                        operator = name
                        sql = f"select `{name}`, occurs from (select `{name}`, count(*) as occurs from Clean_Data group by `{name}` limit 1) t1"
                    elif name == 'SALE DATE':
                        operator = 'max'
                        sql = f"select {operator}(`{name}`) as {operator} from Clean_Data"
                    else:
                        # use the average since these are continuous
                        operator = 'avg'
                        sql = f"select {operator}(`{name}`) as {operator} from Clean_Data"
                    cursor.execute(sql)
                    measure = cursor.fetchone()[operator]
                    query_dict[name] = measure
        finally:
            connection.close()

        if type(query_dict['SALE DATE']) == datetime:
            query_dict['SALE DATE'] = [query_dict['SALE DATE'].strftime("%m-%d-%Y %H:%M:%S")]

        max_date = pd.to_datetime('2019-12-31 00:00:00')
        query_df = pd.DataFrame.from_dict(query_dict)
        query_df = query_df.astype({'RESIDENTIAL_UNITS':'int64'})
        query_df = query_df.astype({'COMMERCIAL UNITS':'int64'})
        query_df = query_df.astype({'TOTAL UNITS':'int64'})
        query_df = query_df.astype({'LAND_SQUARE_FEET':'int64'})
        query_df = query_df.astype({'GROSS_SQUARE_FEET':'int64'})
        query_df = query_df.astype({'YEAR BUILT':'int64'})
        query_df['Date'] = 0

        query_df['SALE DATE'] = pd.to_datetime(query_df['SALE DATE'])

        def month_distance(start, end):
            mdiff = (end.year - start.year) * 12 + end.month - start.month
            return mdiff

        for i, row in query_df.iterrows():
            query_df.at[i,'Date'] = month_distance(row['SALE DATE'],max_date)
        query_df.set_index('SALE DATE', inplace=True)
        query_df = pd.get_dummies(query_df, columns = ['Date'], prefix = 'Date')

        one_hots = ['BOROUGH','BUILDING CLASS CATEGORY','ZIP CODE','TAX CLASS AT TIME OF SALE','BUILDING CLASS AT TIME OF SALE']
        query_df = pd.get_dummies(query_df, columns = one_hots, prefix = one_hots)


        for col in needed_cols:
            if col not in query_df.columns:
                query_df[col]=0

        query_df = query_df.reindex(columns=needed_cols)


        predicted_val = loaded_rf.predict(query_df.drop(columns =['SALE_PRICE']))
        print(predicted_val[0])

        return Response(json.dumps({'PRED_SALE_PRICE': predicted_val[0]}), status=200,
                            mimetype='application/json')
    else:
        return Response("{'reason':'illegal method for call'}", status=404, mimetype='application/json')


@app.route('/api/v1/summarize', methods=['GET'])
def api_summarize():
    if request.method == 'GET':

        # selection of columns or data dimensions
        request.json['groupby']
        # filter criteria
        request.json['filter']
        # select which data columns you want to have
        request.json['select']

        return Response(json.dumps({'data': [{'BOROUGH': 'manhattan', 'SALE_PRICE': 500000}, {'BOROUGH': 'brooklyn', 'SALE_PRICE': 400000},]}), status=200, mimetype='application/json')
    else:
        return Response("{'reason':'illegal method for call'}", status=404, mimetype='application/json')


@app.route('/api/v1/trends', methods=['GET'])
def api_trends():
    if request.method == 'GET':

        # specify how you want to summarize "sum, mean, mode, min, max"
        request.json['summary']
        # select which data columns you want to have
        request.json['select']
        # should be a dict {start: date, stop: date}
        request.json['window']
        # should be in the following format xd, xw, xm, xy where x is a number and we have days, weeks, months, years
        request.json['frequency']

        return Response(json.dumps({'data': [{'SALE_PRICE': 500000}, {'SALE_PRICE': 600000}, {'SALE_PRICE': 400000}, {'SALE_PRICE': 4500000}]}), status=200,
                        mimetype='application/json')
    else:
        return Response("{'reason':'illegal method for call'}", status=404, mimetype='application/json')


### WEBSITE STUFF
"""
@app.route('/organization', methods=['GET', ])
def site_organization():
    events = get_events(request.args['orgName'])
    return render_template('orgdisplay.html', orgName=request.args['orgName'], events=events)

@app.route('/event', methods=['GET', ])
def site_event():
    deets = get_event_details(request.args['orgName'], request.args['eventName'])
    return render_template('eventdisplay.html', deets=deets)


### SUPPORTING FUNCTIONS
def get_events(orgName):
    '''

    :param orgName: organization name
    :return: list of event objects in the form [{'eventName': 'my-event-name'},...]
    '''
    myclient = pymongo.MongoClient(dbaddress)

    mydb = myclient['streamphl']
    eventscol = mydb['events']

    events = eventscol.find(filter={'_orgName': orgName}, projection=['_eventName', ])
    events_list = list(events)
    converted = []
    for item in events_list:
        converted.append({'eventName': item['_eventName']})
    return converted

def get_event_details(orgName, eventName):
    myclient = pymongo.MongoClient(dbaddress)

    mydb = myclient['streamphl']
    eventscol = mydb['events']

    querytext = {'_orgName': orgName, '_eventName': eventName}

    count = eventscol.count_documents(filter=querytext)

    event_dict = {}

    if count == 1:
        d = eventscol.find(filter=querytext)[0]
        event_dict['orgName'] = d['_orgName']
        event_dict['eventName'] = d['_eventName']
        event_dict['key'] = d['key']
        event_dict['services'] = d['services']

    return event_dict
"""

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
