"""
<<<<<<< Updated upstream
E-mail messages incoming from Github.
"""
from twisted.mail import smtp
from twisted.python import log
=======
Accept forwarded incoming Github e-mails.
"""
from twisted.mail import smtp
>>>>>>> Stashed changes

from zope.interface import implements


class Message(object):
    """
<<<<<<< Updated upstream
    An e-mail message from Github.
=======
    A message from Github.
>>>>>>> Stashed changes
    """
    implements(smtp.IMessage)

    def __init__(self, messageReceived):
        self.lines = []
        self.messageReceived = messageReceived


    def lineReceived(self, line):
        """
        Receives a single message line.
        """
        self.lines.append(line)


    def eomReceived(self):
        """
        Constructs the message and handles it further.
        """
        message = "\n".join(self.lines)
        self.lines = None
        self.messageReceived(message)


    def connectionLost(self):
        """
        The connection vanished prematurely.

        This probably shouldn't happen, and is logged.
        """
        self.lines = None
<<<<<<< Updated upstream
        log.err("Connection lost while receiving message from Github")



class MessageDelivery(object):
    implements(smtp.IMessageDelivery)

    def receivedHeader(self, helo, origin, recipients):
        """
        Builds the appropriate Received header for Github messages.
        """
        try:
            recipient, = recipients
        except TypeError:
            log.err("More than one recipient in a message from Github")


    def validateTo(self, user):
        """
        Validates that this message is being sent to an accepted user.
        """


    def validateFrom(self, helo, origin):
        """
        Check that a message is coming from Github.
        """
        if not helo:
            raise smtp.SMTPBadSender(origin, 503, "Say HELO first.")

        if origin.domain != "github.com":
            raise smtp.SMTPBadSender(origin, 550, "I only talk to Github.")

        return origin
=======
>>>>>>> Stashed changes
