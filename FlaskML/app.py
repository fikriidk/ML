import os
import numpy as np
import flask
import pickle
from flask import Flask, redirect, url_for, request, render_template


# creating instance of the class
app = Flask(__name__, template_folder='templates')

# to tell flask what url should trigger the function index()


@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')


# prediction function
# Memprediksi input dari form user
def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 3)
    loaded_model = pickle.load(
        open("./model/yugiohcard.pkl", "rb"))  # load the model
    # predict the values using loded model
    result = loaded_model.predict(to_predict)
    return result


@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        name = request.form['name']
        level = request.form['level']
        attack = request.form['attack']
        defend = request.form['defend']

        to_predict_list = list(map(int, [level, attack, defend]))
        result = ValuePredictor(to_predict_list)

        if int(result) == 0:
            prediction = 'Anda Memiliki kartu yang lemah'
            img = 'static/img/larvae-moth-card.jpg'
            
        elif int(result) == 1:
            prediction = 'Anda Memiliki kartu yang normal'
            img = 'static/img/dark_blade_card.png'
            
        elif int(result) == 2:
            prediction = 'Anda Memiliki kartu yang kuat'
            img = 'static/img/chaos-emperor_card.png'
        return render_template("result.html", prediction=prediction, name=name, img=img)


if __name__ == "__main__":
    app.run(debug=False)  # use debug = False for jupyter notebook
