import os
import json
from dotenv import load_dotenv
from typing import Optional
from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import PlainTextResponse

from wa_me.wa_me import Bot
import hmac
import requests

app = FastAPI()
bot = Bot()

load_dotenv()

PHONE_ID = os.environ["PHONE_ID"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
VERIFY_TOKEN = os.environ["VERIFY_TOKEN"]

bot.start(phone_id=PHONE_ID, token=ACCESS_TOKEN)

# @app.get("/webhook")
# async def ping(
#     token: str = Query(alias="hub.verify_token"),
#     challenge: str = Query(alias="hub.challenge"),
# ):
#     if token == VERIFY_TOKEN:
#         print(token, challenge)
#         return str(challenge)
#     return "Invalid verify token"

@app.get("/webhook")
async def verify_token(
        verify_token: Optional[str] = Query(None, alias="hub.verify_token", regex="^[A-Za-z1-9-_]*$"),
        challenge: Optional[str] = Query(None, alias="hub.challenge", regex="^[A-Za-z1-9-_]*$"),
        mode: Optional[str] = Query("subscribe", alias="hub.mode", regex="^[A-Za-z1-9-_]*$"),
) -> Optional[str]:
    token = VERIFY_TOKEN
    if not token:
        print(
            "🔒Token not defined. Must be at least 8 chars or numbers."
            "💡Tip: set -a; source .env; set +a"
        )
        raise HTTPException(status_code=500, detail="Webhook unavailable.")
    elif verify_token == token and mode == "subscribe":
        return PlainTextResponse(f"{challenge}")
    else:
        raise HTTPException(status_code=403, detail="Token invalid.")


@app.post("/webhook")
async def echo_bot(request: Request):
    data = await request.json()
    print(data)
    msg = data.get('entry')[0].get('changes')[0].get('value').get('messages')[0].get('text').get('body')
    print(msg)
    # bot.handle(data)
    return str(msg)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
