from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length

# Formulario para login de usuario
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

# Formulario para registrar un nuevo usuario
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])

    role = SelectField(
        'Role',
        choices=[('Lector', 'Lector'), ('Bibliotecario', 'Bibliotecario')],
        validators=[DataRequired()])
    submit = SubmitField('Register')

# Formulario para cambiar la contraseña del usuario
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Current password', validators=[DataRequired()])
    new_password = PasswordField('New password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm new password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Password')

# Formulario para crear o editar un libro
class LibroForm(FlaskForm):
    titulo = StringField('Book title', validators=[DataRequired()])
    autor = StringField('Author name', validators=[DataRequired()])
    categoria = StringField('Book category', validators=[DataRequired()])
    estado = SelectField('Status',choices=[('Disponible', 'Disponible'), ('Prestado', 'Prestado')],validators=[DataRequired()] )
    isbn = StringField('Book ISBN', validators=[DataRequired()])
    año_publicacion = IntegerField('Publication Year', validators=[DataRequired()])
    submit = SubmitField('Save')
