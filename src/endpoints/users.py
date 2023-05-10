from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
import werkzeug

from src.database import db

from src.models.user import User,  user_schema, users_schema

users = Blueprint("users",
                  __name__,
                  url_prefix="/api/v1/users")

@users.post("/")
def create():
    post_data = None
    
    try:
        post_data = request.get_json()
        
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Post body JSON data not found",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    user = User(id = request.get_json().get("id", None),
                name = request.get_json().get("name", None),
                lastname = request.get_json().get("lastname", None),
                phone_number = request.get_json().get("phone_number", None),
                email = request.get_json().get("email", None),
                password = request.get_json().get("password", None))
    
    try:
        db.session.add(user)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    return {"data": user_schema.dump(user)}, HTTPStatus.CREATED
       
@users.get("/")
def read_all():
    users = User.query.order_by(User.name).all()
    
    return {"data": users_schema.dump(users)}, HTTPStatus.OK

@users.get("/<string:id>")
def read_one(id):
    user = User.query.filter_by(id=id).first()
    
    if(not user):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    
    return {"data": user_schema.dump(user)}, HTTPStatus.OK

@users.put("/<string:id>")
def update(id):
    post_data = None
    
    try:
        post_data = request.get_json()
    
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Put body JSON data not found",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
        
    user = User.query.filter_by(id=id).first()
    
    if(not user):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    
    user.name = request.get_json().get('name', user.name)
    user.lastname = request.get_json().get('lastname', user.lastname)
    user.phone_number = request.get_json().get('phone_number', user.phone_number)
    user.email = request.get_json().get('email', user.email)
    user.password = request.get_json().get('password', user.password)
    
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    return {"data": user_schema.dump(user)}, HTTPStatus.OK

@users.delete("/<string:id>")
def delete(id):
    user = User.query.filter_by(id=id).first()
    
    if(not user):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    
    try:
        db.session.delete(user)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Resource could not be deleted",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    return {"data": ""}, HTTPStatus.NO_CONTENT

@users.post("/auth")
def authentication(id):
    return "Authenticating an user ... soon"

@users.get("/<string:user_id>/balance")
def CalculateBalance(user_id):
    user = User.query.filter_by(id=user_id).first()
    
    if(not user):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    
    income_total = sum(i.value for i in user.incomes)
    outgo_total = sum(i.value for i in user.outgoes)
    
    total_balance = income_total - outgo_total
    
    return {"balance": total_balance}