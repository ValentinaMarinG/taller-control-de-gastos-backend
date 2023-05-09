from flask import Blueprint, request

outgoes = Blueprint("outgoes",
                    __name__,
                    url_prefix="api/v1/outgo")

@outgoes.post("/")
def create():
    return "Creating an outgo ... soon"

@outgoes.get("/<int:id>")
def read_one():
    return "Reading an specific outgo ... soon"

@outgoes.get("/")
def read_by_date():
    return "Reading outgoes according to a date range ... soon"

@outgoes.get("/")
def read_all_of_a_user():
    return "Reading all the outgoes of an specific user ... soon"

@outgoes.put("/<int:id>")
def update():
    return "Updating an outgo ... soon"

@outgoes.delete("/<int:id>")
def delete():
    return "Removing an outgo ... soon"