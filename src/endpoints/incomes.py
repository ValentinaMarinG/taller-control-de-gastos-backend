from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
import werkzeug

from src.database import db
from datetime import datetime

from src.models.income import Income, income_schema, incomes_schema
from src.models.user import User, user_schema, users_schema

incomes = Blueprint("incomes",
                    __name__,
                    url_prefix="/api/v1/incomes")

@incomes.post("/")
def create():
    post_data = None
    
    try:
        post_data = request.get_json()
        
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Post body JSON data not found",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    income = Income(value = request.get_json().get("value", None),
                    user_id = request.get_json().get("user_id", None))
    
    try:
        db.session.add(income)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    return {"data": income_schema.dump(income)}, HTTPStatus.CREATED

@incomes.get("/<int:id>")
def read_one(id):
    income = Income.query.filter_by(id=id).first()
    
    if(not income):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    
    return {"data": income_schema.dump(income)}, HTTPStatus.OK

@incomes.get("/user/<string:user_id>/dates")
def read_by_date(user_id):
    dates_data = None
    
    try:
        dates_data = request.get_json()
        
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Get body JSON data not found",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    start_date = request.get_json().get("start_date", None)
    end_date = request.get_json().get("end_date", None)
    
    incomes = Income.query.filter_by(user_id=user_id).filter(Income.date >= start_date, Income.date <= end_date).all()
    
    return {"data": incomes_schema.dump(incomes)}, HTTPStatus.OK

@incomes.get("/user/<string:user_id>")
def read_all_of_a_user(user_id):
    incomes = Income.query.filter_by(user_id=user_id).all()
    
    return {"data": incomes_schema.dump(incomes)}, HTTPStatus.OK
    
@incomes.put("/<int:id>")
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
    
    income.value = request.get_json().get('value', income.value)
    
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    return {"data": income_schema.dump(income)}, HTTPStatus.OK

@incomes.delete("/<int:id>")
def delete(id):
    income = Income.query.filter_by(id=id).first()
    
    if(not income):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    
    try:
        db.session.delete(income)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Resource could not be deleted",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    return {"data": ""}, HTTPStatus.NO_CONTENT