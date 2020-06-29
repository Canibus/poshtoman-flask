class LoggerMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        #print('test func called')
        #print(environ['REQUEST_METHOD'], environ['REMOTE_ADDR'])
        #print(environ)#REQUEST_METHOD REMOTE_ADDR HTTP_API_TOKEN HTTP_REFERER
        print(environ)
        return self.app(environ, start_response)