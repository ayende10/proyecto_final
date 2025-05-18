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

@main.route('/libro', methods=['GET'])
def listar_libro():
    """
    Retorna una lista de libros (JSON).
    """
    libro = Libro.query.all()

    data = [
        {'id': libro.id, 'titulo': libro.titulo, 'autor': libro.autor, 'bibliotecario_id': libro.bibliotecario_id}
        for libro in libro
    ]
    return jsonify(data), 200


@main.route('/libro/<int:id>', methods=['GET'])
def listar_un_libro(id):
    """
    Retorna un solo libro por su ID (JSON).
    """
    libro = Libro.query.get_or_404(id)

    data = {
        'id': libro.id,
        'titulo': libro.titulo,
        'autor': libro.autor,
        'bibliotecario_id': libro.bibliotecario_id
    }

    return jsonify(data), 200


@main.route('/libro', methods=['POST'])
def crear_libro():
    """
    Crea un libro sin validación.
    Espera JSON con 'titulo', 'autor' y 'bibliotecario_id'.
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    nuevo_libro = Libro(
        titulo=data.get('titulo'),
        autor=data.get('autor'),
        bibliotecario_id=data.get('bibliotecario_id')  # sin validación de usuario
    )

    db.session.add(nuevo_libro)
    db.session.commit()

    return jsonify({'message': 'Libro creado', 'id': nuevo_libro.id, 'bibliotecario_id': nuevo_libro.bibliotecario_id}), 201

@main.route('/libro/<int:id>', methods=['PUT'])
def actualizar_libro(id):
    """
    Actualiza un libro sin validación de usuario o permisos.
    """
    libro = Libro.query.get_or_404(id)
    data = request.get_json()

    libro.titulo = data.get('titulo', libro.titulo)
    libro.autor = data.get('autor', libro.autor)
    libro.bibliotecario_id = data.get('bibliotecario_id', libro.bibliotecario_id)

    db.session.commit()

    return jsonify({'message': 'Libro actualizado', 'id': libro.id}), 200

@main.route('/libro/<int:id>', methods=['DELETE'])
def eliminar_libro(id):
    """
    Elimina un libro sin validación de permisos.
    """
    libro = Libro.query.get_or_404(id)
    db.session.delete(libro)
    db.session.commit()

    return jsonify({'message': 'Libro eliminado', 'id': libro.id}), 200