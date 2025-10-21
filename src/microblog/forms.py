from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from email_validator import validate_email, EmailNotValidError

class SignupForm(FlaskForm):
    """Formulario de registro de usuario con validación completa."""
    username = StringField("Nombre de usuario", validators=[
        DataRequired(message="El nombre de usuario es requerido"),
        Length(min=3, max=80, message="El nombre de usuario debe tener entre 3 y 80 caracteres")
    ])
    email = StringField("Correo electrónico", validators=[
        DataRequired(message="El correo electrónico es requerido"),
        Email(message="Por favor ingresa un correo electrónico válido"),
        Length(max=255, message="El correo electrónico debe tener menos de 255 caracteres")
    ])
    password = PasswordField("Contraseña", validators=[
        DataRequired(message="La contraseña es requerida"),
        Length(min=6, max=128, message="La contraseña debe tener entre 6 y 128 caracteres")
    ])
    submit = SubmitField("Registrarse")

    def validate_email(self, field):
        """Validación personalizada de email usando la librería email-validator."""
        try:
            validate_email(field.data)
        except EmailNotValidError:
            raise ValidationError("Por favor ingresa un correo electrónico válido")

class LoginForm(FlaskForm):
    """Formulario de inicio de sesión con funcionalidad recordarme."""
    email = StringField("Correo electrónico", validators=[
        DataRequired(message="El correo electrónico es requerido"),
        Email(message="Por favor ingresa un correo electrónico válido"),
        Length(max=255, message="El correo electrónico debe tener menos de 255 caracteres")
    ])
    password = PasswordField("Contraseña", validators=[
        DataRequired(message="La contraseña es requerida")
    ])
    remember_me = BooleanField("Recordarme")
    submit = SubmitField("Iniciar sesión")

class PostForm(FlaskForm):
    """Formulario de creación de post con validación completa."""
    title = StringField("Título", validators=[
        DataRequired(message="El título es requerido"),
        Length(min=3, max=255, message="El título debe tener entre 3 y 255 caracteres")
    ])
    content = TextAreaField("Contenido", validators=[
        DataRequired(message="El contenido es requerido"),
        Length(min=10, message="El contenido debe tener al menos 10 caracteres")
    ])
    excerpt = TextAreaField("Resumen", validators=[
        Length(max=500, message="El resumen debe tener menos de 500 caracteres")
    ])
    category = SelectField("Categoría", choices=[
        ('', 'Selecciona una categoría'),
        ('technology', 'Tecnología'),
        ('lifestyle', 'Estilo de vida'),
        ('travel', 'Viajes'),
        ('food', 'Comida'),
        ('sports', 'Deportes'),
        ('business', 'Negocios'),
        ('education', 'Educación'),
        ('other', 'Otro')
    ])
    submit = SubmitField("Crear Post")

class EditPostForm(FlaskForm):
    """Formulario de edición de post con la misma validación que la creación."""
    title = StringField("Título", validators=[
        DataRequired(message="El título es requerido"),
        Length(min=3, max=255, message="El título debe tener entre 3 y 255 caracteres")
    ])
    content = TextAreaField("Contenido", validators=[
        DataRequired(message="El contenido es requerido"),
        Length(min=10, message="El contenido debe tener al menos 10 caracteres")
    ])
    excerpt = TextAreaField("Resumen", validators=[
        Length(max=500, message="El resumen debe tener menos de 500 caracteres")
    ])
    category = SelectField("Categoría", choices=[
        ('', 'Selecciona una categoría'),
        ('technology', 'Tecnología'),
        ('lifestyle', 'Estilo de vida'),
        ('travel', 'Viajes'),
        ('food', 'Comida'),
        ('sports', 'Deportes'),
        ('business', 'Negocios'),
        ('education', 'Educación'),
        ('other', 'Otro')
    ])
    is_published = BooleanField("Publicado")
    submit = SubmitField("Actualizar Post")
