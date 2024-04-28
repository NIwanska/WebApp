from flask import (
    render_template,
    Blueprint,
    request,
    redirect,
    url_for,
    flash,
)
from ..models import db, AuthUser
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash


bp = Blueprint(
    "auth",
    __name__,
    template_folder="templates/",
    static_folder="static",
    url_prefix="/auth",
)


@bp.route("/signup")
def signup():
    return render_template("auth/signup.html")


@bp.route("/signup", methods=["POST"])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")

    user = AuthUser.query.filter_by(
        email=email
    ).first()  # if this returns a user, then the email already exists in database

    if (
        user
    ):  # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for("auth.signup"))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = AuthUser(
        email=email,
        username=username,
        password=generate_password_hash(password, method="pbkdf2:sha256"),
    )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))


@bp.route("/login")
def login():
    return render_template("auth/login.html")


@bp.route("/login", methods=["POST"])
def login_post():
    # login code goes here
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = AuthUser.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(
            url_for("auth.login")
        )  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for("main.home"))
