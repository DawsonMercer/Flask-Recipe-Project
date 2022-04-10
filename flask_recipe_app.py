import csv
import os
import random
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

#venv\Scripts\activate
#$env:FLASK_APP = "flask_recipe_app"
# $env:FLASK_ENV = "development"
#flask run


@app.route("/")
def main_page():
    return render_template("index.html")


@app.route("/view-all")
def view_all():
    return render_template("viewAll.html")

@app.route("/recipe/<string:recipe_name>")
def recipe(recipe_name):

    recipe_list = ["applepie", "smoothie", "salad"]
    # todo if recipe_name exists in csv, display recipe. else error

    if(recipe_name in recipe_list):
        return render_template("recipe.html", recipe_name=recipe_name)
    else:
        return render_template("error.html")


@app.route("/pick-random")
def pick_random():
    recipe_list = ["applepie", "smoothie", "salad"]

    # todo add random page html
    random_recipe_name = random.choice(recipe_list)
    index = recipe_list.index(random_recipe_name)

    return render_template("random.html", recipe_list=recipe_list, index=index)

@app.route("/log-in")
def log_in():
    return render_template("login.html")

@app.route("/json")
def json():
    return render_template("json.html")

@app.route("/background_process_test")
def background_process_test():
    print("hello")
    return("nothing")