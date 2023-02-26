import os
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from fastapi import FastAPI, Response, Request


load_dotenv()

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
twil_whatsapp_number = os.environ["TWILIO_WHATSAPP_NUMBER"]
client = Client(account_sid, auth_token)

app = FastAPI()

def send_message(body_text):
    client.messages.create(
        body=body_text,
        from_="whatsapp:"+twil_whatsapp_number,
        to="whatsapp:+6591878206"
    )

@app.get("/")
async def index():
    return {"message": "hello world!"}

@app.post("/echo")
async def echo_msg(request: Request):
    """
    echos a user's message back
    """
    data = await request.form()
    print(data)
    msg = data.get('Body')
    phone_number = data.get('From')
    print(phone_number.split(':')[-1])
    # resp = MessagingResponse()
    # resp.message(f"User said: {msg}")
    # return Response(content=str(resp), media_type='application/xml')
    return send_message(msg)
