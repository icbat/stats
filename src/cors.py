import bottle


class EnableCors(object):
    name = 'enable_cors'
    api = 2

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            bottle.response.headers['Access-Control-Allow-Origin'] = '*'
            bottle.response.headers['Access-Control-Allow-Methods'] = 'POST, GET'
            bottle.response.headers['Access-Control-Allow-Headers'] = ''

            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors
