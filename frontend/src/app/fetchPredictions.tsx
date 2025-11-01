export const fetchKernalDensityPrediction = async (lat: number, long: number) => {
  const res = await fetch("http://127.0.0.1:8000/predict/collision", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ lat: lat, long: long }),
  });
  return await res.json()
};

export const fetchHood = async (lat: number, long: number) => {
  const res = await fetch("http://127.0.0.1:8000/neighbourhood", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ lat: lat, long: long }),
  });
  return await res.json()
};

export const fetchSeverityRisk = async (features: object) => {
  const res = await fetch("http://127.0.0.1:8000/predict/severity", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(features),
  });
  return await res.json()
};




