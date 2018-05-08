from LGBTListing import app
from quart import render_template


@app.route("/")
async def index():
	return await render_template("index.html")


@app.errorhandler(404)
async def page_not_found(e):
	return await render_template('404.html'), 404
