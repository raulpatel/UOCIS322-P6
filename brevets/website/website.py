from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')


@app.route('/listAll', methods=['GET'])
def listeverything():
    top = request.args.get('top', type=int)
    dtype = request.args.get('dtype', type=str)
    if top:
        r = requests.get('http://restapi:5000/listAll/' + dtype + "?top=" + str(top))
    else:
        r = requests.get('http://restapi:5000/listAll/' + dtype)
    return render_template('index.html', result=r.text)

@app.route('/listOpenOnly', methods=['GET'])
def listopen():
    top = request.args.get('top', type=int)
    dtype = request.args.get('dtype', type=str)
    if top:
        r = requests.get('http://restapi:5000/listOpenOnly/' + dtype + "?top=" + str(top))
    else:
        r = requests.get('http://restapi:5000/listOpenOnly/' + dtype)
    return render_template('index.html', result=r.text)

@app.route('/listCloseOnly', methods=['GET'])
def listclose():
    top = request.args.get('top', type=int)
    dtype = request.args.get('dtype', type=str)
    if top:
        r = requests.get('http://restapi:5000/listCloseOnly/' + dtype + "?top=" + str(top))
    else:
        r = requests.get('http://restapi:5000/listCloseOnly/' + dtype)
    return render_template('index.html', result=r.text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
