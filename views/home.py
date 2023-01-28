from flask_restful import Resource,reqparse

class HelloWorld(Resource):
    def get(self):
        return 'Welcome'
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('name',type=str, required=True)
        parser.add_argument('age',type=str,required=False)
        args=parser.parse_args()
        print(args)
        return args