"""
Tests for the post-receive hook endpoint.
"""
from twisted.python import log
from twisted.trial import unittest

from firehub import postreceive


class FakeRequest(object):
    """
    An extremely simple fake request.
    """
    def __init__(self, args={}):
        self.args = args



SIMPLE_PAYLOAD = "{}"
MALFORMED_PAYLOAD = '*'



class EndpointTest(unittest.TestCase):
    def setUp(self):
        self.payload = None
        self.resource = postreceive.Endpoint(self.payloadReceived)
        self.request = FakeRequest()


    def payloadReceived(self, payload):
        self.payload = payload


    def _test(self, args, expectFailure=True):
        request = FakeRequest(args)

        try:
            self.calledWithError = False
            def observer(event):
                self.assertTrue(event["isError"])
                self.assertTrue(event["message"])
                self.calledWithError = True

            log.addObserver(observer)

            body = self.resource.render_POST(request)
            self.assertEqual(body, "")

            if expectFailure:
                self.assertTrue(self.calledWithError)
                self.assertIdentical(self.payload, None)
            else:
                self.assertFalse(self.calledWithError)
                self.assertNotIdentical(self.payload, None)
        finally:
            log.removeObserver(observer)


    def test_simple(self):
        args = {"payload": [SIMPLE_PAYLOAD]}
        self._test(args, expectFailure=False)


    def test_missingPayload(self):
        self._test({})


    def test_twoPayloads(self):
        args = {"payload": [SIMPLE_PAYLOAD, SIMPLE_PAYLOAD]}
        self._test(args)


    def test_malformedPayload(self):
        args = {"payload": [MALFORMED_PAYLOAD]}
        self._test(args)
