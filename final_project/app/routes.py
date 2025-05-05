from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.forms import LibroForm, ChangePasswordForm
from app.models import db, Libro, User

# Blueprint principal que maneja el dashboard y libros
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """ Página de inicio pública. """
    return render_template('index.html')

@main.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    """ 
    Permite al usuario autenticado cambiar su contraseña.
    """
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('❌ La contraseña actual es incorrecta.', 'error')
            return redirect(url_for('main.cambiar_password'))

        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('✅ Contraseña actualizada correctamente.', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('cambiar_password.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    """ 
    Panel principal del usuario con libros visibles según su rol. 
    """
    libros = Libro.query.all() if current_user.role.name == 'Lector' else Libro.query.filter_by(bibliotecario_id=current_user.id).all()
    return render_template('dashboard.html', libros=libros)

@main.route('/libro/crear', methods=['GET', 'POST'])
@login_required
def crear_libro():
    """ 
    Permite crear un nuevo libro (solo bibliotecarios o admins). 
    """
    if current_user.role.name not in ['Admin', 'Bibliotecario']:
        flash("❌ No tienes permisos para crear libros.", "error")
        return redirect(url_for('main.dashboard'))

    form = LibroForm()
    if form.validate_on_submit():
        libro = Libro(
            titulo=form.titulo.data,
            descripcion=form.descripcion.data,
            bibliotecario_id=current_user.id
        )
        db.session.add(libro)
        db.session.commit()
        flash("📖 Libro creado exitosamente.", "success")
        return redirect(url_for('main.dashboard'))

    return render_template('libro_form.html', form=form)

@main.route('/libro/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_libro(id):
    """ 
    Permite editar un libro (solo bibliotecarios o admins). 
    """
    libro = Libro.query.get_or_404(id)

    if current_user.role.name not in ['Admin', 'Bibliotecario'] and libro.bibliotecario_id != current_user.id:
        flash("❌ No tienes permiso para editar este libro.", "error")
        return redirect(url_for('main.dashboard'))

    form = LibroForm(obj=libro)

    if form.validate_on_submit():
        libro.titulo = form.titulo.data
        libro.descripcion = form.descripcion.data
        db.session.commit()
        flash("📖 Libro actualizado exitosamente.", "success")
        return redirect(url_for('main.dashboard'))

    return render_template('libro_form.html', form=form, editar=True)

@main.route('/libro/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_libro(id):
    """ 
    Elimina un libro (solo bibliotecarios o admins). 
    """
    libro = Libro.query.get_or_404(id)

    if current_user.role.name not in ['Admin', 'Bibliotecario'] and libro.bibliotecario_id != current_user.id:
        flash("❌ No tienes permiso para eliminar este libro.", "error")
        return redirect(url_for('main.dashboard'))

    db.session.delete(libro)
    db.session.commit()
    flash("🗑️ Libro eliminado correctamente.", "success")
    return redirect(url_for('main.dashboard'))

@main.route('/usuarios')
@login_required
def listar_usuarios():
    """ 
    Muestra la lista de usuarios (solo admins). 
    """
    if current_user.role.name != 'Admin':
        flash("❌ No tienes permiso para ver esta página.", "error")
        return redirect(url_for('main.dashboard'))

    usuarios = User.query.all()
    return render_template('usuarios.html', usuarios=usuarios)
