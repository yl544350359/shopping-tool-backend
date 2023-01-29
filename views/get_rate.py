from flask_restful import Resource
from utilities.money import getCurrencyRate

class GetRate(Resource):
    def get(self):
        rate=getCurrencyRate()
        return {"rate":rate}
