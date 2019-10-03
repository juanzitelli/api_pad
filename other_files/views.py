# -*- coding: utf-8 -*-
import os
from flask import Blueprint, render_template

static_folder = os.path.join(os.pardir, 'static')
home = Blueprint('home',__name__, template_folder='template', static_folder=static_folder)

@home.route('/')
def index():
    return render_template('index.html')