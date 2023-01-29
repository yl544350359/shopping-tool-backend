from flask_restful import Resource, reqparse
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from utilities.mercari import mercari_brief_info
from utilities.custom_exception import *
from urllib.parse import urlparse
import re
class ItemDetail(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('item_url',type=str, required=True, help='Url is missing')
        args=parser.parse_args()
        try:
            if not args["item_url"].startswith("http"):
                raise InvalidUrlError("Invalid url")
            res=urlparse(args['item_url'])
            domain_name=res.netloc
            if domain_name=="jp.mercari.com" or domain_name=='www.mercari.com' or domain_name=='item.mercari.com':
                print("Detected Mercari URL...")
                match_reg=r'm\d{10,}'
                match=re.findall(match_reg,args['item_url'], re.I)
                if match:
                    rebuild_url="https://jp.mercari.com/item/"+match[0]
                    print(rebuild_url)
                    data=mercari_brief_info(rebuild_url)
                else:
                    raise NoSupportError("No item ID in url")
            else:
                raise NoSupportError(f"We cannot analyzing [{domain_name}] now. Please waiting for our update.")
        except TimeoutError as e:
            return e.args[0], 408
        except WebDriverException as e:
            return str(e), 503
        except NoSupportError as e: 
            return e.args[0], 404
        except InvalidUrlError as e:
            return e.args[0], 400
        return data
      