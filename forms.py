from flask_wtf import FlaskForm
import wtforms


class SignUpForm(FlaskForm):
    username = wtforms.StringField(
        label="Логін користувача",
        validators=[wtforms.validators.DataRequired(), wtforms.validators.Length(min=3)]
    )
    password = wtforms.PasswordField(
        label="Пароль",
        validators=[wtforms.validators.DataRequired(), wtforms.validators.Length(min=6)]
    )
    first_name = wtforms.StringField(
        label="Ваше ім'я (за бажанням)",
        validators=[wtforms.validators.Optional()]
    )
    last_name = wtforms.StringField(
        label="Ваше прізвище (за бажанням)",
        validators=[wtforms.validators.Optional()]
    )
    phone_number = wtforms.StringField(
        label="Ваш номер телефону (за бажанням)",
        validators=[wtforms.validators.Optional()]
    )

    submit = wtforms.SubmitField(label="Зареєструватись")


class SigninForm(FlaskForm):
    username = wtforms.StringField(
        label="Логін користувача",
        validators=[wtforms.validators.DataRequired(), wtforms.validators.Length(min=3)]
    )
    password = wtforms.PasswordField(
        label="Пароль",
        validators=[wtforms.validators.DataRequired(), wtforms.validators.Length(min=6)]
    )

    submit = wtforms.SubmitField(label="Вхід")
