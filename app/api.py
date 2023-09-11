import json

from flask import Flask, request, render_template

from inference import get_recommendations


app = Flask(__name__)


@app.route('/auth')
def login():
    return render_template('index.html')


@app.route('/index')
def access_param():
    id = request.args.get('id')
    # '99509958336271854753464934769683843557'
    responce = get_recommendations(id)
    return json.dumps(responce)

app.run(debug=True, host="0.0.0.0", port=5000)

# http://127.0.0.1:5000/index?id=99509958336271854753464934769683843557
# CHECK THAT IT WORKS!