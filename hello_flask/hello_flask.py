from flask import Flask     # Import Flask

app = Flask(__name__)       # Instantiate a flask instance and make it a variable called 'app' so it's easier to work with.

#Generic 'Hello World' with Flask taken from http://flask.pocoo.org/docs/0.12/

@app.route('/')             # This is a definition of the '/' (index) route
def hello_world():          # This is a definition of the endpoint
    return 'Hello, World!'


# Arguments Demo.

from flask import request                   # We import request
"""
    request is a flask object that contains all the data a request has. It's up to you're endpoint to handle that request.
    A request object contains various fields that store information. We will only worry about args (arguments).
    Other fields include form, cookies, files and a lot more.
    If you want to find out more; go here http://flask.pocoo.org/docs/0.12/api/#incoming-request-data
    """

@app.route('/whats_your_name', methods=["POST"])
def what_is_your_name():

    """
    We are expecting a route that resembles this:
        /whats_your_name?name=<some_name>
    The argument we are looking for is 'name'.
    We seek the value of this argument.
    """

    your_name = request.args.get("name")        # We get the value of the argument 'name'

    return "Your name is %s" % your_name



# Lets get our templating game on

from flask import render_template           # We import render_template
"""
Render template is a flask method that renders Jinja2 static_html. 
It takes the path to the template as the first parameter.
It then takes a series of optional parameters. All of which correspond to variables described in your template file.
"""


# A basic templating demo
@app.route('/profoundly_pathetic_route', methods=["GET"])
def profoundly_pathetic_endpoint():
    """
        We are expecting a route that resembles this:
            /profoundly_pathetic_route?name=<some_name>
        """

    name = request.args.get("name")         # Again, we get a name arguement

    return render_template("template.html", ex=name)    # This time we feed the value if that argument into a template
                                                        # Jinja then injects it into prewritten html

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True
    )