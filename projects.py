import configparser
import glob

class Project:
    """
    An object for storing a projects data.
    Stores a dictionary as public information, and the email is a ~private~ variable.
    """
    _mentor_email       = None

    public_information  = {}

    def __init__(self, project_id, title, mentor_name, description, learning_outcomes, requirements, mentor_email):
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
            "learning_outcomes" : learning_outcomes.split(","),
            "requirements"      : requirements.split(",")
        }
        self._mentor_email      = mentor_email

    def __str__(self):
        """
        A minimal string represenatation of the project object; will be used for logging
        :return:
        """
        return_string = "Project: {}-{}".\
            format(self.public_information["project_id"],
                   self.public_information["title"])

        return return_string

    def get_project_information(self):
        """
        :return: all public information on a project
        """
        return self.public_information

    def get_id(self):
        return self.public_information["project_id"]

    def get_mentor_email(self):
        """
        :return: the mentors email
        """
        return self._mentor_email


class Projects_Factory:
    """
    Class that will be used to read project files, generate project objects,
    and store the project objects in a list, and sorts in order of largest id to smallest id.
    (Reverse sorting means that the project created last will appear first on the site).

    This class reads project files following the .ini format and whos extension is .project
    """

    _directory = None
    projects = []
    _filenames = []

    def __init__(self, directory):
        self._directory = directory
        self.update_projects()

    def __str__(self):
        """
        Returns the directory and size of projects list as a string;
        Good for logging.
        :return:
        """
        string = """
                Project Factory:\n
                Directory: {}\n
                Size: {}\n
                """.format(self._directory, len(self.projects))
        return string

    def _read_project(self, filename):
        """
        Reads a specific project given a filename using the config parser.
        :param filename:
        :return: a configparser object, to be treated like a dictionary.
        """
        parser = configparser.ConfigParser()
        parser.read(filename, "utf8")
        return parser

    def _make_project(self, project_dict):
        """
        :param project_dict:
        :return: a Project object
        """
        project = Project(project_id=project_dict["public"]["project_id"],
                          title=project_dict["public"]["project_title"],
                          mentor_name=project_dict["public"]["mentor_name"],
                          description=project_dict["public"]["description"],
                          learning_outcomes=project_dict["public"]["learning_outcomes"],
                          requirements=project_dict["public"]["requirements"],
                          mentor_email=project_dict["private"]["mentor_email"])
        return project

    def _read_directory(self):
        """
        Reads all files in the directory with the .project extension.
        :return:
        """
        self._filenames = glob.glob(self._directory + "/*.project")

    def update_projects(self):
        """
        Updates the list of projects with Project objects and sorts in reverse order.
        :return:
        """
        self._read_directory()
        for filename in self._filenames:
            project = self._make_project(self._read_project(filename))
            self.projects.append(
                (int(project.get_id()), project)
            )
        self.projects = sorted(self.projects, reverse=True)

    def get_projects_as_dicts(self):
        """
        :return: The list of Projects
        """
        return [ _project[1].get_project_information() for _project in self.projects ]

    def get_project_by_id(self, project_id):
        for project in self.projects:
            if project[0] == int(project_id):
                return project[1]

def test():
    import config
    """
    Tests Project_Factory and Project classes
    :return:
    """
    project_factory = Projects_Factory(config.projects_directory)
    projects = project_factory.get_projects()
    print("Factory: ", str(project_factory), "\n",
          "Projects List: ", projects, "\n",
          "Project: ", str(projects[0][1]),"\n",
          "Project Info: ", projects[0][1].get_project_information(), "\n",
          "Mentors Email: ", projects[0][1].get_mentor_email()
          )