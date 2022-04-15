import csv
import os
import random
from flask import Flask, render_template, request, redirect, url_for
# TODO HASH PASSOWRDS
# TODO ADD LOG IN FEATURE sql?
app = Flask(__name__)
# recipe_list = []
# recipe_dict = {}


#venv\Scripts\activate
#$env:FLASK_APP = "flask_recipe_app"
# $env:FLASK_ENV = "development"
#flask run


@app.route("/")
def main_page():
    recipe_list, recipe_dict = read_csv()
    return render_template("index.html")


@app.route("/view-all")
def view_all():
    recipe_list, recipe_dict = read_csv()
    print(recipe_list)
    print(recipe_dict)
    return render_template("viewAll.html", recipe_list=recipe_list)

@app.route("/next/<string:recipe_name>")
def next_recipe(recipe_name):
    recipe_list, recipe_dict = read_csv()
    current_index = recipe_list.index(recipe_name)
    if current_index+1 > len(recipe_list)-1:
        current_index = 0
        next_recipe = recipe_list[current_index]
    else:
        next_recipe = recipe_list[current_index+1]
    current_recipe = recipe_dict[next_recipe]
    ingredients = current_recipe[2].split("-")
    return render_template("recipe.html", recipe_name=next_recipe, current_recipe=current_recipe, ingredients=ingredients)


@app.route("/prev/<string:recipe_name>")
def prev_recipe(recipe_name):
    recipe_list, recipe_dict = read_csv()
    current_index = recipe_list.index(recipe_name)
    if current_index-1 < 0 :
        current_index = len(recipe_list)-1
        prev_recipe = recipe_list[current_index]
    else:
        prev_recipe = recipe_list[current_index-1]
    current_recipe = recipe_dict[prev_recipe]
    ingredients = current_recipe[2].split("-")
    return render_template("recipe.html", recipe_name=prev_recipe, current_recipe=current_recipe, ingredients=ingredients)


@app.route("/recipe/<string:recipe_name>")
def recipe(recipe_name):
    recipe_list, recipe_dict = read_csv()
    print(recipe_list)
    if(recipe_name in recipe_list):
        current_recipe = recipe_dict[recipe_name]
        ingredients = current_recipe[2].split("-")

        print("current recipe", current_recipe)
        return render_template("recipe.html", recipe_name=recipe_name, current_recipe=current_recipe, ingredients=ingredients)
    else:
        return render_template("error.html")


@app.route("/pick-random")
def pick_random():
    recipe_list, recipe_dict = read_csv()
    random_recipe_name = random.choice(recipe_list)
    index = recipe_list.index(random_recipe_name)

    return render_template("random.html", recipe_list=recipe_list, index=index, recipe_dict=recipe_dict)

@app.route("/log-in")
def log_in():
    # add functionality and redirect to main page for log in
    return render_template("login.html")


app.config["UPLOAD_PATH"] = "static/images"
@app.route("/upload-recipe", methods=["GET", "POST"])
# @app.route("/upload-recipe")
def upload_recipe():
    if request.method == "POST":

        recipe_name = request.form.get("recipe_name")
        description = request.form.get("description")
        recipe_ingredients = request.form.get("recipe_ingredients")
        prepare = request.form.get("prepare")
        servings = request.form.get("servings")
        # print(recipe_name,description,recipe_ingredients,servings)
        uploaded_file = request.files["recipe_image"]
        if uploaded_file.filename != "":
            uploaded_file.save(os.path.join(app.config["UPLOAD_PATH"], uploaded_file.filename))
            # fixme it adds double csv file i am unsure exactly what is happening here
            recipe_list, recipe_dict = read_csv()

            recipe_dict[recipe_name] = [description, uploaded_file.filename, recipe_ingredients, prepare, servings]
            recipe_list.append(recipe_name)
            write_csv(recipe_dict)
        return redirect(url_for("main_page"))
    else:
        return render_template("upload_recipe.html")


@app.route("/remove-recipe")
def remove_recipe():
    recipe_list, recipe_dict = read_csv()
    return render_template("remove_recipe.html", recipe_list=recipe_list)

@app.route("/delete/<recipe>")
def delete(recipe):
    recipe_list, recipe_dict = read_csv()
    print("recipe to delete is", recipe)
    print("recipe list", recipe_list)
    print("recipe dict", recipe_dict)
    try:
        if recipe in recipe_list and recipe in recipe_dict:
            remove = recipe_list.index(recipe)
            recipe_list.pop(remove)
            del recipe_dict[recipe]
            write_csv(recipe_dict)

        return redirect(url_for("remove_recipe"))
    except:
        return "Trouble deleting recipe. Try again."


def write_csv(recipe_dict):
    with open("recipes.csv", "w", newline="") as file:
        writer = csv.writer(file)
        for key, value in recipe_dict.items():
            writer.writerow([key, value[0], value[1], value[2], value[3], value[4]])


def read_csv():
    recipe_images = []
    recipe_list = []
    recipe_dict = {}
    with open("recipes.csv", newline="") as file:
        reader = csv.reader(file)
        # print(recipe_dict)
        for row in reader:
            recipe_dict[row[0]] = [row[1], row[2], row[3], row[4], row[5]]
            recipe_list.append(row[0])
            print(recipe_list)
            print(recipe_dict)
        return recipe_list, recipe_dict


