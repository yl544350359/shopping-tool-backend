from flask_restful import Resource, reqparse
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from utilities.mercari import mercari_brief_info
from utilities.custom_exception import *

class ItemDetail(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('item_url',type=str, required=True, help='Url is missing')
        args=parser.parse_args()
        try:
            data=mercari_brief_info(args['item_url'])
        except TimeoutError as e:
            return e.args[0], 408
        except WebDriverException as e:
            return str(e), 503
        return data
      