from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import neighbourhood, predictCollisionRisk, predictSeverityRisk

app: FastAPI = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
  return {"OK!"}


app.include_router(predictCollisionRisk.router)
app.include_router(predictSeverityRisk.router)
app.include_router(neighbourhood.router)
