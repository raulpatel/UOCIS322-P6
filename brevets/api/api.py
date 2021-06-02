import os
import logging
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.tododb

def csv_form(lst, top):
    upper = list(lst[0].keys())  # make sure we have a list of the keys
    lst_len = len(lst)
    row_len = len(upper)
    upper = ",".join(upper)
    upper += "<br>"
    vals = ""
    if top != -1 and top < lst_len:
        length = top  # set the new length if one is specified
    for i in range(lst_len):
        rows = list(lst[i].values())
        for i in range(row_len):
            rows[i] = str(rows[i])
        row = ",".join(rows)
        row += "<br>"
        vals += row
    return upper + vals
        

def json_form(lst, top):
    if top == -1:
        return jsonify(lst)
    else:
        if top > len(lst):
            top = len(lst)
        result = []
        for i in range(top):
            result.append(lst[i])
        return jsonify(result)

class listAll(Resource):
    def get(self, dtype):
        topk = int(request.args.get('top', default=-1))
        lst = list(db.tododb.find({}, {'_id': 0, 'km': 1, 'open': 1, 'close': 1}))
        if dtype == 'CSV':
            return csv_form(lst, topk)
        return json_form(lst, topk)

class listOpenOnly(Resource):
    def get(self, dtype):
        topk = int(request.args.get('top', default=-1))
        lst = list(db.tododb.find({}, {'_id': 0, 'km': 1, 'open': 1}))
        if dtype == 'CSV':
            return csv_form(lst, topk)
        return json_form(lst, topk)

class listCloseOnly(Resource):
    def get(self, dtype):
        topk = int(request.args.get('top', default=-1))
        lst = list(db.tododb.find({}, {'_id': 0, 'km': 1, 'close': 1}))
        if dtype == 'CSV':
            return csv_form(lst, topk)
        return json_form(lst, topk)

# Create routes
# Another way, without decorators
api.add_resource(listAll, '/listAll', '/listAll/<string:dtype>')
api.add_resource(listOpenOnly, '/listOpenOnly', '/listOpenOnly/<string:dtype>')
api.add_resource(listCloseOnly, '/listCloseOnly', '/listCloseOnly/<string:dtype>')

app.logger.setLevel(logging.DEBUG)

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
