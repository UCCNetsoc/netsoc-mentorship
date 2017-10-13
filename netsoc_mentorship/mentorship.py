from flask import Flask
from flask import render_template, request
from netsoc_mentorship.projects import Projects_Factory, Project
from netsoc_mentorship.email_client import Email_Client
import netsoc_mentorship.config as config

app = Flask(__name__)

email_client = Email_Client(sendgrid_key=config.email_config["API_KEY"],
                            sender_email=config.email_config["Sender_Address"],
                            admin_email=config.email_config["Admin_Email"])

projects_factory = Projects_Factory(config.projects_directory)

@app.route("/")
def home():
    projects = projects_factory.get_projects_as_dicts()
    return render_template("home.html", PROJECTS=projects)


@app.route("/project-proposal", methods=["POST"])
def projects_proposal():
    form = request.form
    project = projects_factory.get_project_by_id(form["project_id"])
    subject, body = email_client.create_project_application_email(first_name=form["app_first_name"],
                                                  last_name=form["app_last_name"],
                                                  applicants_email=form["app_email"],
                                                  cover_letter=form["cover_letter"],
                                                  project_title=project.get_project_information()["title"])

    email_sent = email_client.send_email(subject=subject,
                                         message_body=body,
                                         recipients=[project.get_mentor_email()])

    if email_sent:
        response_message = "Thank you for your application. We will be in touch with you shortly."
    else:
        response_message = "We apologise as we seem to be having some technical difficulties. Please try again later."

    return render_template("submission.html", RESPONSE_MESSAGE=response_message)


@app.route("/netsoc_mentorship-proposal", methods=["POST"])
def mentorship_propasal():
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


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=False
    )