# -*- coding: utf-8 -*-
__author__ = 'OL'

import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import os
import sys
import json
import shutil
import pickle


module_path = sys.path[0]
sys.path.append(module_path)
from format_converter.converter_lib import json_obj_to_excel


class IndexPageHandle(tornado.web.RequestHandler):
    """Define the index page handle, when request to visit index page received, it invokes the render method"""
    def get(self):
        self.render(r"templates\index.html")


class AjaxHandle(tornado.web.RequestHandler):
    def post(self):
        """
        query = dict()
        if self.get_argument("sku_name", default=None):
            query["sku_name"] = self.get_argument("sku_name", default=None)
        if self.get_argument("size", default=None):
            query["size"] = self.get_argument("size", default=None)
        if self.get_argument("category", default=None):
            if (self.get_argument("category", default=None) != 0) and (self.get_argument("category", default=None) != -1):
                query["category"] = self.get_argument("category", default=None)
        if self.get_argument("B2C_platform", default=None):
            if (self.get_argument("B2C_platform", default=None) != 0) and (self.get_argument("B2C_platform", default=None) != -1):
                query["B2C_platform"] = self.get_argument("B2C_platform", default=None)

        for key in query.keys():
            query[key] = query[key]

        db = MySQLdb.Connect(
            host="localhost",
            user="root",
            passwd="",
            db="sku",
        )
        db.query('SET NAMES utf8')
        cursor = db.cursor()

        sql_base = u"SELECT * from skuprice WHERE "

        condition = [x+"='"+y+"' AND " for x, y in query.items()]
        condition = "".join(condition)
        condition = condition.rstrip(" AND ")
        sql = sql_base+condition
        sql = sql.encode(encoding="utf8")

        try:
            cursor.execute(sql)
            data_tuple = cursor.fetchall()
            db.commit()

            json_obj = list()
            for data in data_tuple:
                response = dict()
                response['sku_name'] = data[0]    # data[0] has a str type
                response['B2C_platform'] = data[1]
                response['vendor_url'] = data[2]
                response['scrapping_time'] = data[3]
                response['source_name'] = data[4]
                response['price'] = data[5]
                response['sales_volume'] = data[6]
                response['comments'] = data[7]
                json_obj.append(response)
            json_str = json.dumps(json_obj)   # json_str object has a str type
            self.write(json_str)

        except:
            db.rollback()
            print('Exception Occured !')
            self.write("NO_DATA")
        """


class FileHandler(tornado.web.RequestHandler):
    # get post data
    def post(self):
        file_body = self.request.files['filefieldname'][0]['body']
        img = Image.open(StringIO.StringIO(file_body))
        img.save("../img/", img.format)

handlers = [
    (r"/", IndexPageHandle),
    (r"/ajax", AjaxHandle),
    (r"/upload", )
    (r"/static/(.*)", tornado.web.StaticFileHandler),
]

settings = {"static_path": os.path.join(sys.path[0], "static"),
            }

app = tornado.web.Application(handlers, **settings)

if __name__ == '__main__':
    server = tornado.httpserver.HTTPServer(app)  # serve the app instance
    server.listen(8085)  # listen port 8085
    tornado.ioloop.IOLoop.instance().start()  # launch the server
