from flask_wtf import FlaskForm
import wtforms

class SignUpForm(FlaskForm):
    username = wtforms.StringField(
        label="Логін користувача",
        validators=[wtforms.validators.DataRequired(), wtforms.validators.length(min=3)]
    )
    password = wtforms.PasswordField(
        label="Пароль",
        validators=[wtforms.validators.DataRequired(), wtforms.validators.length(min=6)]
    )
    fullname = wtforms.StringField(label="Ваше повне ім'я(за бажанням)")
    phone_number = wtforms.StringField(label="Ваше номер телефону(за баанням)")

    submit = wtforms.SubmitField(label="Зареєструватись")

class SigninForm(FlaskForm):
    username = wtforms.StringField(
        label="Логін користувача",
        validators=[wtforms.validators.DataRequired(), wtforms.validators.length(min=3)]
    )
    password = wtforms.PasswordField(
        label="Пароль",
        validators=[wtforms.validators.DataRequired(), wtforms.validators.length(min=6)]
    )

    submit = wtforms.SubmitField(label="Вхід")