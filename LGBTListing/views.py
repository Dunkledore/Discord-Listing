from LGBTListing import app
from quart import render_template, request, redirect, session, url_for, flash
from .utils.oauth import OAuth
from .models import database, Guild
from .utils.login import require_login
from .forms import AddGuildForm


@app.route("/")
@app.route("/index")
async def index():
	guilds = Guild.query.all()

	return await render_template("index.html", guilds=guilds)


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
	print(session["user"])

	return redirect('/myguilds')


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
	print(session)
	if not session.get("user"):
		return redirect("/login")
	else:
		user = session['user']
		return await render_template("profile.html", user=user)


@app.route('/myguilds')
@require_login
async def myguilds():
	owned_guilds = session["owned_guilds"]
	for counter, guild in enumerate(owned_guilds):
		if Guild.query.filter_by(id=guild['id']).first():
			owned_guilds[counter]['in_db'] = True
	return await render_template("guilds.html", owned_guilds=owned_guilds)


@app.route('/addguild/<id_>', methods=['GET', 'POST'])
@require_login
async def addguild(id_):
	owned_guild = False
	for guild in session["owned_guilds"]:
		if guild["id"] == id_:
			owned_guild = guild

	if not owned_guild:
		await flash("You are not the owner of this guild", "error")
		return redirect('/myguilds')

	guild = Guild.query.filter(Guild.id == id_).first()
	if guild:
		await flash("Guild already added", "info")
		return redirect('/editguild/{}'.format(id_))

	add_guild_form = AddGuildForm()
	if request.method == "GET":
		return await render_template('addguild.html', add_guild_form=add_guild_form)

	description = add_guild_form.description.data
	admin1_id = add_guild_form.admin1_id.data
	admin2_id = add_guild_form.admin2_id.data
	invite_link = add_guild_form.invite_link.data
	name = owned_guild["name"]

	guild = Guild(id=id_, name=name, description=description, admin_1_id=admin1_id or 0, admin_2_id=admin2_id or 0, invite_link=invite_link)
	database.session.add(guild)
	database.session.commit()
	await flash("Guild added", "info")
	return redirect("/myguilds")


@app.route('/logout')
async def logout():
	for k in list(session):
		print(k)
		session.pop(k)
	await flash("Logged Out", "error")
	return redirect(url_for('index'))


@app.route('/db')
def testdb():
	try:
		database.session.query("1").from_statement("SELECT 1").all()
		return '<h1>It works.</h1>'
	except:
		return '<h1>Something is broken.</h1>'


@app.route('/tables')
def tables():
	database.create_all()
