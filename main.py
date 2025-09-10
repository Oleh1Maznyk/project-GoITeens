from flask import Flask, flash, render_template, redirect
from flask_login import LoginManager, login_required, current_user, login_user, logout_user


app = Flask(__name__)