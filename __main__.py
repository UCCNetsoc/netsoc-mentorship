from config import flask_config

from mentorship import app

if __name__ == "__main__":
    app.run(**flask_config)
