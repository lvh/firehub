"""
Tests for accepting e-mail from Github.
"""
from functools import partial

from twisted.python import log
from twisted.trial import unittest

from firehub import incoming


class MessageTest(unittest.TestCase):
    def setUp(self):
        self.message = incoming.Message(self.messageReceived)
        self.messageContent = None


    def messageReceived(self, messageContent):
        """
        Called when a message is received from Github.
        """
        self.messageContent = messageContent


    def test_simple(self):
        lines = "abc"
        for line in lines:
            self.message.lineReceived(line)
        self.message.eomReceived()

        self.assertEquals(self.messageContent, "\n".join(lines))
        self.assertIdentical(self.message.lines, None)


    def test_connectionLost(self):
        self.connectionLost = False
        def observer(event):
            self.assertTrue(event["isError"])
            self.assertTrue(event["message"])
            self.connectionLost = True

        try:
            log.addObserver(observer)
            self.message.connectionLost()
            self.assertTrue(self.connectionLost)
            self.assertIdentical(self.message.lines, None)
        finally:
            log.removeObserver(observer)



class MessageRecipientTest(unittest.TestCase):
    """
    Tests what happens when messages are delivered with different
    recipients.
    """
    def setUp(self):
        self.delivery = incoming.MessageDelivery()



class FakeOrigin(object):
    def __init__(self, domain):
        self.local = "issues"
        self.domain = domain



githubOrigin = FakeOrigin("github.com")
bitbucketOrigin = FakeOrigin("bitbucket.com")

githubHelo = "github.com", "207.97.227.239"
bitbucketHelo = "bitbucket.com", "128.177.10.242"

githubData = githubHelo, githubOrigin
bitbucketData = bitbucketHelo, bitbucketOrigin



class MessageOriginTest(unittest.TestCase):
    def setUp(self):
        self.delivery = incoming.MessageDelivery()


    def test_noHelo(self):
        """
        Tests that not saying HELO first doesn't work.
        """
        self.delivery.validateFrom(None, githubOrigin)


    def test_fromGithub(self):
        """
        Tests that a message from Github is accepted.
        """
        self.delivery.validateFrom(*githubData)


    def test_notFromGithub(self):
        """
        Tests that a message not from Github is rejected.
        """
        self.delivery.validateFrom(*bitbucketData)



class ReceivedHeaderTest(unittest.TestCase):
    """
    Tests for the Received header as produced by ``MessageDelivery``.
    """
    def setUp(self):
        delivery = incoming.MessageDelivery()
        self.receivedHeader = partial(delivery.receivedHeader, *githubData)


    def test_singleRecipient(self):
        """
        Tests delivery to a single recipient.
        """
        try:
            self.receivedHeader()
        finally:
            pass


    def test_multipleRecipients(self):
        """
        Tests delivery to multiple recipients.
        """
