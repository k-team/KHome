import json
import urlparse
from functools import wraps
import requests
from flask import (Response, request, jsonify as _jsonify, current_app,
        make_response)

def jsonify(obj):
    """
    Updated jsonify, adding list support.
    """
    if isinstance(obj, (list, tuple)):
        return Response(json.dumps(obj), mimetype='application/json')
    return _jsonify(obj)

def cached(timeout=5 * 60, key='view/%s'):
    """
    Decorator adding a cache to the concerned view.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = key % request.path
            rv = cache.get(cache_key)
            if rv is not None:
                return rv
            rv = f(*args, **kwargs)
            cache.set(cache_key, rv, timeout=timeout)
            return rv
        return decorated_function
    return decorator

def proxy(proxy_url, url, **options):
    """
    Generates an app route pointing to the same relative url as the specified
    proxy url. Doesn't return anything, only add the route.
    """
    view_name = url.strip('/').replace('/<>', '_')
    def view(*args, **kwargs):
        request_func = getattr(requests, request.method.lower())
        view_url = urlparse.urljoin(proxy_url, request.path)
        data = request.form \
                if request.method.lower() in ['put', 'post'] \
                else request.data
        print 'data', data
        r = request_func(view_url, headers=request.headers, data=data)
        resp = make_response(r.content)
        resp.headers['Content-type'] = r.headers['Content-type']
        resp.status_code = r.status_code
        return resp
    current_app.add_url_rule(url, view_name, view_func=view, **options)
