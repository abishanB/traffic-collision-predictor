from fastapi import APIRouter
from pydantic import BaseModel
import geopandas as gpd
from shapely.geometry import Point

router = APIRouter()


class Coordinates(BaseModel):
  lat: float
  long: float


neighbourhoods = gpd.read_file(
  "./routes/toronto_neigbourhoods.geojson")

if neighbourhoods.crs is None or neighbourhoods.crs.to_string() != "EPSG:4326":
  neighbourhoods = neighbourhoods.to_crs(epsg=4326)


def parse_neighbourhood_info(neighbourhood_str: str) -> tuple[str, int]:
  # return name and number separately
  # neighbourhood_str example: "Downtown (31)"
  if not neighbourhood_str or neighbourhood_str == "Unknown":
    return "Unknown", 0

  try:
    name_part = neighbourhood_str.rsplit('(', 1)[0].strip()
    number_part = int(neighbourhood_str.rsplit('(', 1)[1].rstrip(')'))
    return name_part, number_part
  except (IndexError, ValueError):
    return neighbourhood_str, 0


def find_neighbourhood_by_coords(lat: float, lon: float) -> tuple[str, int]:
  point = Point(lon, lat)
  for _, row in neighbourhoods.iterrows():
    if row["geometry"].contains(point):
      neighbourhood = (
          row.get("AREA_NAME")
          or row.get("Neighbourhood")
          or row.get("name")
          or "Unknown"
      )
      return parse_neighbourhood_info(neighbourhood)
  return "Unknown", -1


@router.post("/neighbourhood")
def get_neighbourhood(coords: Coordinates) -> object:
  hood_name, hood_number = find_neighbourhood_by_coords(
    coords.lat, coords.long)
  return {
      "neighbourhood_name": hood_name,
      "neighbourhood_number": hood_number,
      "lat": coords.lat,
      "long": coords.long
  }
