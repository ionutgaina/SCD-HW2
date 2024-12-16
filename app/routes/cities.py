from fastapi import APIRouter, HTTPException, status
from routes.utils import is_valid_objectid
from database import db
from models import City
from bson.objectid import ObjectId

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_city(city: City):
    if not is_valid_objectid(city.idTara):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Country not found"
        )
    if not db.countries.find_one({"_id": ObjectId(city.idTara)}):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Country not found"
        )
    if db.cities.find_one({"idTara": city.idTara, "nume": city.nume}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="City already exists in the specified country",
        )
    result = db.cities.insert_one(city.dict())
    return {"id": str(result.inserted_id)}


@router.get("/")
def get_cities():
    cities = list(db.cities.find())
    return [
        {
            "id": str(c["_id"]),
            "idTara": c["idTara"],
            "nume": c["nume"],
            "lat": c["lat"],
            "lon": c["lon"],
        }
        for c in cities
    ]


@router.get("/country/{id_tara}")
def get_cities_by_country(id_tara: str):
    if not is_valid_objectid(id_tara):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Country not found"
        )
    cities = list(db.cities.find({"idTara": id_tara}))
    return [
        {
            "id": str(c["_id"]),
            "idTara": c["idTara"],
            "nume": c["nume"],
            "lat": c["lat"],
            "lon": c["lon"],
        }
        for c in cities
    ]


@router.put("/{id}")
def update_city(id: str, city: City):
    if not is_valid_objectid(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Country not found"
        )
    if not db.cities.find_one({"_id": ObjectId(id)}):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
    if not is_valid_objectid(city.idTara):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid country ID format"
        )
    if not db.countries.find_one({"_id": ObjectId(city.idTara)}):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Country not found"
        )
    db.cities.update_one({"_id": ObjectId(id)}, {"$set": city.dict()})
    return {"message": "City updated successfully"}


@router.delete("/{id}")
def delete_city(id: str):
    if not is_valid_objectid(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Country not found"
        )
    if not db.cities.find_one({"_id": ObjectId(id)}):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
    db.cities.delete_one({"_id": ObjectId(id)})
    return {"message": "City deleted successfully"}
