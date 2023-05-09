from flask import Blueprint, request

users = Blueprint("users",
                  __name__,
                  url_prefix="/api/v1/users")

@users.post("/")
def create():
    return "Creating a user ... soon"
        
@users.get("/")
def read_all():
    return "Reading all users ... soon"

@users.get("/<int:id>")
def read_one(id):
    return "Reading a user ... soon"

@users.put("/<int:id>")
def update(id):
    return "Updating a user ... soon"

@users.delete("<int:id>")
def delete(id):
    return "Removing a user ... soon"

@users.post("/auth")
def authentication(id):
    return "Authenticating an user ... soon"

@users.get("/<int:id>/balance")
def CalculateBalance(id):
    return "Calculating the user's total balance ... soon"