import config
from flask import Flask
from flask import render_template, request
from projects import Projects_Factory

from email_client import Email_Client

app = Flask("netsoc_mentorship")

# Create the email client
email_client = Email_Client(sendgrid_key=config.email_config["API_KEY"],
                            sender_email=config.email_config["Sender_Address"],
                            admin_email=config.email_config["Admin_Email"])

# Create Projects_Factory to fetch all projects
projects_factory = Projects_Factory(config.projects_directory)


@app.route("/")
def home():
    """
    Populates the home page with all projects.
    :return: A rendered template of home.html
    """
    projects = projects_factory.get_projects_as_dicts()
    return render_template("home.html", PROJECTS=projects)


@app.route("/project-proposal", methods=["POST"])
def projects_proposal():
    """
    Used for submitting a project application form.
    Sends an email to the admin and the mentor of the the application.
    :return: a rendered template of submission.html
    """
    form = request.form
    project = projects_factory.get_project_by_id(form["project_id"])
    subject, body = email_client.create_project_application_email(first_name=form["app_first_name"],
                                                                  last_name=form["app_last_name"],
                                                                  applicants_email=form["app_email"],
                                                                  cover_letter=form["cover_letter"],
                                                                  project_title=project.get_project_information()[
                                                                      "title"])

    email_sent = email_client.send_email(subject=subject,
                                         message_body=body,
                                         recipients=[project.get_mentor_email()])

    if email_sent:
        response_message = "Thank you for your application. We will be in touch with you shortly."
    else:
        response_message = "We apologise as we seem to be having some technical difficulties. Please try again later."

    return render_template("submission.html", RESPONSE_MESSAGE=response_message)


@app.route("/mentorship-proposal", methods=["POST"])
def mentorship_propasal():
    """
        Used for submitting a mentorship proposal form.
        Sends an email of the application to the admin
        :return: a rendered template submission.html
        """
    form = request.form
    subject, body = email_client.create_mentorship_proposal_email(first_name=form["mentor_first_name"],
                                                                  last_name=form["mentor_last_name"],
                                                                  applicants_email=form["mentor_email"],
                                                                  title=form["mentor_project_title"],
                                                                  description=form["mentor_project_description"])

    email_sent = email_client.send_email(subject=subject,
                                         message_body=body)

    if email_sent:
        response_message = "Thank you for your application. We will be in touch with you shortly."
    else:
        response_message = "We apologise as we seem to be having some technical difficulties. Please try again later."

    return render_template("submission.html", RESPONSE_MESSAGE=response_message)