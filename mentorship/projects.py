import configparser
import glob

class Project:
    """
    An object for storing a projects data.
    Stores a dictionary as public information, and the email is a ~private~ variable.
    """
    _mentor_email       = None

    public_information  = {***REMOVED***

    def __init__(self, project_id, title, mentor_name, description, learning_outcomes, requirments, mentor_email):
        """
        :param project_id:
        :param title:
        :param mentor_name:
        :param description:
        :param learning_outcomes:
        :param requirments:
        :param mentor_email:

        sets information to the public information dictionary and the email address.
        """
        self.public_information = {
            "project_id"        : project_id,
            "title"             : title,
            "mentor_name"       : mentor_name,
            "description"       : description,
            "learning_outcomes" : learning_outcomes,
            "requirements"      : requirements
        ***REMOVED***
        self._mentor_email      = mentor_email

    def __str__(self):
        """
        A minimal string represenatation of the project object; will be used for logging
        :return:
        """
        return_string = "Project: {project_id***REMOVED***-{name***REMOVED***".\
            format(self.public_information["project_id"],
                   self.public_information["name"])

        return return_string

    def get_project_information(self):
        """
        :return: all public information on a project
        """
        return self.public_information

    def get_mentor_email(self):
        """
        :return: the mentors email
        """
        return self._mentor_email