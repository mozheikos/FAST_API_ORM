import fastapi
import uvicorn
from endpoints import users, auth

app = fastapi.FastAPI()
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/login", tags=["login"])

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host='0.0.0.0', reload=True)
