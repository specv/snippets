# tags: %tornado %http

import urllib.parse

import tornado.web
import tornado.httpclient


class ForwardingRequestHandler(tornado.web.RequestHandler):

    HOST = None
    URI = None

    async def prepare(self):
        response = await self._forwarding()
        self.set_status(response.code)

        self._set_headers(response)

        if response.body:
            self.write(response.body)

        self.finish()

    def _set_headers(self, response):
        # TODO: Host, X-Scheme, X-Real-IP, X-Forwarded-For ...
        for name, value in response.headers.items():
            self.set_header(name, value)

    async def _forwarding(self):
        if self.URI:
            uri = self.URI.format(*self.path_args, **self.path_kwargs)
            uri = urllib.parse.urlsplit(self.request.uri)._replace(path=uri).geturl()
        else:
            uri = self.request.uri

        return await tornado.httpclient.AsyncHTTPClient().fetch(
            tornado.httpclient.HTTPRequest(
                url=urllib.parse.urljoin(self.HOST, uri),
                method=self.request.method,
                body=self.request.body,
                headers=self.request.headers,
                follow_redirects=True,
                allow_nonstandard_methods=True,
            ),
            raise_error=False,
        )

