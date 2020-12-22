from flask import Flask, render_template
from flask import Response

app = Flask(__name__)

from flask import request

import json
import requests

### WEBSITE STUFF
@app.route('/predict_sales', methods=['GET', 'POST'])
def predict_sales():
    if request.method == 'POST':
        print(request.form['borough'])
        url = "https://6893.stephenshanko.com/api/v1/predictsale"

        params = {"BOROUGH": request.form['borough'],
             "BUILDING CLASS CATEGORY": request.form['bcc'],
             "ZIP CODE": request.form['zip'],
             "RESIDENTIAL_UNITS": request.form['res'],
             "COMMERCIAL UNITS": request.form['comm'],
             "TOTAL UNITS": request.form['total'],
             "LAND_SQUARE_FEET": request.form['land'],
             "GROSS_SQUARE_FEET": request.form['gross'],
             "YEAR BUILT": request.form['year'],
             "TAX CLASS AT TIME OF SALE": request.form['tax'],
             "BUILDING CLASS AT TIME OF SALE": request.form['bcsale'],
             "SALE DATE": request.form['saledate']}

        to_discard = []
        for key in params:
            if params[key].strip() == '':
                to_discard.append(key)
        for item in to_discard:
            params.pop(item)

        if 'BOROUGH' in params:
            params['BOROUGH'] = int(params['BOROUGH'])
        if 'ZIP CODE' in params:
            params['ZIP CODE'] = int(params['ZIP CODE'])
        if 'RESIDENTIAL_UNITS' in params:
            params['RESIDENTIAL_UNITS'] = int(params['RESIDENTIAL_UNITS'])
        if 'COMMERCIAL UNITS' in params:
            params['COMMERCIAL UNITS'] = int(params['COMMERCIAL UNITS'])
        if 'TOTAL UNITS' in params:
            params['TOTAL UNITS'] = int(params['TOTAL UNITS'])
        if 'LAND_SQUARE_FEET' in params:
            params['LAND_SQUARE_FEET'] = int(params['LAND_SQUARE_FEET'])
        if 'GROSS_SQUARE_FEET' in params:
            params['GROSS_SQUARE_FEET'] = int(params['GROSS_SQUARE_FEET'])
        if 'YEAR BUILT' in params:
            params['YEAR BUILT'] = int(params['YEAR BUILT'])
        if 'TAX CLASS AT TIME OF SALE' in params:
            params['TAX CLASS AT TIME OF SALE'] = int(params['TAX CLASS AT TIME OF SALE'])

        payload = {"params":
            params
        }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=json.dumps(payload))
        return render_template('predictsales.html', pred_price=response.json()['PRED_SALE_PRICE'], params=payload['params'])
    else:
        return render_template('predictsales.html', pred_price=None, params=None)

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
