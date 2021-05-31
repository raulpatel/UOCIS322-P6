import os
from flask import Flask, request
from flask_restful import Resource, Api
from pymongo import MongoClient
app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.tododb

def csv_form(lst, top):
    upper = list(lst[0].keys())  # make sure we have a list of the keys
    length = len(upper)
    upper = ", ".join(upper)  # convert to string
    upper += "\n"
    vals = ""
    if top != -1:
        length = top  # set the new length if one is specified
    for i in range(length):
        row = ", ".join(list(lst[i].values()))
        row += "\n"
        vals += row
    return upper + vals
        

def json_form(lst, top):
    if top == -1:
        return flask.jsonify(lst)
    else:
        result = []
        for i in range(top):
            result.append(lst[i])
        return flask.jsonify(result)

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
api.add_resource(listAll, '/listAll/<string:dtype>')
api.add_resource(listOpenOnly, '/listOpenOnly/<string:dtype>')
api.add_resource(listCloseOnly, '/listCloseOnly/<string:dtype>')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
