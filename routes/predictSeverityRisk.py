from fastapi import APIRouter
from pydantic import BaseModel
import joblib
import pandas as pd

router = APIRouter()

# Random Forest Model for Severity Risk Prediction
load_model_obj = joblib.load("./RandomForestModel/rf_model.joblib")
rf_model = load_model_obj["model"]
feature_names = load_model_obj.get("feature_names", [])


class Features(BaseModel):
  neighbourhood: str
  light_condition: str
  visibility: str
  road_condition: str
  time_of_day: str
  dow: str
  season: str
  vehicle_type: str
  driver_action: str
  impact_type: str
  age_range: str


def classify_risk(probability: float) -> str:
  if probability <= 0.50:
    return "Low Risk"
  elif probability <= 0.80:
    return "Medium Risk"
  else:
    return "High Risk"


@router.post("/predict/severity")
def predict_severity(features: Features) -> object:  # severity risk prediction
  features_data = {
    "LIGHT": [features.light_condition],
    "VISIBILITY": [features.visibility],
    "ROAD_CONDITION": [features.road_condition],
    "DOW": [features.dow],
    "TIME_OF_DAY": [features.time_of_day],
    "SEASON": [features.season],
    "VEHICLE_TYPE": [features.vehicle_type],
    "DRIVER_ACTION": [features.driver_action],
    "IMPACT_TYPE": [features.impact_type],
    "NEIGHBOURHOOD": [features.neighbourhood],
    "AGE_RANGE": [features.age_range]
  }
  features_df = pd.DataFrame(features_data)

  severity_probability = rf_model.predict_proba(features_df)[0][1]
  severity_risk_class = classify_risk(severity_probability)
  return {
    "severity_risk_score": severity_probability,
    "severity_risk_class": severity_risk_class
  }
