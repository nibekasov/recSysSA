import json

from flask import Flask, render_template, request, redirect, url_for, session
from inference import get_recommendations


app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        return access_param(username)
    else:
        return render_template('login.html')


@app.route('/index')
def access_param(id):
    # 283725137902134437008251670019063891876
    responce = get_recommendations(id)
    return render_template('table.html', result=responce)

app.run(debug=True, host="0.0.0.0", port=5000)


# CHECK THAT IT WORKS!
