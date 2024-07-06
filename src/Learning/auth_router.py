from fastapi import APIRouter

route = APIRouter()

@route.get("/routerget")
def routetest():
    return {"the route":"looks good"}