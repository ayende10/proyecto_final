from flask import Blueprint, request, jsonify
from app.models import db, Libro

# Blueprint solo con endpoints de prueba para cursos
main = Blueprint('main', __name__)

@main.route('/') # Ambas rutas llevan al mismo lugar
@main.route('/dashboard')
def index():
    """
    Página de inicio pública (home).
    """
    return '<h1>Corriendo en Modo de Prueba.</h1>'

@main.route('/libros', methods=['GET'])
def listar_libro():
    """
    Retorna una lista de libros (JSON).
    """
    libro = libro.query.all()

    data = [
        {'id': libro.id, 'titulo': libro.titulo, 'descripcion': libro.descripcion, 'bibliotecario_id': libro.bibliotecario_id}
        for libro in libro
    ]
    return jsonify(data), 200


@main.route('/libros/<int:id>', methods=['GET'])
def listar_un_libro(id):
    """
    Retorna un solo libro por su ID (JSON).
    """
    libro = libro.query.get_or_404(id)

    data = {
        'id': libro.id,
        'titulo': libro.titulo,
        'descripcion': libro.descripcion,
        'bibliotecario_id': libro.bibliotecario_id
    }

    return jsonify(data), 200


@main.route('/libros', methods=['POST'])
def crear_libro():
    """
    Crea un libro sin validación.
    Espera JSON con 'titulo', 'descripcion' y 'bibliotecario_id'.
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    libro = libro(
        titulo=data.get('titulo'),
        descripcion=data.get('descripcion'),
        bibliotecario_id=data.get('bibliotecario_id')  # sin validación de usuario
    )

    db.session.add(libro)
    db.session.commit()

    return jsonify({'message': 'Libro creado', 'id': libro.id, 'bibliotecario_id': libro.bibliotecario_id}), 201

@main.route('/libros/<int:id>', methods=['PUT'])
def actualizar_libro(id):
    """
    Actualiza un libro sin validación de usuario o permisos.
    """
    libro = libro.query.get_or_404(id)
    data = request.get_json()

    libro.titulo = data.get('titulo', libro.titulo)
    libro.descripcion = data.get('descripcion', libro.descripcion)
    libro.profesor_id = data.get('bibliotecario_id', libro.bibliotecario_id)

    db.session.commit()

    return jsonify({'message': 'Libro actualizado', 'id': libro.id}), 200

@main.route('/libros/<int:id>', methods=['DELETE'])
def eliminar_libro(id):
    """
    Elimina un libro sin validación de permisos.
    """
    libro = libro.query.get_or_404(id)
    db.session.delete(libro)
    db.session.commit()

    return jsonify({'message': 'Libro eliminado', 'id': libro.id}), 200
