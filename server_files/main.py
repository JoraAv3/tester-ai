from __future__ import annotations
import json
import uuid
import httpx
import requests
from typing import Union, Optional, List, Dict
import tiktoken
import asyncio

from fastapi import FastAPI, File, HTTPException, Depends, Request, UploadFile, WebSocket, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse

from starlette.responses import Response, RedirectResponse
from pydantic import ValidationError

from tester.router import MessageCreate, SessionLocal, User, UserCreate, UserResponse, UserTokens, get_db, get_hashed_password, SignInResponse, \
    SignInRequest, verify_password, GoogleDataResponse, GoogleRegistrationCreate, MessageOrm

from wolverine_main.wolverine.wolverine import send_message_to_gpt, apply_message_changes


def get_application() -> FastAPI:
    application = FastAPI(openapi_url='')
    # application.config["PREFERRED_URL_SCHEME"] = "https"
    return application

# openapi_url=''


origins = [
    '*'
]

app = get_application()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
    max_age=600,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConnectionManager:
    def __init__(self):
        self.connections: Dict = {}

    async def connect(self, websocket: WebSocket, token: str):
        await websocket.accept()
        self.connections[token] = websocket

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, data: str, token: str):
        print("token", token, self.connections)
        await self.connections[token].send_text(data)


manager = ConnectionManager()


def send_to_gpt(message_response, user: User):
    global manager
    print("message_response", message_response)

    async def broadcast():
        global manager
        await manager.broadcast(json.dumps(
            {"question_id": answer_message_response.question_id, "text": answer_message_response.text}), user.token_id)
    try:
        gpt_check = send_message_to_gpt(
            message_response.text, args=[], error_message='')

        answer_message = apply_message_changes(
            message=message_response.text, changes=gpt_check)
        answer_message_response = save_message(
            answer_message, user, message_response.id)
        asyncio.run(broadcast())
    except Exception as err:
        print("error", err)


@app.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    await manager.connect(websocket, token)
    while True:
        data = await websocket.receive_text()
        await manager.broadcast(data, token)


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def get_started(request: Request):
    return templates.TemplateResponse("getstarted.html", {"request": request})


@app.get("/chat", response_class=HTMLResponse)
async def get_started(request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request})


@app.get("/tarif", response_class=HTMLResponse)
async def get_started(request: Request):
    return templates.TemplateResponse("upgradeplan.html", {"request": request})


@app.post('/signup', response_model=UserResponse)
def save_data(data: UserCreate, response: Response):
    try:
        db = SessionLocal()
        hashed_password = get_hashed_password(data.password)
        token_id = str(uuid.uuid4())
        user = User(email=data.email, password=hashed_password, registered_at=data.registered_at,
                    token_id=token_id)
        db.add(user)
        db.commit()
        db.refresh(user)

        tokens = UserTokens(user_id=user.id)
        db.add(tokens)
        db.commit()
        db.refresh(tokens)
        return {'token_id': user.token_id}
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as error:
        response.status_code = 400
        return {'message': f'{error}'}


def verify_token(req: Request):
    token = req.headers["Authorization"].replace("Bearer", "").lstrip()
    db = get_db()
    verified_user = db.query(User).filter(User.token_id == token).first()
    if verified_user:
        return verified_user
    return None


@app.get('/check-user')
def check_user(user: User = Depends(verify_token)):
    if user:
        return list(user.messages)
    raise HTTPException(
        status_code=403, detail='Authorization is needed')


@app.post('/signin', response_model=SignInResponse)
def sign_in(data: SignInRequest):
    db = SessionLocal()
    user = db.query(User).filter(User.email == data.email).first()

    if user and verify_password(data.password, user.password):
        setattr(user, "token_id", str(uuid.uuid4()))
        db.commit()
        db.refresh(user)
        return {'token_id': user.token_id}
    else:
        raise HTTPException(
            status_code=401, detail='Invalid email or password')


# AIzaSyDSd9wufqjLYT8MlTqDV-ClqmOF5UJ6gRk

@app.get('/registeration/google')
async def reg_google(request: Request, response: Response):
    try:
        data = dict(request.query_params)
        db = SessionLocal()
        # token_url = "https://oauth2.googleapis.com/token"
        # token_data = {
        # "code": data.get("id"),
        # "client_id": "283997917725-svbidm10v7aksu9pe67m0f2vbpohh75i.apps.googleusercontent.com",
        # "client_secret": "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",
        # "redirect_uri": "https:/app.tester-ai.com/chat",
        # "grant_type": "authorization_code",
        # "scope": "https://oauth2.googleapis.com/auth/cloud-platform"
        # }
        # print("Before token_response")
        # token_response = requests.post(token_url, data=token_data)
        # print("token_response", token_response)
        # if token_response.status_code == 200:
        # token_json = token_response.json()
        # access_token = token_json["access_token"]
        # profile_url = "https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses"
        # headers = {"Authorization": f"Bearer {access_token}"}

        # print("access_token", access_token)
        # profile_response = requests.get(profile_url, headers=headers)
        # print("profile_response", profile_response)
        # if profile_response.status_code == 200:
        token_id = data.get("jti")
        existing_google_user = db.query(User).filter(
            User.google_id == data.get("id")).first()

        if existing_google_user:
            print("Пользователь уже существует:",
                  existing_google_user.login, token_id)
            existing_google_user.token_id = token_id
            db.commit()
            db.refresh(existing_google_user)
        else:
            google_data = User(
                login=data.get("email"), token_id=token_id, google_id=data.get("id"))
            db.add(google_data)
            db.commit()
            db.refresh(google_data)

            tokens = UserTokens(user_id=google_data.id)
            db.add(tokens)
            db.commit()
            db.refresh(google_data)

        return {'token': google_data.token_id}
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as error:
        print("google error", error)
        response.status_code = 400
        return {'message': f'{error}'}


@app.get("/auth/google")
async def google_login(*args, **kwargs):
    print(args, kwargs)


github_client_id = '35b417b8af88e62aeecd'
github_client_secret = '28d0094b06e492b87836752fb39390d5a22477ca'


@app.get('/github-login')
async def github_login():
    return RedirectResponse(f'https://github.com/login/oauth/authorize?client_id={github_client_id}', status_code=302)


@app.get('/github-code')
async def github_code(code: str, request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request})


@app.get('/github-user')
async def github_code(code: str, request: Request):
    try:
        db = SessionLocal()
        params = {
            'client_id': github_client_id,
            'client_secret': github_client_secret,
            'code': code
        }
        headers = {'Accept': 'application/vnd.github+json'}
        async with httpx.AsyncClient() as client:
            response = await client.post(url='https://github.com/login/oauth/access_token', params=params, headers=headers)
            response_json = response.json()
            access_token = response_json['access_token']
            headers.update({'Authorization': f'bearer {access_token}'})

            response = await client.get('https://api.github.com/user', headers=headers)
            user_data = response.json()
            login = user_data.get('login')
            github_id = user_data.get("id")
            name = user_data.get("name")
            token_id = access_token

            if not github_id:
                raise HTTPException(
                    status_code=403, detail="Invalid Github credentials.")

            existing_github_user = db.query(User).filter(
                User.github_id == github_id).first()

            if existing_github_user:
                print("Пользователь уже существует:",
                      existing_github_user.login, token_id)
                existing_github_user.token_id = token_id
                db.commit()
                db.refresh(existing_github_user)
            else:
                github_user = User(
                    login=login, github_id=github_id, name=name, token_id=token_id)
                db.add(github_user)
                db.commit()
                db.refresh(github_user)

                tokens = UserTokens(user_id=github_user.id)
                db.add(tokens)
                db.commit()
                db.refresh(tokens)
                print(
                    "Новый пользователь добавлен в базу данных:", github_user.login)
        return {'token': token_id}
    except Exception as error:
        print("error", error)
        raise HTTPException(
            status_code=403, detail="Invalid Github credentials.")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def save_message(message: str, user: User, question_id: Optional[Union[int, None]] = None):
    db = SessionLocal()
    db_message = MessageOrm(
        text=message,
        user_id=user.id,
        question_id=question_id
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


@app.post("/messages")
async def create_message(message: MessageCreate, background_tasks: BackgroundTasks, verified_user: User = Depends(verify_token)):
    try:
        if not verified_user:
            raise Exception("Authorization needed")

        db = get_db()
        user = db.query(User).filter(User.id == verified_user.id).first()

        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        text_lenqth = encoding.encode(message.text)
        if len(text_lenqth) > user.tokens.tokens:
            return MessageOrm(text="Upgrade your plan to send messages now", user_id=user.id, question_id=user.messages[-1].id)

        messages_count = db.query(MessageOrm).filter(
            MessageOrm.question_id == None, MessageOrm.user_id == user.id).count()
        if user.tokens.message_count <= messages_count:
            return MessageOrm(text="Upgrade your plan to send messages", user_id=user.id, question_id=user.messages[-1].id)

        message_response = save_message(message.text, user)

        background_tasks.add_task(send_to_gpt, message_response, user)

        return {"question_id": message_response.id, "text": "You will give answer from chat GPT after a while"}
    except Exception as error:
        print("\nerror", error, "\n")
        return MessageOrm(text="Please type your question again after a few minutes", user_id=user.id)


@app.post("/file/upload")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...), verified_user: User = Depends(verify_token)):
    try:
        if not verified_user:
            raise Exception("Authorization needed")

        db = SessionLocal()
        user = db.query(User).filter(User.id == verified_user.id).first()

        content = await file.read()

        messages_count = db.query(MessageOrm).filter(
            MessageOrm.question_id == None, MessageOrm.user_id == user.id).count()
        if user.tokens.message_count <= messages_count:
            return MessageOrm(text="Upgrade your plan to send messages", user_id=user.id, question_id=user.messages[-1].id)

        message_response = save_message(content.decode(), user)

        if message_response == '':
            raise Exception('Enter your question')

        background_tasks.add_task(
            send_to_gpt, message_response, user)
        return {"id": message_response.id, "text": message_response.text}
    except Exception as error:
        print(error)
        return MessageOrm(text="Please type your question again after a few minutes", user_id=user.id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8090)
