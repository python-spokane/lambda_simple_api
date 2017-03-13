# Python Imports
from __future__ import print_function
import json


CEREALS = {
    1: {
        'name': 'Lucky Charms',
        'brand': 'GM',
        'knockoff': False,
    },
    2: {
        'name': 'Marshmallow Mateys',
        'brand': 'Malt O Meal',
        'knockoff': True,
    },
    3: {
        'name': 'Apple Jacks',
        'brand': 'GM',
        'knockoff': False,
    },
    4: {
        'name': 'Apple Dapples',
        'brand': 'Malt O Meal',
        'knockoff': True,
    },

}


class HTTPRequestHandler(object):

    def __init__(self, event):
        self._event = event
        self._http_method = event['httpMethod']
        self._method_handlers = {
            'get': self._get_handler,
            'post': self._post_handler,
        }

    def get_payload(self):
        if self._http_method == 'GET':
            qs_params = self._event.get('queryStringParameters')
            return qs_params or {}
        return json.loads(self._event['body'])

    def get_http_handler(self):
        return self._method_handlers.get(self._http_method.lower())

    def _get_handler(self):
        payload = self.get_payload()

        if 'id' in payload:
            cereal_id = int(payload['id'])
            selected_cereal = CEREALS.get(cereal_id)
            if not selected_cereal:
                return ('No cereal found', 404)
            return (selected_cereal, 200)

        return (CEREALS, 200)

    def _post_handler(self):
        payload = self.get_payload()
        cereal_id = payload.pop('id', None)

        if not cereal_id:
            cereal_id = max(CEREALS.keys()) + 1

        CEREALS[int(cereal_id)] = payload

        return (CEREALS, 200)

    def generate_response(self):
        handler = self.get_http_handler()
        if not handler:
            response_body = 'Unsupported method: %s' % self._http_method
            status_code = 400
        else:
            response_body, status_code = handler()

        return {
            'statusCode': status_code,
            'body': json.dumps(response_body, indent=2),
            'headers': {
                'Content-Type': 'application/json',
            },
        }


def handler(event, context):
    """Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.
    """

    print("Received event: " + json.dumps(event, indent=2))

    request_handler = HTTPRequestHandler(event)
    return request_handler.generate_response()
