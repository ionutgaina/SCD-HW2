from fastapi import APIRouter, HTTPException, status
from bson.objectid import ObjectId
from routes.utils import is_valid_objectid
from models import Country
from database import db

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_country(country: Country):
    if db.countries.find_one({"nume": country.nume}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Country already exists"
        )
    result = db.countries.insert_one(country.dict())
    return {"id": str(result.inserted_id)}


@router.get("/")
def get_countries():
    countries = list(db.countries.find())
    return [
        {"id": str(c["_id"]), "nume": c["nume"], "lat": c["lat"], "lon": c["lon"]}
        for c in countries
    ]


@router.put("/{id}")
def update_country(id: str, country: Country):
    if not is_valid_objectid(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Country not found"
        )
    if not db.countries.find_one({"_id": ObjectId(id)}):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Country not found"
        )
    db.countries.update_one({"_id": ObjectId(id)}, {"$set": country.dict()})
    return {"message": "Country updated successfully"}


@router.delete("/{id}")
def delete_country(id: str):
    if not is_valid_objectid(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Country not found"
        )
    if not db.countries.find_one({"_id": ObjectId(id)}):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Country not found"
        )
    db.countries.delete_one({"_id": ObjectId(id)})
    return {"message": "Country deleted successfully"}
