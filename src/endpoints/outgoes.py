from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
import werkzeug

from src.database import db
from datetime import datetime

from src.models.outgo import Outgo, outgo_schema, outgoes_schema

outgoes = Blueprint("outgoes",
                    __name__,
                    url_prefix="/api/v1/outgoes")

@outgoes.post("/")
def create():
    post_data = None
    
    try:
        post_data = request.get_json()
        
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Post body JSON data not found",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    outgo = Outgo(value = request.get_json().get("value", None),
                  user_id = request.get_json().get("user_id", None))
    
    try:
        db.session.add(outgo)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    return {"data": outgo_schema.dump(outgo)}, HTTPStatus.CREATED

@outgoes.get("/<int:id>")
def read_one(id):
    outgo = Outgo.query.filter_by(id=id).first()
    
    if(not outgo):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    
    return {"data": outgo_schema.dump(outgo)}, HTTPStatus.OK

@outgoes.get("/user/<string:user_id>/dates")
def read_by_date(user_id):
    dates_data = None
    
    try:
        dates_data = request.get_json()
        
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Get body JSON data not found",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    start_date = request.get_json().get("start_date", None)
    end_date = request.get_json().get("end_date", None)
    
    outgoes = Outgo.query.filter_by(user_id=user_id).filter(Outgo.date >= start_date, Outgo.date <= end_date).all()
    
    return {"data": outgoes_schema.dump(outgoes)}, HTTPStatus.OK

@outgoes.get("/user/<string:user_id>")
def read_all_of_a_user(user_id):
    outgoes = Outgo.query.filter_by(user_id=user_id).all()
    
    return {"data": outgoes_schema.dump(outgoes)}, HTTPStatus.OK

@outgoes.put("/<int:id>")
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
    
    outgo.value = request.get_json().get('value', outgo.value)
    
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    return {"data": outgo_schema.dump(outgo)}, HTTPStatus.OK

@outgoes.delete("/<int:id>")
def delete(id):
    outgo = Outgo.query.filter_by(id=id).first()
    
    if(not outgo):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    
    try:
        db.session.delete(outgo)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Resource could not be deleted",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    return {"data": ""}, HTTPStatus.NO_CONTENT