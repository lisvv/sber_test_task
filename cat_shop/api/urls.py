from flask_restx import Api

api = Api()

cats_ns = api.namespace('cats', description='all about cats')
