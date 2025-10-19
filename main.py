from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

kde_model = joblib.load("./KernalDensityModel/model.pkl")


class InputData(BaseModel):
  lat: float
  long: float


@app.get("/")
def root():
  return {"OK!"}


@app.post("/predict")
def predict(data: InputData):
  point = np.array([[data.lat, data.long]])
  log_density = kde_model.score_samples(point)
  risk_score = np.exp(log_density)[0]

  return {"prediction": risk_score}
