import os
from typing import List, Tuple

from api.urls import api
from db.models import Breed, Kitty, db
from flask import abort, current_app, request
from flask_restx import Namespace, Resource, fields, reqparse
from PIL import Image
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

upload_parser = reqparse.RequestParser()
upload_parser.add_argument(
    "image", location="files", type=FileStorage, required=True, action="append"
)

cats_ns = Namespace("cats", description="All about cats")


class ImageLinkField(fields.Raw):
    def format(self, value: str) -> str:
        static = current_app.config["UPLOAD_FOLDER"]
        return f"{api.base_url}{static}/{value}"


get_cats = api.model(
    "get_cats",
    {
        "id": fields.Integer(readonly=True, description="Cat unique identifier"),
        "name": fields.String(required=True, description="Cat detail"),
        "description": fields.String(required=True, description="Cat description"),
        "image": ImageLinkField(required=True, description="Cat photo"),
        "breed_id": fields.Integer(required=True, description="Breed identifier"),
        "birthday": fields.Date(requred=True, description="Brithday"),
    },
)

post_cats = api.model(
    "post_cats",
    {
        "id": fields.Integer(readonly=True, description="Cat unique identifier"),
        "name": fields.String(required=True, description="Cat detail"),
        "description": fields.String(required=True, description="Cat description"),
        "breed_id": fields.Integer(required=True, description="Breed identifier"),
        "birthday": fields.Date(requred=True, description="Brithday"),
    },
)


@cats_ns.route("/")
class CatsList(Resource):
    @cats_ns.doc("cats_list", params={"search": {"description": "Full text search"}})
    @cats_ns.marshal_list_with(get_cats)
    def get(self) -> Tuple[List[Kitty], int]:
        cats = Kitty.query.all()
        searched_value = request.args.get("search")
        if searched_value:
            cats = Kitty.fulltext_search(searched_value).all()
        return cats, 200

    @cats_ns.doc("create_cat")
    @cats_ns.expect(post_cats)
    @cats_ns.marshal_with(post_cats, code=201)
    def post(self) -> Tuple[Kitty, int]:
        file = request.files.get("image")
        data = request.json or request.values
        breed = Breed.query.get(data.get("breed_id"))
        if not breed:
            abort(403, "Breed not found")
        if file:
            static_root = current_app.config["UPLOAD_FOLDER"]
            filename = secure_filename(file.filename)
            ext = filename.split(".")
            name, ext = ext if len(ext) > 1 else ext
            file.save(os.path.join(static_root, filename))
            file.close()
            thumbnail_file = Image.open(os.path.join(static_root, filename))
            thumbnail_file.thumbnail((500, 500))
            thumbnail_file.save(os.path.join(static_root, f"{filename}_thumb.{ext}"))
            image = {"image": filename}
            new_cat = Kitty(**{**data, **image})
        else:
            new_cat = Kitty(**data)
        db.session.add(new_cat)
        db.session.commit()
        return new_cat, 201


@cats_ns.route("/<int:id>")
@cats_ns.response(404, "Cat not found")
@cats_ns.param("id", "Cat identifier")
class CatsDetail(Resource):
    @cats_ns.doc("get_cat")
    @cats_ns.marshal_list_with(get_cats)
    def get(self, id: int) -> Tuple[Kitty, int]:
        cat = Kitty.query.get_or_404(id)
        return cat, 200

    @cats_ns.doc("delete_todo")
    @cats_ns.response(204, "Todo deleted")
    def delete(self, id: int) -> Tuple[str, int]:
        cat = Kitty.query.get_or_404(id)
        with db.session() as ses:
            ses.delete(cat)
            ses.commit()
        return "", 204

    @cats_ns.expect(post_cats)
    @cats_ns.marshal_with(post_cats)
    def patch(self, id: int) -> Tuple[Kitty, int]:
        cat = Kitty.query.get_or_404(id)
        file = request.files.get("image")
        if file:
            static_root = current_app.config["UPLOAD_FOLDER"]
            filename = secure_filename(file.filename)
            ext = filename.split(".")
            name, ext = ext if len(ext) > 1 else ext
            file.save(os.path.join(static_root, filename))
            file.close()
            thumbnail_file = Image.open(os.path.join(static_root, filename))
            thumbnail_file.thumbnail((100, 100))
            thumbnail_file.save(os.path.join(static_root, f"{filename}_thumb.{ext}"))
            cat.image = filename
            for key, value in request.values:
                setattr(cat, key, value)
        else:
            for key, value in request.json.items():
                setattr(cat, key, value)
            db.session.commit()
        return cat, 200
