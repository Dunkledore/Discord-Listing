from LGBTListing import app
from quart import render_template, request, redirect, session
from .utils.oauth import OAuth


@app.route("/")
async def index():
	return await render_template("index.html")


@app.errorhandler(404)
async def page_not_found(e):
	return await render_template('404.html'), 404


@app.route('/callback')
async def callback():
	args = request.args
	if args.get('error'):
		return args['error']
	code = args.get('code')

	OAuth.set_session_token(code)
	OAuth.set_user_variables()

	return redirect('/profile')


@app.route('/login')
async def login():
	args = request.args
	scope = args.get(
		'scope',
		'identify connections guilds')
	authorization_url = OAuth.initialise_oauth(scope)

	return redirect(authorization_url)


@app.route('/profile')
async def profile():
	if not session.get("user"):
		return redirect("/login")
	else:
		user = session['user']
		return await render_template("profile.html", user=user)
