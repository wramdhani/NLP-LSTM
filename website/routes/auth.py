from flask import Blueprint, render_template

auth = Blueprint(
   'auth', __name__,
   template_folder="../templates",
   static_folder="../static")

@auth.route('/login')
def home():
  return render_template("login.html")

@auth.route('/register')
def register():
    return render_template("register.html")