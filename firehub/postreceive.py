"""
A Github post-receive hook endpoint.
"""
import json

from twisted.python import log
from twisted.web import resource


class Endpoint(resource.Resource):
    def __init__(self, payloadReceived):
        self.payloadReceived = payloadReceived


    def render_POST(self, request):
        try:
            rawPayload, = request.args["payload"]
            payload = json.loads(rawPayload)
            self.payloadReceived(payload)
        except KeyError:
            log.err("Missing or more than one payload from post-receive hook")
        except ValueError:
            log.err("Malformed JSON from post-receive hook")
 
        return ""
