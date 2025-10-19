from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
app = FastAPI()


@app.get("/")
def root():
  return {"OK!"}
