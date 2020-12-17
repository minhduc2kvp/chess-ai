from aiohttp import web
from aiohttp.web import Response
from json import loads, dumps

from app.service.predict_chess import predict


main_routes = web.RouteTableDef()


@main_routes.get("/home")
async def home(request):
    file = open("app/Templates/index.html", "r")
    html = file.read()
    return Response(text=html, content_type="text/html")


@main_routes.post("/api/game")
async def game(request):
    body = await request.text()
    result = predict(loads(body))
    return Response(text=str(result))