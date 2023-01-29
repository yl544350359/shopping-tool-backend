from flask import Flask
from flask_cors import CORS
from flask_restful import Api, Resource
from views import HelloWorld,ItemDetail,GetRate

app=Flask(__name__)
CORS(app)
api=Api(app)

api.add_resource(HelloWorld,"/")
api.add_resource(ItemDetail,"/itemDetail")
api.add_resource(GetRate,"/getRate")

if __name__=="__main__":
    app.run(debug=True)