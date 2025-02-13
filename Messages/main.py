import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pusher import Pusher
from fastapi import Request
from sqlalchemy.orm import Session
from core.database import get_db, Base, engine
from model.services import create_message, get_all_messages
from model.models import Users, Messages
from model.schemas import users

app = FastAPI()
Base.metadata.create_all(engine)

# isko mene pusher ki website se menu mn app key pr click kr k waha se liya hai.
pusher_client = Pusher(
    app_id="1939974",
    key="b97eb7652c72bc68f79c",
    secret="c0a7d2087776e3dff096",
    cluster="ap2",
    ssl=True
)

templates = Jinja2Templates(directory="templates")  #fastapi ko html k page se connect krne k liye jinja templating use krni hoti hai. yaha pr templates ek dusra folder hai.
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/save_username")
async def save_username(user : users, db: Session = Depends(get_db)):
    db_user = Users(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    db_message = Messages(content=user.message)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    return {"message": "Username and message saved successfully", "username": user.username, "message": user.message}

active_connections = []


@app.websocket("/ws/chat")
async def chat(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    
    old_messages = get_all_messages(db)
    messages = [{"username": msg.username, "content": msg.content} for msg in old_messages]
    await websocket.send_json(messages)

    active_connections.append(websocket) 

    try:
        while True:
            message_data = await websocket.receive_text()

            try:
                data = json.loads(message_data)
                message = data["message"]  
                username = data["username"]  
                
                create_message(db=db, message=message, username=username)

                for connection in active_connections:
                    if connection != websocket:  
                        await connection.send_text(f"{username}: {message}")

                pusher_client.trigger('chat-channel', 'new-message', {'username': username, 'message': message})

            except json.JSONDecodeError:
                print("Received invalid message format")

    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print("Client disconnected")