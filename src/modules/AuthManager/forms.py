from wtforms import Form, StringField, PasswordField, validators, RadioField


class fRegistration(Form):
    login = StringField('Логин', [validators.Length(min=3, max=15), validators.required()])
    password = PasswordField('Пароль', [
        validators.Length(min=6, max=30),
        validators.required(),
        validators.EqualTo('confirm_password', message='Пароли должны совпадать')]
    )
    confirm_password = PasswordField('Повторите пароль', validators=[
        validators.Length(min=6, max=30),
        validators.required()
    ])
    first_name = StringField('Имя', [validators.Length(min=2, max=30), validators.required()])
    second_name = StringField('Фамилия', [validators.Length(min=2, max=30), validators.required()])


class fLogin(Form):
    login = StringField('Логин', [validators.Length(min=3, max=15), validators.required()])
    password = PasswordField('Пароль', [validators.Length(min=6, max=30), validators.required()])


class fResetPW(Form):
    login = StringField('Логин', [validators.Length(min=3, max=15), validators.required()])


class fEditProfile(Form):
    first_name = StringField('Имя', [validators.Length(min=2, max=30), validators.required()])
    secon_dname = StringField('Фамилия', [validators.Length(min=2, max=30), validators.required()])
    login = StringField('Логин', [validators.Length(min=3, max=15), validators.required()])