from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from datetime import datetime
import sqlalchemy.exc
import werkzeug

from src.database import db

from src.models.outgo import Outgo, outgo_schema, outgoes_schema
from src.models.user import User, user_schema


outgoes = Blueprint("outgoes",
                    __name__,
                    url_prefix="/api/v1/outgoes")

#Endpoint para crear un egreso
@outgoes.post("/")
@jwt_required()
def create():
    post_data = None
    
    try:
        post_data = request.get_json()
        
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Post body JSON data not found",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
        
    user_id = user_schema.dump(get_jwt_identity())["id"]
    user = User.query.filter_by(id=user_id).first()
    
    outgo = Outgo(description = request.get_json().get("description", None),
                  date = request.get_json().get("date", None),
                  hour = request.get_json().get("hour", None),
                  value = request.get_json().get("value", None),
                  user_id = user.id)
    
    try:
        db.session.add(outgo)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    return {"data": outgo_schema.dump(outgo)}, HTTPStatus.CREATED

#Endpoint para listar todos los egresos de un usuario en sesión según un rango de fechas
@outgoes.get("/by_dates")
@jwt_required()
def read_by_date():
    dates_data = None
    
    try:
        dates_data = request.get_json()
        
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Get body JSON data not found",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
        
    id = user_schema.dump(get_jwt_identity())["id"]
    user = User.query.filter_by(id=id).first()
    
    start_date = request.get_json().get("start_date", None)
    end_date = request.get_json().get("end_date", None)
    
    outgoes = Outgo.query.filter_by(user_id=user.id).filter(Outgo.date >= start_date).filter(Outgo.date <= end_date).all()
    
    return {"data": outgoes_schema.dump(outgoes)}, HTTPStatus.OK

#Endpoint para listar todos los egresos del usuario en sesión
@outgoes.get("/")
@jwt_required()
def read_all_of_a_user():
    user_id = user_schema.dump(get_jwt_identity())["id"]
    user = User.query.filter_by(id=user_id).first()
    
    outgoes = Outgo.query.filter_by(user_id=user.id).all()
    
    return {"data": outgoes_schema.dump(outgoes)}, HTTPStatus.OK

#Endpoint para editar un egreso
@outgoes.put("/<int:id>")
@jwt_required()
def update(id):
    post_data = None
    
    try:
        post_data = request.get_json()
    
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Put body JSON data not found",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
        
    outgo = Outgo.query.filter_by(id=id).first()
    
    if(not outgo):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    
    user_id = user_schema.dump(get_jwt_identity())["id"]
    user = User.query.filter_by(id=user_id).first()
    
    if(not outgo.user_id==user.id):
        return {"error":"Outgo not valid"}, HTTPStatus.BAD_REQUEST
    
    outgo.description = request.get_json().get('description', outgo.description)
    outgo.date        = request.get_json().get('date', outgo.date)
    outgo.hour        = request.get_json().get('hour', outgo.hour)
    outgo.value       = request.get_json().get('value', outgo.value)
    
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    return {"data": outgo_schema.dump(outgo)}, HTTPStatus.OK

#Endpoint para remover un egreso
@outgoes.delete("/<int:id>")
@jwt_required()
def delete(id):
    outgo = Outgo.query.filter_by(id=id).first()
    
    if(not outgo):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND

    user_id = user_schema.dump(get_jwt_identity())["id"]
    user = User.query.filter_by(id=user_id).first()
    
    if(not outgo.user_id==user.id):
        return {"error":"Outgo not valid"}, HTTPStatus.BAD_REQUEST
    
    try:
        db.session.delete(outgo)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Resource could not be deleted",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    return {"data": ""}, HTTPStatus.NO_CONTENT