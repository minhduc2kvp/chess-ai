from aiohttp import web
from app.router import add_routes

app = web.Application()
app.add_routes([web.static("/static", "app/Templates/static")])
app.add_routes([web.static("/img", "app/Templates/static/img")])
add_routes(app=app)
web.run_app(app, host="localhost", port=7000)
