from flask import Flask, flash, render_template, redirect, url_for, request
from flask_login import LoginManager, login_required, current_user, login_user, logout_user


from forms import SigninForm, SignUpForm
from models import User, db

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def get():
    return render_template("login.html")


@app.route("/signUp/", methods=["GET", "POST"])
def sign_up():
    sign_up_form = SignUpForm()

    if sign_up_form.validate_on_submit():
        username = sign_up_form.username.data
        password = sign_up_form.password.data
        fullname = sign_up_form.fullname.data
        phone_number = sign_up_form.phone_number.data

        user = User(
    username=username,
    password=password,
    fullname=fullname,
    phone_number=phone_number,
    )
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("Ви успішно зареєструвались")
        return redirect(url_for("index"))

    return render_template("sign_up.html", form=sign_up_form)

@app.route("/signIn/", methods=["GET", "POST"], endpoint="sign_in")
def sign_in_view():
    form = SigninForm()
    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.is_verify_password(form.password.data):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Логін або пароль невірні")
            return redirect(url_for("sign_in"))

    return render_template("sign_in.html", form=form)


@app.get("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("sign_in"))


# with app.app_context():
#     db.drop_all()
#     db.create_all()



if __name__ == "main":
    app.run(debug=True)