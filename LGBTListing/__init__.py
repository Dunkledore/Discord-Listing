from quart import Quart
import quart.flask_patch
import flask_login
from .instance import config


app = Quart(__name__)
app.OAUTH2_CLIENT_SECRET = app.config['SECRET_KEY'] = config.OAUTH2_CLIENT_SECRET
app.OAUTH2_CLIENT_ID = config.OAUTH2_CLIENT_ID
app.OAUTH2_REDIRECT_URI = config.OAUTH2_REDIRECT_URI


login_manager = flask_login.LoginManager()
login_manager.init_app(app)



import LGBTListing.views



