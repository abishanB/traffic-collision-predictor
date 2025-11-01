from fastapi import APIRouter
from pydantic import BaseModel
import joblib
import numpy as np

router = APIRouter()

# Kernal Density Model for Collision Risk Prediction
load_model_obj: dict = joblib.load("./KernalDensityModel/kd_model.joblib")
kd_model = load_model_obj["model"]
kd_min_risk: int = load_model_obj["min_risk"]
kd_max_risk: int = load_model_obj["max_risk"]


class Coordinates(BaseModel):
  lat: float
  long: float


def classify_risk(score: float) -> str:
  if score < 15:
    return "Low Risk"
  elif score < 60:
    return "Medium Risk"
  else:
    return "High Risk"


@router.post("/predict/collision")
def predict_kernal_density_evaluation(coords: Coordinates) -> object:
  point: np.ndarray = np.array([[coords.lat, coords.long]])
  log_density: np.ndarray = kd_model.score_samples(point)
  risk_score: float = np.exp(log_density)[0]

  # scale of 0 - 100
  normalized_risk_score: float = (
      (risk_score - kd_min_risk) / (kd_max_risk - kd_min_risk)) * 100
  risk_class: str = classify_risk(normalized_risk_score)

  return {"collision_risk_score": normalized_risk_score, "collision_risk_class": risk_class}
