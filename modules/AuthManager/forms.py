from wtforms import Form, StringField, PasswordField, validators, RadioField


class fRegistration(Form):
    username = StringField('Имя пользователя', [validators.Length(min=2, max=15), validators.required()])
    password = PasswordField('Пароль', [
        validators.Length(min=6, max=30),
        validators.required(),
        validators.EqualTo('confirm_password', message='Пароли должны совпадать')]
    )
    confirm_password = PasswordField('Повторите пароль', validators=[
        validators.Length(min=6, max=30),
        validators.required()
    ])
    firstname = StringField('Имя', [validators.Length(min=2, max=30), validators.required()])
    secondname = StringField('Фамилия', [validators.Length(min=2, max=30), validators.required()])


class fLogin(Form):
    username = StringField('Имя пользователя', [validators.Length(min=3, max=25), validators.required()])
    password = PasswordField('Пароль', [validators.Length(min=6, max=30), validators.required()])


class fResetPW(Form):
    username = StringField('Имя пользователя', [validators.Length(min=3, max=25), validators.required()])
