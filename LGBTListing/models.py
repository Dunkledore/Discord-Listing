import quart.flask_patch
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


class Guild(database.Model):

	id = database.Column(database.BigInteger, primary_key=True)
	name = database.Column(database.String(80))
	description = database.Column(database.String(80))
	owner_id = database.Column(database.BigInteger)
	admin_1_id = database.Column(database.BigInteger)
	admin_2_id = database.Column(database.BigInteger)
	category = database.Column(database.String(80), default="Misc")
	invite_link = database.Column(database.String(80))
	icon = database.Column(database.String(150))







