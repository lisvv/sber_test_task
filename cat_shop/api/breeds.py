from typing import List, Tuple

from api.urls import api
from db.models import Breed, Kitty, db
from flask import Request, Response, current_app, request
from flask_restx import Namespace, Resource, fields, reqparse
from werkzeug.datastructures import FileStorage

upload_parser = reqparse.RequestParser()
upload_parser.add_argument(
    "image", location="files", type=FileStorage, required=True, action="append"
)

breed_ns = Namespace("breed", description="Breeds")


class ImageLinkField(fields.Raw):
    def format(self, value: str) -> str:
        static = current_app.config["UPLOAD_FOLDER"]
        return f"{api.base_url}{static}/{value}"


breed = api.model(
    "get_breed",
    {
        "id": fields.Integer(readonly=True, description="Breed unique identifier"),
        "name": fields.String(required=True, description="Breed name"),
    },
)


@breed_ns.route("/")
class BreedList(Resource):
    @breed_ns.doc("breed_list")
    @breed_ns.marshal_list_with(breed)
    def get(self) -> Tuple[List[Breed], int]:
        breeds = Breed.query.all()
        searched_value = request.args.get("search")
        if searched_value:
            cats = Kitty.fulltext_search(searched_value).all()
        return breeds, 200

    @breed_ns.doc("create_cat")
    @breed_ns.expect(breed)
    @breed_ns.marshal_with(breed, code=201)
    def post(self) -> Tuple[Breed, int]:
        data = request.json
        new_breed = Breed(**data)
        db.session.add(new_breed)
        db.session.commit()
        return new_breed, 201


@breed_ns.route("/<int:id>")
@breed_ns.response(404, "Cat not found")
@breed_ns.param("id", "Breed identifier")
class BreedDetail(Resource):
    @breed_ns.doc("get_breed")
    @breed_ns.marshal_list_with(breed)
    def get(self, id: int) -> Tuple[Breed, int]:
        breed = Breed.query.get_or_404(id)
        return breed, 200

    @breed_ns.doc("delete_breed")
    @breed_ns.response(204, "Breed deleted")
    def delete(self, id: int) -> Tuple[str, int]:
        cat = Breed.query.get_or_404(id)
        with db.session() as ses:
            ses.delete(cat)
            ses.commit()
        return "", 204

    @breed_ns.expect(breed)
    @breed_ns.marshal_with(breed)
    def patch(self, id: int) -> Tuple[Breed, int]:
        breed = Breed.query.get_or_404(id)
        for key, value in request.json.items():
            setattr(breed, key, value)
        db.session.commit()
        return breed, 200
