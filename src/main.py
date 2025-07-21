import uvicorn
from fastapi import FastAPI

from routers import email_router, event_router, user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(event_router)
app.include_router(email_router)


@app.get("/")
def root():
    return {"message": "API is running"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
