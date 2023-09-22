import json

# from flask import Flask, request, render_template
from flask import Flask, render_template, request, redirect, url_for, session
from inference import get_recommendations


app = Flask(__name__)


@app.route('/auth')
def log():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        return access_param(username)
        # # Dummy user validation
        # if username == 'admin' and password == 'password':
        #     session['username'] = username
        #     return redirect(url_for('home'))
        # else:
        #     return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/index')
def access_param(id):
    # id = request.args.get('id')
    # '99509958336271854753464934769683843557'
    responce = get_recommendations(id)
    return json.dumps(responce)

app.run(debug=True, host="0.0.0.0", port=5000)

# http://127.0.0.1:5000/index?id=283725137902134437008251670019063891876
# CHECK THAT IT WORKS!
