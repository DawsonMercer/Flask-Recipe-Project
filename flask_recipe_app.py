import csv
import os
import random
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
recipe_list = []
recipe_dict = {}


#venv\Scripts\activate
#$env:FLASK_APP = "flask_recipe_app"
# $env:FLASK_ENV = "development"
#flask run


@app.route("/")
def main_page():
    read_csv()
    return render_template("index.html")


@app.route("/view-all")
def view_all():
    return render_template("viewAll.html", recipe_list=recipe_list)

@app.route("/recipe/<string:recipe_name>")
def recipe(recipe_name):
    if(recipe_name in recipe_list):
        current_recipe = recipe_dict[recipe_name]
        ingredients = current_recipe[2].split("-")

        print("current recipe", current_recipe)
        return render_template("recipe.html", recipe_name=recipe_name, current_recipe=current_recipe, ingredients=ingredients)
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

def read_csv():
    recipe_images = []
    with open("recipes.csv", newline="") as file:
        reader = csv.reader(file)
        # print(recipe_dict)
        for row in reader:
            recipe_dict[row[0]] = [row[1], row[2], row[3], row[4], row[5]]
            recipe_list.append(row[0])
            print(recipe_list)
            print(recipe_dict)