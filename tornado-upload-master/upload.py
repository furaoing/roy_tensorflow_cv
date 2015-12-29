import tornado.httpserver, tornado.ioloop, tornado.options, tornado.web, os.path, random, string
from tornado.options import define, options

from classify_image_roy_variant_web import NodeLookup
from classify_image_roy_variant_web import create_graph
from classify_image_roy_variant_web import run_inference_on_image
from classify_image_roy_variant_web import roy_config
from baidu_translate import translate
import os

import sys

define("port", default=80, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/upload", UploadHandler)
        ]
        tornado.web.Application.__init__(self, handlers)
        
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("upload_form.html")
        
class UploadHandler(tornado.web.RequestHandler):
    config = roy_config
    node_lookup = NodeLookup(config)
    # Creates graph from saved GraphDef.
    create_graph(config)
    logging.basicConfig(filename="server_log", level=logging.DEBUG)

    def post(self):
        file1 = self.request.files['file1'][0]
        original_fname = file1['filename']
        extension = os.path.splitext(original_fname)[1]
        fname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
        final_filename= fname+extension

        relative_path = "uploads/" + final_filename
        base_path = sys.path[0]
        abs_path = os.path.join(base_path, relative_path)

        output_file = open(abs_path, 'wb')
        output_file.write(file1['body'])
        output_file.close()

        try:
            result_str = run_inference_on_image(abs_path, self.node_lookup, self.config)
        except:
            debug_msg = time.asctime() + " Method: run_inference_on_image Failed"
            logging.debug(debug_msg)
            result_str = "Image Format Error"

        try:
            result_str = translate(result_str)
            result_str = result_str.replace(r"|", r"</br>")
        except:
            debug_msg = time.asctime() + " Baidu Translate API Call Failed"
            logging.debug(debug_msg)
            result_str = "Baidu Translate API Call Failed"

        self.finish("Result:" + r"</br></br>" + result_str)


def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":

    # Script Initialization Start

    pid = os.getpid()
    with open("/var/run/upload.pid", "w") as f:
        f.write(str(pid))

    # Script Initialization End

    main()
