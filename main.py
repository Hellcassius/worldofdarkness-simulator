#!/usr/bin/env python
from flask_wtf import FlaskForm
from flask import Flask, render_template, request, url_for, jsonify
from wtforms import SelectField

app = Flask(__name__)
app.config["SECRET_KEY"] = "!@#$%^&*()"
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        print("######################## POST ###################################")

    else:
        print("########################### GET #######################################")


    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
