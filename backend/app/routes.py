import os
import json
from flask import Blueprint, request, jsonify,Response
from app import db
from app.models import Usuario
from datetime import datetime
from flask_jwt_extended import verify_jwt_in_request,create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")


auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/api/usuarios", methods=["GET"])
@jwt_required()
def get_usuarios():
    usuarios = Usuario.query.all()
    usuarios_list = []
    for usuario in usuarios:
        usuarios_list.append({
            "id": usuario.id,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "email": usuario.email,
            "fecha_nacimiento": usuario.fecha_nacimiento.strftime("%Y-%m-%d"),
            "contrasena": usuario.contrasena,
            "fecha_registro": usuario.fecha_registro.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(usuarios_list), 200

@auth_bp.route("/api/usuarios", methods=["POST"])
def create_usuario():
    data = request.get_json()
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    email = data.get("email")
    fecha_nacimiento = data.get("fecha_nacimiento")
    contrasena = data.get("contrasena")

    if not nombre or not apellido or not email or not fecha_nacimiento or not contrasena:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    try:
        fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido"}), 400

    nuevo_usuario = Usuario(
        nombre=nombre,
        apellido=apellido,
        email=email,
        fecha_nacimiento=fecha_nacimiento,
        contrasena=contrasena,
        fecha_registro=datetime.now(),
        rol="user"
    )

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"message": "Usuario creado exitosamente"}), 201

@auth_bp.route("/api/usuarios/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({"message": "Usuario eliminado exitosamente"}), 200

@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    contrasena = data.get("contrasena")

    if not email or not contrasena:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    usuario = Usuario.query.filter_by(email=email, contrasena=contrasena).first()
    if not usuario:
        return jsonify({"error": "Credenciales inválidas"}), 401

    access_token = create_access_token(identity=str(usuario.id))
    return jsonify(access_token=access_token), 200

@auth_bp.route("/api/usuario", methods=["GET"])
@jwt_required()
def get_usuario():
    current_user = get_jwt_identity()
    
    usuario = Usuario.query.get(current_user)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "email": usuario.email,
        "fecha_nacimiento": usuario.fecha_nacimiento.strftime("%Y-%m-%d"),
        "fecha_registro": usuario.fecha_registro.strftime("%Y-%m-%d %H:%M:%S")
    }), 200

@auth_bp.route("/api/usuario", methods=["PATCH"])
@jwt_required()
def update_usuario():
    current_user = get_jwt_identity()
    usuario = Usuario.query.get(current_user)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    data = request.get_json()
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    email = data.get("email")
    fecha_nacimiento = data.get("fecha_nacimiento")

    if nombre:
        usuario.nombre = nombre
    if apellido:
        usuario.apellido = apellido
    if email:
        usuario.email = email
    if fecha_nacimiento:
        try:
            usuario.fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido"}), 400

    db.session.commit()

    return jsonify({"message": "Usuario actualizado exitosamente"}), 200

@auth_bp.route("/api/usuario-contra", methods=["PATCH"])
@jwt_required()
def update_contrasena():
    current_user = get_jwt_identity()
    usuario = Usuario.query.get(current_user)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    data = request.get_json()
    contrasena = data.get("contrasena")
    nueva_contrasena = data.get("nueva_contrasena")
    if not contrasena or not nueva_contrasena:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    if not contrasena == usuario.contrasena:
        return jsonify({"error": "La contraseña actual no es correcta"}), 401
    
    usuario.contrasena = nueva_contrasena
    db.session.commit()

    return jsonify({"message": "Contraseña actualizada exitosamente"}), 200
#