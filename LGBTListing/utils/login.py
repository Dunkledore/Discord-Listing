from quart import session, redirect, flash
from functools import wraps


def require_login(function_):
	@wraps(function_)
	async def wrapper(*args, **kwargs):
		if "user" not in session or not session["user"]:
			await flash("Login Required", "error")
			return redirect('/index')
		return await function_(*args, **kwargs)
	return wrapper

