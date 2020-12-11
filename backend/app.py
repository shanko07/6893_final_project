from flask import Flask, render_template
from flask import Response

app = Flask(__name__)

from flask import request

import json
import requests

### API STUFF

@app.route('/api/v1/predictsale', methods=['GET'])
def api_predictsale():
    if request.method == 'GET':
        param_names = ['BOROUGH',
                  'NEIGHBORHOOD',
                  'BUILDING_CLASS',
                  'ZIP_CODE',
                  'RESIDENTIAL_UNITS',
                  'COMMERCIAL_UNITS',
                  'TOTAL_UNITS',
                  'LAND_SQUARE_FEET',
                  'GROSS_SQUARE_FEET',
                  'YEAR_BUILT', 'TAX_CLASS_AT_TIME_OF_SALE',
                  'BUILDING_CLASS_AT_TIME_OF_SALE',
                  'SALE_DATE'
                  ]

        # TODO: find out if any params are missing from request and use summary stats to fill that missing data
        # TODO: query the model with given params and filled missing data to obtain the predicted sale price

        pred = 500000

        return Response(json.dumps({'PRED_SALE_PRICE': pred}), status=200,
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
