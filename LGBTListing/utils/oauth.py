from .. import app
import os
from quart import session
from requests_oauthlib import OAuth2Session


class OAuth:
	API_BASE_URL = os.environ.get('API_BASE_URL', 'https://discordapp.com/api')
	AUTHORIZATION_BASE_URL = API_BASE_URL+'/oauth2/authorize'
	TOKEN_URL = API_BASE_URL+'/oauth2/token'

	os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

	@staticmethod
	def token_updater(token):
		session['oauth2_token'] = token

	@staticmethod
	def make_session(token=None, state=None, scope=None):
		return OAuth2Session(
			client_id=app.OAUTH2_CLIENT_ID,
			token=token,
			state=state,
			scope=scope,
			redirect_uri=app.OAUTH2_REDIRECT_URI,
			auto_refresh_kwargs={
				'client_id': app.OAUTH2_CLIENT_ID,
				'client_secret': app.OAUTH2_CLIENT_SECRET,
			},
			auto_refresh_url=OAuth.TOKEN_URL,
			token_updater=OAuth.token_updater)

	@staticmethod
	def set_session_token(code):
		discord = OAuth.make_session(state=session.get('oauth2_state'))
		token = discord.fetch_token(
			OAuth.TOKEN_URL,
			client_secret=app.OAUTH2_CLIENT_SECRET,
			code=code)
		session['oauth2_token'] = token

	@staticmethod
	def initialise_oauth(scope):
		discord = OAuth.make_session(scope=scope.split(' '))
		authorization_url, state = discord.authorization_url(OAuth.AUTHORIZATION_BASE_URL)
		session['oauth2_state'] = state
		return authorization_url

	@staticmethod
	def set_user_variables():
		token = session.get('oauth2_token')
		if token:
			discord = OAuth.make_session(token=token)
			session['guilds'] = discord.get(OAuth.API_BASE_URL+'/users/@me/guilds').json()
			# A list containing guild dicts containing id, name, icon, owner and permissions
			session['user'] = discord.get(OAuth.API_BASE_URL+'/users/@me').json()
			# A user dict that contains id, username, discriminator and avatar
			session['user_connections'] = discord.get(OAuth.API_BASE_URL+'/users/@me/connections').json()
			# A list list contains connection dicts containing id, name, type, revoked and integrations
