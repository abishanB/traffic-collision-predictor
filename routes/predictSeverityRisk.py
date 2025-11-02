from fastapi import APIRouter
from pydantic import BaseModel
import joblib
import pandas as pd

router = APIRouter()

# Random Forest Model for Severity Risk Prediction
load_model_obj = joblib.load("./RandomForestModel/rf_model.joblib")
rf_model = load_model_obj["model"]
feature_names = load_model_obj.get("feature_names", [])


class FeaturesInput(BaseModel):
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
def predict_severity(featuresInput: FeaturesInput) -> object:  # severity risk prediction
  features_data: dict = {
    "LIGHT": [featuresInput.light_condition],
    "VISIBILITY": [featuresInput.visibility],
    "ROAD_CONDITION": [featuresInput.road_condition],
    "DOW": [featuresInput.dow],
    "TIME_OF_DAY": [featuresInput.time_of_day],
    "SEASON": [featuresInput.season],
    "VEHICLE_TYPE": [featuresInput.vehicle_type],
    "DRIVER_ACTION": [featuresInput.driver_action],
    "IMPACT_TYPE": [featuresInput.impact_type],
    "NEIGHBOURHOOD": [featuresInput.neighbourhood],
    "AGE_RANGE": [featuresInput.age_range]
  }
  features_df: pd.DataFrame = pd.DataFrame(features_data)

  severity_probability: float = rf_model.predict_proba(features_df)[0][1]
  severity_risk_class: str = classify_risk(severity_probability)
  return {
    "severity_risk_score": severity_probability,
    "severity_risk_class": severity_risk_class
  }
