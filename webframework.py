import re, traceback

class wsgiapp:
    """Base class for my wsgi application."""

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response
        self.status = "200 OK"
        self._headers = []

    def header(self, header_name, header_value):
        self._headers.append((header_name, header_value))

    def __iter__(self):
        try:
            x = self.delegate()
            self.start(self.status, self._headers)
        except:
            headers = [("Content-Type", "text/plain")]
            self.start("500 Internal Error", headers)
            x = "Internal Error:\n\n" + traceback.format_exc()

        # return value can be a string or a list. 
        # we should be able to return an iter in both the cases.
        if isinstance(x, str):
            return iter([x])
        else:
            return iter(x)

    def delegate(self):
        path = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']

        for pattern, name in self.urls:
            m = re.match('^' + pattern + '$', path)
            if m:
                # pass the matched groups as arguments to the function
                args = m.groups()
                funcname = method.upper() + "_" + name
                func = getattr(self, funcname)
                return func(*args)
        return self.notfound()

class application(wsgiapp):
    urls = [
        ("/", "index"),
        ("/hello/(.*)", "hello"),
        ("/err", "error")
    ]

    def GET_index(self):
        self.header('Content-type', 'text/plain')
        return "Welcome!\n"

    def GET_hello(self, name):
        self.header('Content-type', 'text/plain')
        return "Hello %s!\n" % name

    def GET_error(self):
        raise Exception("this is an error")

    def notfound(self):
        self.status = '404 Not Found'
        self.header('Content-type', 'text/plain')
        return "Not Found\n"

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()