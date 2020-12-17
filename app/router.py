from app.controller.home import main_routes


def add_routes(app):
    app.add_routes(main_routes)