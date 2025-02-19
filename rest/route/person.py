import pandas as pd
from flask import Blueprint, request

from ..ExceptionHandler import exception_handler
from ..status_code import (
    CODE_OK,
    FILE_NOT_PROVIDED,
    REQUIRED_FIELD,
    WRITER_NOT_PROVIDED,
)
from .src.presentation.controller.person import PersonController

person_route = Blueprint("person_route", __name__, url_prefix="/person")


@person_route.post("/")
@exception_handler
def create_person():
    params = request.args.to_dict()

    if (write_uid := params.get("write_uid")) is None:
        return WRITER_NOT_PROVIDED

    lc = PersonController(write_uid, person_route.config, constant.TIME_OUT)

    request_data = request.get_json()
    lc.create(
        request_data["person_id"],
        request_data["name"],
        request_data["last_name"],
        request_data["mail_address"],
        request_data.get("birthdate"),
        request_data.get("document_number"),
        request_data.get("address"),
    )

    return CODE_OK


@person_route.post("/csv")
@exception_handler
def create_persons_from_csv():
    params = request.args.to_dict()

    if (write_uid := params.get("write_uid")) is None:
        return WRITER_NOT_PROVIDED

    lc = PersonController(
        write_uid,
        person_route.config["MONGO_SERVER"],
        person_route.config["RABBITMQ_SERVER"],
    )

    if "file" not in request.files:
        return FILE_NOT_PROVIDED
    file = request.files["file"]

    if file.filename == "":
        return FILE_NOT_PROVIDED

    df = pd.read_csv(file, delimiter=",")

    lc.insert_many(df.to_dict())

    return CODE_OK


@person_route.get("/", defaults={"id": None})
@person_route.get("/<id>")
@exception_handler
def fetch_persons(id=None):
    params = request.args.to_dict()

    if (write_uid := params.get("write_uid")) is None:
        return WRITER_NOT_PROVIDED

    lc = PersonController(
        write_uid,
        person_route.config["MONGO_SERVER"],
        person_route.config["RABBITMQ_SERVER"],
    )
    data = lc.get_by_id(id) if id is not None else lc.fetch()

    return (CODE_OK[0], data)


@person_route.put("/<id>")
@exception_handler
def update_person(id):
    params = request.args.to_dict()

    if (write_uid := params.get("write_uid")) is None:
        return WRITER_NOT_PROVIDED
    if (person_id := id) is None:
        return REQUIRED_FIELD

    request_data = request.get_json()
    request_data.update(params["write_uid"])

    lc = PersonController(
        write_uid,
        person_route.config["MONGO_SERVER"],
        person_route.config["RABBITMQ_SERVER"],
    )
    lc.update(person_id, request_data)

    return CODE_OK


@person_route.delete("/<id>")
@exception_handler
def delete_person(id):
    params = request.args.to_dict()

    if (write_uid := params.get("write_uid")) is None:
        return WRITER_NOT_PROVIDED
    if (person_id := id) is None:
        return REQUIRED_FIELD

    lc = PersonController(
        write_uid,
        person_route.config["MONGO_SERVER"],
        person_route.config["RABBITMQ_SERVER"],
    )
    lc.delete(person_id)

    return CODE_OK
