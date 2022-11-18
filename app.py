import os

from flask import Flask
from flask import render_template
from flask import redirect
from flask import request

from database import User

from flask_login import LoginManager
from flask_login import login_user
from flask_login import login_required
from flask_login import logout_user

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

app = Flask(__name__)

app.config["SECRET_KEY"] = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.get(id=int(id))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login")


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def register():
    name = request.form.get("name")
    password = request.form.get("passwd")
    # User.create(name=name, password=password)
    generate_password = generate_password_hash(password, method="sha256")
    User.create(name=name, password=generate_password)
    return redirect("/login")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    name = request.form.get("name")
    password = request.form.get("passwd")
    user = User.get(name=name)
    # if user.password == password:
    #     login_user(user)
    #     return redirect("/")
    if check_password_hash(user.password, password):
        login_user(user)
        return redirect("/")
    return redirect("/login")


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
