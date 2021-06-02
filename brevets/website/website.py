from flask import Flask, render_template, request, redirect, url_for
import requests
import logging

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/listAll', methods=['GET'])
def listeverything():
    top = request.args.get('top')
    dtype = str(request.args.get('dtype'))
    if top:
        r = requests.get('http://restapi:5000/listAll/' + dtype + "?top=" + str(top))
    else:
        r = requests.get('http://restapi:5000/listAll/' + dtype)
    return r.text    

@app.route('/listOpenOnly', methods=['GET'])
def listopen():
    top = request.args.get('top')
    dtype = str(request.args.get('dtype'))
    if top:
        r = requests.get('http://restapi:5000/listOpenOnly/' + dtype + "?top=" + str(top))
    else:
        r = requests.get('http://restapi:5000/listOpenOnly/' + dtype)
    return r.text

@app.route('/listCloseOnly', methods=['GET'])
def listclose():
    top = request.args.get('top')
    dtype = str(request.args.get('dtype'))
    if top:
        r = requests.get('http://restapi:5000/listCloseOnly/' + dtype + "?top=" + str(top))
    else:
        r = requests.get('http://restapi:5000/listCloseOnly/' + dtype)
    return r.text


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
