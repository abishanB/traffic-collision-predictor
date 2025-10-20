from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

kd_model = joblib.load("./KernalDensityModel/model.joblib")


class InputData(BaseModel):
  lat: float
  long: float


@app.get("/")
def root():
  return {"OK!"}


@app.post("/predict/kd")
def predict(data: InputData) -> object:
  point = np.array([[data.lat, data.long]])
  log_density = kd_model.score_samples(point)
  risk_score = np.exp(log_density)[0]

  return {"prediction": risk_score}
