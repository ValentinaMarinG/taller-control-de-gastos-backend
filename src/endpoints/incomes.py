from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
import sqlalchemy.exc
import werkzeug

from src.database import db

from src.models.income import Income, income_schema, incomes_schema
from src.models.user import User, user_schema


incomes = Blueprint("incomes",
                    __name__,
                    url_prefix="/api/v1/incomes")

#Endpoint para crear un ingreso
@incomes.post("/")
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
    
    income = Income(description = request.get_json().get("description", None),
                    date = request.get_json().get("date", None),
                    hour = request.get_json().get("hour", None),
                    value = request.get_json().get("value", None),
                    user_id = user.id)
    
    try:
        db.session.add(income)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    return {"data": income_schema.dump(income)}, HTTPStatus.CREATED

#Endpoint para listar todos los ingresos de un usuario en sesión según un rango de fechas
@incomes.get("/by_dates")
@jwt_required()
def read_by_date():
    dates_data = None
    
    try:
        dates_data = request.get_json()
        
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Get body JSON data not found",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
        
    user_id = user_schema.dump(get_jwt_identity())["id"]
    user = User.query.filter_by(id=user_id).first()
    
    start_date = request.get_json().get("start_date", None)
    end_date = request.get_json().get("end_date", None)
    
    incomes = Income.query.filter_by(user_id=user.id).filter(Income.date >= start_date).filter(Income.date <= end_date).all()
    
    return {"data": incomes_schema.dump(incomes)}, HTTPStatus.OK

#Endpoint para listar todos los ingresos del usuario en sesión
@incomes.get("/")
@jwt_required()
def read_all_of_a_user():
    user_id = user_schema.dump(get_jwt_identity())["id"]
    user = User.query.filter_by(id=user_id).first()
    
    incomes = Income.query.filter_by(user_id=user.id).all()
    
    return {"data": incomes_schema.dump(incomes)}, HTTPStatus.OK
   
#Endpoint para editar un ingreso 
@incomes.put("/<int:id>")
@jwt_required()
def update(id):
    post_data = None
    
    try:
        post_data = request.get_json()
    
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Put body JSON data not found",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
        
    income = Income.query.filter_by(id=id).first()
    
    if(not income):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    
    user_id = user_schema.dump(get_jwt_identity())["id"]
    user = User.query.filter_by(id=user_id).first()
    
    if(not income.user_id==user.id):
        return {"error":"Income not valid"}, HTTPStatus.BAD_REQUEST
    
    income.description = request.get_json().get('description', income.description)
    income.date        = request.get_json().get('date', income.date)
    income.hour        = request.get_json().get('hour', income.hour)
    income.value       = request.get_json().get('value', income.value)
    
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    return {"data": income_schema.dump(income)}, HTTPStatus.OK

#Endpoint para remover un ingreso
@incomes.delete("/<int:id>")
@jwt_required()
def delete(id):
    income = Income.query.filter_by(id=id).first()
    
    if(not income):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    
    user_id = user_schema.dump(get_jwt_identity())["id"]
    user = User.query.filter_by(id=user_id).first()
    
    if(not income.user_id==user.id):
        return {"error":"Income not valid"}, HTTPStatus.BAD_REQUEST
    
    try:
        db.session.delete(income)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Resource could not be deleted",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    return {"data": ""}, HTTPStatus.NO_CONTENT