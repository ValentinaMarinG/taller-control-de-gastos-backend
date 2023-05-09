from flask import Blueprint, request

incomes = Blueprint("incomes",
                    __name__,
                    url_prefix="api/v1/incomes")

@incomes.post("/")
def create():
    return "Creating an income ... soon"

@incomes.get("/<int:id>")
def read_one():
    return "Reading an specific income ... soon"

@incomes.get("/")
def read_by_date():
    return "Reading incomes according to a date range ... soon"

@incomes.get("/")
def read_all_of_a_user():
    return "Reading all the incomes of an specific user ... soon"

@incomes.put("/<int:id>")
def update():
    return "Updating an income ... soon"

@incomes.delete("/<int:id>")
def delete():
    return "Removing an income ... soon"