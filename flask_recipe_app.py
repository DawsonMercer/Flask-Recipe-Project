import csv
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template("index.html")