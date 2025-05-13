from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.forms import LibroForm, ChangePasswordForm
from app.models import db, Libro, User

# Blueprint principal que maneja el dashboard, gestión de cursos y cambio de contraseña
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """ Página de inicio pública (home)."""
    return render_template('index.html')

@main.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    """
    Permite al usuario autenticado cambiar su contraseña.
    """
    form = ChangePasswordForm()

    if form.validate_on_submit():
        # Verifica que la contraseña actual sea correcta
        if not current_user.check_password(form.old_password.data):
            flash('Current password is incorrect.')  # 🔁 Traducido
            return render_template('cambiar_password.html', form=form)

        # Actualiza la contraseña y guarda
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('✅ Password updated successfully.')  # 🔁 Traducido
        return redirect(url_for('main.dashboard'))

    return render_template('cambiar_password.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    """
    Panel principal del usuario. Muestra los libros si no es lector.
    """
    if current_user.role.name in ['Admin', 'Lector', 'Bibliotecario']:
        libros = Libro.query.all()
    else:
        libros = []

    return render_template('dashboard.html', libros=libros)

@main.route('/libros', methods=['GET', 'POST'])
@login_required
def libro():
    """
    Permite crear un nuevo libro. Solo disponible para bibliotecarios o admins.
    """
    form = LibroForm()
    if form.validate_on_submit():
        libro = Libro(
            titulo=form.titulo.data,
            autor=form.autor.data,
            isbn=form.isbn.data,
            categoria=form.categoria.data,
            estado=form.estado.data,
            año_publicacion=form.año_publicacion.data

        
        )
        db.session.add(libro)
        db.session.commit()
        flash("Book created successfully.")  # 🔁 Traducido
        return redirect(url_for('main.dashboard'))

    return render_template('libro_form.html', form=form)

@main.route('/libros/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_libro(id):
    """
    Permite editar un libro existente. Solo si es admin o el bibliotecario.
    """
    libro = Libro.query.get_or_404(id)

    # Validación de permisos:
    # El admin puede editar cualquier libro.
    # El bibliotecario solo puede editar los libros que él mismo ha creado (libro.bibliotecario_id == current_user.id).
    if current_user.role.name == 'Admin' or libro.bibliotecario_id == current_user.id:
        form = LibroForm(obj=libro)

        if form.validate_on_submit():
            libro.titulo = form.titulo.data
            libro.autor = form.autor.data
            libro.isbn = form.isbn.data
            libro.categoria = form.categoria.data
            libro.estado = form.estado.data
            libro.año_publicacion = form.año_publicacion.data

            db.session.commit()
            flash("Book updated successfully.")  # 🔁 Traducido
            return redirect(url_for('main.dashboard'))
        
        return render_template('libro_form.html', form=form, editar=True)
    else:
        flash('You do not have permission to edit this book.')  # 🔁 Traducido
        return redirect(url_for('main.dashboard'))

@main.route('/libros/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_libro(id):
    """
    Elimina un libro si el usuario es admin o bibliotecario.
    """
    libro = Libro.query.get_or_404(id)

    # Validación de permisos: El admin puede eliminar cualquier libro.
    # El bibliotecario solo puede eliminar los libros que él mismo ha creado.
    if current_user.role.name not in ['Admin', 'Bibliotecario'] or (
        libro.bibliotecario_id != current_user.id and current_user.role.name != 'Admin'):
        flash('You do not have permission to delete this book.')  # 🔁 Traducido
        return redirect(url_for('main.dashboard'))

    db.session.delete(libro)
    db.session.commit()
    flash("Book deleted successfully.")  # 🔁 Traducido
    return redirect(url_for('main.dashboard'))

@main.route('/usuarios')
@login_required
def listar_usuarios():
    if current_user.role.name != 'Admin':
        flash("You do not have permission to view this page.")
        return redirect(url_for('main.dashboard'))

    # Obtener instancias completas de usuarios con sus roles (no usar .add_columns)
    usuarios = User.query.join(User.role).all()

    return render_template('usuarios.html', usuarios=usuarios)
