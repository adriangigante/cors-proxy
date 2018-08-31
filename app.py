# -*- coding: utf-8 -*-
import flask
import requests
from flask import json

app = flask.Flask(__name__)

method_requests_mapping = {
    'GET': requests.get,
    'HEAD': requests.head,
    'POST': requests.post,
    'PUT': requests.put,
    'DELETE': requests.delete,
    'PATCH': requests.patch,
    'OPTIONS': requests.options,
}

@app.route('/<path:url>', methods=method_requests_mapping.keys())
def proxy(url):

    requests_function = method_requests_mapping[flask.request.method]
    response = requests.get(url)
    data = {
        'contents' : response.text,
        'status' : {
            'url' : url,
            'content_type' : response.headers['content-type'],
            'http_code' : response.status_code
            }
    }
    js = json.dumps(data)

    response = flask.Response(js,                   
                              status = 200,
                              content_type = 'application/json')
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
