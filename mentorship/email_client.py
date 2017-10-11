from sendgrid import Email, sendgrid
from sendgrid.helpers.mail import Content, Mail, Personalization

class Email_Client:
    """
    An email client for sending project applications to mentors and mentorship applications to the admin email.
    Uses the sendgrid API.
    """

    _sg = None
    _sender_email = None
    _admin_email = None

    def __init__(self, sendgrid_key, sender_email, admin_email):
        """
        Initiated with the sendgrid API key, a list of recipients, and the admins email, as well as the sender email.
        :param recipients:
        :param sendgrid_key:
        :param sender_email:
        :param admin_email:
        """
        self._sg = sendgrid.SendGridAPIClient(apikey=sendgrid_key)
        self._sender_email  = Email(sender_email)
        self._admin_email   = Email(admin_email)

    def create_project_application_email(self, first_name, last_name, applicants_email, cover_letter, project_title):
        """
        Creates an email subject and body for a project application.
        :param first_name:
        :param last_name:
        :param applicants_email:
        :param cover_letter:
        :param project_title:
        :return:
        """
        subject = project_title
        message_body = """
                Applicants Name: {***REMOVED*** {***REMOVED***\n
                Applicants Email: {***REMOVED***\n
                Applying for {***REMOVED***\n\n
                Cover Letter: {***REMOVED***""".format(first_name, last_name, applicants_email, project_title, cover_letter)
        return subject, message_body

    def create_mentorship_proposal_email(self, first_name, last_name, applicants_email, title, description):
        """
        Creates a mentorship proposal subject and body
        :param first_name:
        :param last_name:
        :param applicants_email:
        :param title:
        :param description:
        :return:
        """
        subject = "Mentorship Application: {***REMOVED***".format(title)
        message_body = """
                Name:   {***REMOVED*** {***REMOVED***\n
                Email:  {***REMOVED***\n\n
                Project Title:  {***REMOVED***\n
                Description:    {***REMOVED***
                """.format(first_name, last_name, applicants_email, title, description)
        return subject, message_body

    def send_email(self, subject, message_body, recipients=[]):
        """
        Sends an email using the send grid API
        :param subject:
        :param message_body:
        :param additional_emails:
        :return:
        """
        content = Content("text/plain", message_body)
        mail = Mail(self._sender_email, subject, self._admin_email, content)

        if len(recipients) > 0:
            recipients_personalization = Personalization()
            for address in recipients:
                recipients_personalization.add_to(email=Email(address))
            mail.add_personalization(recipients_personalization)
        response = self._sg.client.mail.send.post(request_body=mail.get())
        return str(response.status_code).startswith("20")


def test():
    import config
    email_config = config.email_config
    client = Email_Client(email_config["API_KEY"], email_config["Sender_Address"], email_config["Admin_Email"])
    subject, message = client.create_project_application_email("test", "test", "test", "test", "test")
    print("Project Application\n"
          "Subject: ", subject, "\n"
          "Message: ", message, "\n")
    client.send_email(subject, message, recipients=["<insert your email here>"])
