from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import db, Libro

# Blueprint para pruebas con libros
main = Blueprint('main', __name__)

@main.route('/')  
@main.route('/dashboard')
def index():
    """ Página de inicio pública. """
    return '<h1>Corriendo en Modo de Prueba.</h1>'

@main.route('/libro', methods=['GET'])
def listar_libro():
    """ 
    Retorna una lista de libros en formato JSON. 
    """
    libro = Libro.query.all()

    data = [
        {'id': libro.id, 'titulo': libro.titulo, 'descripcion': libro.descripcion, 'bibliotecario_id': libro.bibliotecario_id}
        for libro in libro
    ]
    return jsonify(data), 200

@main.route('/libro/<int:id>', methods=['GET'])
def listar_un_libro(id):
    """ 
    Retorna un solo libro por su ID en formato JSON. 
    """
    libro = Libro.query.get_or_404(id)

    data = {
        'id': libro.id,
        'titulo': libro.titulo,
        'descripcion': libro.descripcion,
        'bibliotecario_id': libro.bibliotecario_id
    }

    return jsonify(data), 200

@main.route('/libro', methods=['POST'])
@login_required
def crear_libro():
    """ 
    Crea un libro con validación de usuario. Solo Admins o Bibliotecarios pueden crear. 
    """
    if current_user.role.name not in ['Admin', 'Bibliotecario']:
        return jsonify({'error': 'No tienes permisos para crear un libro.'}), 403

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    libro = Libro(
        titulo=data.get('titulo'),
        descripcion=data.get('descripcion'),
        bibliotecario_id=current_user.id
    )

    db.session.add(libro)
    db.session.commit()

    return jsonify({'message': '📖 Libro creado exitosamente.', 'id': libro.id}), 201

@main.route('/libro/<int:id>', methods=['PUT'])
@login_required
def actualizar_libro(id):
    """ 
    Actualiza un libro. Solo Admins o Bibliotecarios con permisos pueden modificar. 
    """
    libro = Libro.query.get_or_404(id)

    if current_user.role.name not in ['Admin', 'Bibliotecario'] and libro.bibliotecario_id != current_user.id:
        return jsonify({'error': 'No tienes permiso para actualizar este libro.'}), 403

    data = request.get_json()
    libro.titulo = data.get('titulo', libro.titulo)
    libro.descripcion = data.get('descripcion', libro.descripcion)
    libro.bibliotecario_id = data.get('bibliotecario_id', libro.bibliotecario_id)

    db.session.commit()

    return jsonify({'message': '📖 Libro actualizado correctamente.', 'id': libro.id}), 200

@main.route('/libro/<int:id>', methods=['DELETE'])
@login_required
def eliminar_libro(id):
    """ 
    Elimina un libro. 
    """