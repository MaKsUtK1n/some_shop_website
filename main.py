from fastapi import FastAPI, Request, Response
from requests import get
from sqlite3 import Connection
from uvicorn import run
from YM import Yoomoney
from string import ascii_uppercase
from random import choice
from Cryptobot import Send
from yoomoney import Client, Quickpay




app = FastAPI()
send = Send("435799:AAawvE2IJ9ViM4SztaTAe9VJ9uWMF0VOupq")
YM = Yoomoney()
ratio = 0.05
con = Connection("db.db", isolation_level=None, check_same_thread=False)
index_HTML = open("optimized_adapter.html", "rb").read()
steam_HTML = open("steam.html", "rb").read()
cl = Client("4100116694491864.D26471E79D330A489EE6DC31B7C9F67A0F66A2414727961A9FB62E6EB45602E64D814607E62D077B43688AE39F15F168DE3CAE408387ADA13EAC74A2C0EBC198E11EFE0EA34F0A1460AD10EEAC449DC860C52255B7C580333974CDB24AEFD9DE2D00C791B5ABA67F7FFFAF3974E8DD96013C60AFF71B19B5364F1D608CCD91A3")



def calculate_comission(amount: int):
    fee = amount * ratio
    fee = fee if fee < 50 else 50
    return int(amount + fee)

def random_string(length: int):
    return "".join(choice(ascii_uppercase) for _ in range(length))


@app.get("/")
def main(request: Request):
    return Response(index_HTML)


@app.get("/api/inputs")
def inputs(request: Request, deposit: str = None, username: str = None, promo: str = None):
    if deposit != "":
        try:
            deposit = int(float(deposit))
            if deposit < 100:
                return Response("H;deposit cant be less than 100RUB")
        except:
            return Response("H;deposit is WRONG")
    if "#" in username:
        return Response("H;username is WRONG")
    if not username.replace("_", "").isalnum():
        return Response("H;username is WRONG")
    try:
        summ = calculate_comission(deposit)
        return Response(f"S;pay {summ}")
    except:
        return Response("S;pay")
    


@app.get("/pay")
def pay(request: Request, deposit: str = None, username: str = None, promo: str = None):
    cryptobot_invoice = send.create_invoice(int(deposit))
    yoomoney_invoice_id = random_string(16)
    yoomoney_invoice = Quickpay("4100116694491864",
                                "shop",
                                "Sponsor this project",
                                "SB",
                                int(deposit),
                                label=yoomoney_invoice_id)
    with con:
        cursor = con.cursor()
        cursor.execute("INSERT INTO payments VALUES(?,?,?,?)", (yoomoney_invoice_id, int(deposit), cryptobot_invoice['invoice_id'], yoomoney_invoice_id))
    




@app.get("/steam")
def steam(request: Request):
    return Response(steam_HTML)



run(app, host="0.0.0.0", port=80)