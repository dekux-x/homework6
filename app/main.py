import json

from fastapi import Cookie, FastAPI, Form, Request, Response, templating
from fastapi.responses import RedirectResponse
from jose import jwt

from .flowers_repository import Flower, FlowersRepository
from .purchases_repository import Purchase, PurchasesRepository
from .users_repository import User, UsersRepository

app = FastAPI()
templates = templating.Jinja2Templates("templates")


flowers_repository = FlowersRepository()
purchases_repository = PurchasesRepository()
users_repository = UsersRepository()


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/signup")
def sign_up(request: Request):
    return templates.TemplateResponse("/app/signup.html",{"request": request})

@app.post("/signup")
def post_sign_ap(
        response: Response,
        full_name: str = Form(),
        email: str = Form(),
        password: str = Form(),
        ):
    if users_repository.get_by_email(email):
        response.status_code = 404
        return Response("There is already exist such user", status_code=404)
    user = User(email, full_name,  password)
    users_repository.save(user)
    return RedirectResponse("/login", status_code=303)

def encode_jwt(user_id: str):
    body = {"user_id": user_id}
    token = jwt.encode(body, "saidshabekov", "HS256")
    return token

def decode_jwt(token: str):
    body = jwt.decode(token, "saidshabekov", "HS256")
    return body["user_id"]

@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse("/app/login.html", {"request": request})

@app.post("/login")
def post_login( email: str = Form(), password: str = Form()):
    users = users_repository.get_all()
    for user in users:
        if user.email == email and user.password == password:
            response = RedirectResponse("/profile", status_code=303)
            token = encode_jwt(user.id)
            response.set_cookie("token", token)
            return response
    return Response("There is no such user", status_code=404)

@app.get("/profile")
def profile(request: Request, token: str = Cookie()):
    user_id = decode_jwt(token)
    user = users_repository.get_by_id(user_id)
    if user:
        return templates.TemplateResponse("/app/profile.html", {"request": request, "user": user})
    return Response("There is problems with cookie", status_code=404)

@app.get("/flowers")
def get_flowers( request: Request):
    flowers = flowers_repository.get_all()
    return templates.TemplateResponse("/app/flowers.html", {"request": request, "flowers": flowers})

@app.post("/flowers")
def post_flowers(name: str = Form(),
                 count: str = Form(),
                 cost: str = Form(),):
    flower = Flower(name, count, cost)
    flowers_repository.save(flower)
    return RedirectResponse("/flowers", status_code=303)



@app.get("/cart/items")
def cart_items(request: Request, cart: str = Cookie(default="[]")):
    cart_json = json.loads(cart)
    total = 0
    for i in cart_json:
        total += int(i["cost"])
    return templates.TemplateResponse("/app/cart/items.html",{
        "request": request,
        "cart": cart_json,
        "total": total
    })


@app.post("/cart/items")
def post_cart_items(response: Response, flower_id: int = Form(), cart = Cookie(default="[]")):
    flower = flowers_repository.get_by_id(flower_id)
    cart_json = json.loads(cart)
    if flower:
        data = {"id": flower.id, "name": flower.name, "cost": flower.cost}
        cart_json.append(data)
        new_cart = json.dumps(cart_json)
        response = RedirectResponse("/flowers", status_code=303)
        response.set_cookie("cart", new_cart)
    return response

@app.get("/purchased")
def get_purchase(request: Request, token: str = Cookie()):
    user_id = decode_jwt(token)
    purchases = purchases_repository.get_all_by_id(user_id)
    flowers = []
    for purchase in purchases:
        flower = flowers_repository.get_by_id(purchase.flower_id)
        if flower:
            flowers.append(flower)
    return templates.TemplateResponse("/app/purchases.html", {
        "request": request,
        "flowers": flowers
    })

@app.post("/purchased")
def post_purchase(cart: str = Cookie(default="[]"), token: str = Cookie()):
    user_id = decode_jwt(token)
    cart_json = json.loads(cart)
    for i in cart_json:
        purchase = Purchase(user_id, i["id"])
        purchases_repository.save(purchase)
    return RedirectResponse("/purchased", status_code=303)