import os
from flask import Flask
from flask import render_template

app = Flask(__name__,template_folder='./templates', static_folder='./static')

@app.route("/")
def main():
    return render_template('index.html')
