from flask import Flask
from flask_cors import CORS
from flask_restful import Api, Resource
# from views.home import HelloWorld
# from views.item_detail import ItemDetail
from views import HelloWorld,ItemDetail

app=Flask(__name__)
CORS(app)
api=Api(app)

api.add_resource(HelloWorld,"/")
api.add_resource(ItemDetail,"/itemDetail")

if __name__=="__main__":
    app.run(debug=True)