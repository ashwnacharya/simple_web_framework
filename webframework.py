class application:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response
    
    urls = [
        ("/", "index"),
        ("/hello", "hello")
    ]

    def __iter__(self):
        path_info = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']

        for path, name in self.urls:
            if path == path_info:
                funcname = method.upper() + "_" + name
                func = getattr(self, funcname)
                return func()
        return self.notfound()

    def GET_index(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield "Welcome!\n"

    def GET_hello(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield "Hello world!\n"

    def notfound(self):
        status = '404 Not Found'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield "Not Found\n"

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()