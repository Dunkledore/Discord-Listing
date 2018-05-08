from quart import Quart
import quart.flask_patch
import flask_login

app = Quart(__name__)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)



import LGBTListing.views



