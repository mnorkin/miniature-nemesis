from amazon_ses import AmazonSES
from amazon_ses import EmailMessage


class mailman():
    """
    Mail-man
    Simple implementation for an email sending using Amazon SES
    """

    def __init__(self, _access_key_id, _secret_access_key):
        """
        Initialization of mail man
        """
        self.access_key_id = _access_key_id
        self.secret_access_key = _secret_access_key
        self.amazon_ses = AmazonSES(self.access_key_id, self.secret_access_key)
        self.send_from = 'maksim.norkin@ieee.org'
        self.send_to = 'm.norkin@gmail.com'
        self.topic = 'Crawler mail-man reporting'
        self.message = EmailMessage()

    def write(self, _message):
        """
        Writing and marking the mail
        """
        self.message.subject = self.topic
        self.message.bodyText = _message
        self.send()

    def send(self):
        """
        Sending a message
        """
        pass
        # self.amazon_ses.sendEmail(self.send_from, self.send_to, self.message)
