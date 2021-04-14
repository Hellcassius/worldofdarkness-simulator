#!/usr/bin/env python
from flask_wtf import FlaskForm
from flask import Flask, render_template, request, url_for, jsonify, redirect
from wtforms import SelectField, IntegerField, StringField
import pandas as pd
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = "!@#$%^&*()"
app.config["TEMPLATES_AUTO_RELOAD"] = True
USER_DATA = pd.read_csv("/home/caio/wod-sim/data/data_sample.csv")


@app.route("/", methods=["GET", "POST"])
def index():
    print(request.method)
    if request.method == "POST":
        print("######################## POST ###################################")
        return render_template("index.html")

    else:
        print("########################### GET #######################################")

        return render_template("index.html")


def roll(n, t):

    result = [random.randint(1, 10) for i in range(1, n + 1)]
    result += [random.randint(1, 10) for roll in result if roll == 10]
    successes = len([roll for roll in result if roll >= t])
    critical = len([roll for roll in result if roll == 1])
    result += [len(result), (successes - critical)]
    str_res = [str(roll) for roll in result]
    return " | ".join(str_res)


def load_sheet(login_data, sheet):
    sheet = Sheet()
    sheet.player = login_data["username"]
    sheet.name = login_data["name"]
    sheet.forca = login_data["forca"]
    sheet.destreza = login_data["destreza"]
    sheet.vigor = login_data["vigor"]
    sheet.carisma = login_data["carisma"]
    sheet.manipulacao = login_data["manipulacao"]
    sheet.compostura = login_data["compostura"]
    sheet.percepcao = login_data["percepcao"]
    sheet.inteligencia = login_data["inteligencia"]
    sheet.raciocinio = login_data["raciocionio"]
    sheet.exp = IntegerField("EXP")

    return sheet


@app.route("/show_sheet", methods=["GET", "POST"])
def show_sheet():
    if request.method == "POST":
        sheet = Sheet()
        print(Login().username.data)
        return render_template("ficha.html", form=sheet)
    else:
        sheet = Sheet()
        return render_template("ficha.html", form=sheet)


@app.route("/roll_result", methods=["GET", "POST"])
def show_roll():
    if request.method == "POST":
        roll_form = Roll()
        n = roll_form.dice_number.data
        t = roll_form.target_diff.data
        roll_form.result = roll(n, t)
        return render_template("roll.html", form=roll_form)
    else:
        r = Roll()
        return render_template("roll.html", form=r)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_form = Login()
        username = login_form.username.data
        mask = USER_DATA["username"] == username
        login_data = USER_DATA[mask]
        if not login_data.empty:
            return redirect("/")
        else:
            return "Bosta!"
    else:
        l = Login()
        return render_template("login.html", form=l)


class Roll(FlaskForm):
    dice_number = IntegerField("number_of_rolls", default=6)
    target_diff = IntegerField("difficulty", default=6)
    result = roll(6, 7)


class Sheet(FlaskForm):
    name = StringField("name")
    player = StringField("player_id")

    forca = SelectField("FOR", choices=[(i, i) for i in range(1, 6)])
    destreza = SelectField("DEX", choices=[(i, i) for i in range(1, 6)])
    vigor = SelectField("STA", choices=[(i, i) for i in range(1, 6)])
    carisma = SelectField("CHA", choices=[(i, i) for i in range(1, 6)])
    manipulacao = SelectField("MAN", choices=[(i, i) for i in range(1, 6)])
    compostura = SelectField("COM", choices=[(i, i) for i in range(1, 6)])
    percepcao = SelectField("PER", choices=[(i, i) for i in range(1, 6)])
    inteligencia = SelectField("INT", choices=[(i, i) for i in range(1, 6)])
    raciocinio = SelectField("WIT", choices=[(i, i) for i in range(1, 6)])
    exp = IntegerField("EXP")


class Login(FlaskForm):
    username = StringField("Username")


if __name__ == "__main__":
    app.run(port=5000, debug=True)