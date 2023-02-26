import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Query
from wa_me.wa_me import Bot


app = FastAPI()
bot = Bot()

load_dotenv()

PHONE_ID = os.environ["PHONE_ID"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
VERIFY_TOKEN = os.environ["VERIFY_TOKEN"]

bot.start(phone_id=PHONE_ID, token=ACCESS_TOKEN)

@app.get("/")
async def ping(
    token: str = Query(alias="hub.verify_token"),
    challenge: str = Query(alias="hub.challenge"),
):
    if token == VERIFY_TOKEN:
        print(token, challenge)
        return str(challenge)
    return "Invalid verify token"

@app.post("/echo")
async def echo_bot(request: Request):
    data = await request.json()
    print(data)
    bot.handle(data)
    return "Success"
