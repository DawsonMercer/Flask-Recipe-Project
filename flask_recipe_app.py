import csv
import os
import random
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, ValidationError, Length

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

# TODO HASH PASSOWRDS
# TODO ADD LOG IN FEATURE sql?
# TODO ADD FILE VERIFICATION FOR PHOTO
app = Flask(__name__)
bcrypt = Bcrypt(app)
# recipe_list = []
# recipe_dict = {}

#venv\Scripts\activate
#$env:FLASK_APP = "flask_recipe_app"
# $env:FLASK_ENV = "development"
#flask run

#create a new db
# python in terminal
# from flask_recipe_all import db
# db.create_all()
# exit()


# add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# secret key
app.config['SECRET_KEY'] = 'my secret key'
db = SQLAlchemy(app)
# TODO THIS IS WHERE I LEFT OFF 24:14 IN THE VID - https://www.youtube.com/watch?v=71EU8gnZqZQ
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# create a db model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    # date_added = db.Column(db.DateTime, default=datetime.utcnow())
    password = db.Column(db.String(80), nullable=False)

    #creat a string
    def __repr__(self):
        return '<Name %r>' % self.name


@app.route('/delete/<int:id>')
def delete_user(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = RegisterForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Sucessfully!")
        our_users = Users.query.order_by(Users.id)
        return render_template("add_user.html", form=form, our_users=our_users)
    except:
        flash("Error deleting User")
        our_users = Users.query.order_by(Users.id)
        return render_template("add_user.html", form=form, our_users=our_users)




class RegisterForm(FlaskForm):
    # todo add Email inside validators list
    username = StringField("Email", validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=1, max=40)])
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = Users.query.filter_by(username=username.data).first()

        if existing_user_username:
            raise ValidationError("That username already exists. Please choose another")

class LogInForm(FlaskForm):
    # todo add Email inside validators list
    username = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


# creat form class
class NamerForm(FlaskForm):
    name = StringField("Name:", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route("/user/add", methods=['GET', 'POST'])
def add_user():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        print(f"HASHED PAASWORD {hashed_password}")
        new_user = Users(username= form.username.data, password = hashed_password)
        db.session.add(new_user)
        db.session.commit()
        our_users = Users.query.order_by(Users.id)
        return redirect(url_for("login"))
    our_users = Users.query.order_by(Users.id)
    return render_template("add_user.html", form=form, our_users=our_users)

# fixme remove this, jsut for testing
# @app.route("/name", methods=['GET', 'POST'])
# def name():
#     name = None
#     form = NamerForm()
#     # validate form
#     if form.validate_on_submit():
#         name = form.name.data
#         form.name.data = ''
#         flash("Successful account created")
#     return render_template("name.html", name=name, form=form)

@app.route("/")
def main_page():
    recipe_list, recipe_dict = read_csv()
    return render_template("index.html")


@app.route("/view-all")
def view_all():
    recipe_list, recipe_dict = read_csv()
    print(recipe_list)
    print(recipe_dict)
    return render_template("viewAll.html", recipe_list=recipe_list, recipe_dict=recipe_dict)

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


@app.route("/log-in", methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username = form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    # add functionality and redirect to main page for log in
    return render_template("login.html", form=form)

@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    # username = db.session["username"]

    our_users = Users.query.order_by(Users.id)
    return render_template('dashboard.html', our_users=our_users)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# TODO ADD FILE VERIFICATION FOR PHOTO
# TODO ADD FILE VERIFICATION FOR PHOTO
# TODO ADD FILE VERIFICATION FOR PHOTO
# TODO ADD FILE VERIFICATION FOR PHOTO
# TODO ADD FILE VERIFICATION FOR PHOTO
# TODO ADD FILE VERIFICATION FOR PHOTO

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


