from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from src.controller.debt_controller import router as debt_controller
from src.controller.group_controller import router as group_controller
from src.controller.login_controller import router as login_controller
from src.controller.payment_controller import router as payment_controller
from src.controller.user_controller import router as user_controller
from src.controller.user_invitation_controller import router as user_invitation_controller
from src.controller.user_in_group_controller import router as user_in_group_controller
from src.database.database import init_db

ALLOWED_ORIGINS = [
                    "http://localhost:5173", 
                   ]

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

#asyncio.get_event_loop()

app = FastAPI(lifespan=lifespan)

@app.head("/")
def head():
    return

@app.get("/")
def home():
    return {"message": "Bienvenido a OurExpenses"}

app.title = "OurExpenses"
app.version = "1.0"

app.add_middleware(CORSMiddleware,
            allow_origins=ALLOWED_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            )

app.include_router(user_controller)
app.include_router(debt_controller)
app.include_router(group_controller)
app.include_router(login_controller)
app.include_router(payment_controller)
app.include_router(user_invitation_controller)
app.include_router(user_in_group_controller)
