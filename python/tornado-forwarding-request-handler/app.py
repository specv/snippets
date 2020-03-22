import tornado.ioloop
import tornado.web

from handler import ForwardingRequestHandler


class MainHandler(ForwardingRequestHandler):

    HOST = 'https://httpbin.org'
    URI = '{}'


def make_app():
    return tornado.web.Application([
        (r"/httpbin/(.+)", MainHandler),
    ], debug=True)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
