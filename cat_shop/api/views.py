from flask import request
from db.models import Kitty, db
from werkzeug.utils import secure_filename
from flask_restx import Resource, fields, reqparse
from flask import current_app
import os
from PIL import Image
from api.urls import cats_ns, api

parser = reqparse.RequestParser()
parser.add_argument('rate', type=int, help='Rate cannot be converted')
parser.add_argument('search')


class ImageLinkField(fields.Raw):
    def format(self, value):
        static = current_app.config["UPLOAD_FOLDER"]
        return f"{api.base_url}/{static}/{value}"


get_cats = api.model('get_cats', {
    'id': fields.Integer(readonly=True, description='Cat unique identifier'),
    'name': fields.String(required=True, description='Cat detail'),
    'description': fields.String(required=True, description='Cat description'),
    'image': ImageLinkField(required=True, description='Cat photo'),
    'breed_id': fields.Integer(required=True, description='Breed identifier'),
    'birthday': fields.Date(requred=True, description='Brithday')
})

post_cats = api.model('post_cats', {
    'id': fields.Integer(readonly=True, description='Cat unique identifier'),
    'name': fields.String(required=True, description='Cat detail'),
    'description': fields.String(required=True, description='Cat description'),
    'breed_id': fields.Integer(required=True, description='Breed identifier'),
    'birthday': fields.Date(requred=True, description='Brithday')
})


@cats_ns.route('/')
class CatsList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @cats_ns.doc('cats_list')
    @cats_ns.marshal_list_with(get_cats)
    def get(self):
        cats = Kitty.query.all()
        searched_value = request.args.get("search")
        if searched_value:
            cats = Kitty.fulltext_search(searched_value).all()
        return cats, 200

    @cats_ns.doc('create_cat')
    @cats_ns.expect(post_cats)
    @cats_ns.marshal_with(post_cats, code=201)
    def post(self):
        file = request.files.get('image')
        filename = ""
        if file:
            static_root = current_app.config['UPLOAD_FOLDER']
            filename = secure_filename(file.filename)
            ext = filename.split('.')
            name, ext = ext if len(ext) > 1 else ext
            file.save(os.path.join(static_root, filename))
            file.close()
            thumbnail_file = Image.open(os.path.join(static_root, filename))
            thumbnail_file.thumbnail((100, 100))
            thumbnail_file.save(os.path.join(static_root, f"{filename}_thumb.{ext}"))
        image = {"image": filename}
        data = request.values
        new_cat = Kitty(**{**data, **image})
        with db.session() as ses:
            ses.add(new_cat)
            ses.commit()
        return new_cat, 201


@cats_ns.route('/<int:id>')
@cats_ns.response(404, 'Cat not found')
@cats_ns.param('id', 'Cat identifier')
class CatsDetail(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @cats_ns.doc('get_cat')
    @cats_ns.marshal_list_with(get_cats)
    def get(self, id):
        cat = Kitty.query.get_or_404(id)
        return cat, 200


    @cats_ns.doc('delete_todo')
    @cats_ns.response(204, 'Todo deleted')
    def delete(self, id):
        cat = Kitty.query.get_or_404(id)
        with db.session() as ses:
            ses.delete(cat)
            ses.commit()
        return '', 204

    @cats_ns.expect(post_cats)
    @cats_ns.marshal_with(post_cats)
    def patch(self, id):
        cat = Kitty.query.get_or_404(id)
        file = request.files.get('image')
        if file:
            static_root = current_app.config['UPLOAD_FOLDER']
            filename = secure_filename(file.filename)
            ext = filename.split('.')
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
        with db.session() as ses:
            ses.add(cat)
            ses.commit()
        return cat