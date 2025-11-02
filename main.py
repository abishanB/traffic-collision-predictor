from fastapi import FastAPI, Request
import time
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


@app.middleware("http")
async def log_request_time(request: Request, call_next):
  start_time = time.time()
  response = await call_next(request)
  duration = (time.time() - start_time) * 1000
  print(f"{request.method} {request.url.path} completed in {duration:.2f} ms")
  return response


@app.get("/")
def root():
  return {"OK!"}


app.include_router(predictCollisionRisk.router)
app.include_router(predictSeverityRisk.router)
app.include_router(neighbourhood.router)
