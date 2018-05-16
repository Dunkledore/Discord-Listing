from quart import Quart
import quart.flask_patch
from .instance import config
from .models import database


app = Quart(__name__)
app.OAUTH2_CLIENT_SECRET = app.config['SECRET_KEY'] = config.OAUTH2_CLIENT_SECRET
app.OAUTH2_CLIENT_ID = config.OAUTH2_CLIENT_ID
app.OAUTH2_REDIRECT_URI = config.OAUTH2_REDIRECT_URI
app.config['SQLALCHEMY_DATABASE_URI'] = config.db_uri

database.init_app(app)



import LGBTListing.views



