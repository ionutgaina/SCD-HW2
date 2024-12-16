from fastapi import APIRouter, HTTPException, status, Query
from routes.utils import is_valid_objectid
from database import db
from models import Temperature
from bson.objectid import ObjectId
from datetime import datetime
from typing import Optional

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_temperature(temperature: Temperature):

    if not is_valid_objectid(temperature.idOras):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )

    if not db.cities.find_one({"_id": ObjectId(temperature.idOras)}):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
    temperature_data = temperature.dict()
    temperature_data["timestamp"] = datetime.now()
    result = db.temperatures.insert_one(temperature_data)
    return {"id": str(result.inserted_id)}


@router.get("/")
def get_temperatures(
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
    from_: Optional[str] = Query(None, alias="from"),
    until: Optional[str] = Query(None),
):
    query = {}

    if lat is not None and lon is not None:
        cities = list(db.cities.find({"lat": lat, "lon": lon}, {"_id": 1}))
    elif lat is not None:
        cities = list(db.cities.find({"lat": lat}, {"_id": 1}))
    elif lon is not None:
        cities = list(db.cities.find({"lon": lon}, {"_id": 1}))
    else:
        cities = list(db.cities.find({}, {"_id": 1}))

    if not cities:
        return []

    city_ids = [str(city["_id"]) for city in cities]
    query["idOras"] = {"$in": city_ids}

    if from_:
        try:
            from_datetime = datetime.strptime(from_, "%Y-%m-%d")
            query["timestamp"] = {"$gte": from_datetime}
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid 'from' format. Use 'yyyy-mm-dd' (e.g., 2024-12-15)",
            )

    if until:
        try:
            until_datetime = datetime.strptime(until, "%Y-%m-%d")  # Only date, not time
            if "timestamp" not in query:
                query["timestamp"] = {}
            query["timestamp"]["$lte"] = until_datetime
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid 'until' format. Use 'yyyy-mm-dd' (e.g., 2024-12-15)",
            )

    temperatures = list(db.temperatures.find(query))
    if not temperatures:
        return []

    return [
        {
            "id": str(t["_id"]),
            "valoare": t["valoare"],
            "timestamp": t["timestamp"].strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        for t in temperatures
    ]


@router.delete("/{id}")
def delete_temperature(id: str):
    if not is_valid_objectid(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Temperature not found"
        )
    if not db.temperatures.find_one({"_id": ObjectId(id)}):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Temperature not found"
        )
    db.temperatures.delete_one({"_id": ObjectId(id)})
    return {"message": "Temperature deleted successfully"}


@router.put("/{id}")
def update_temperature(id: str, temperature: Temperature):
    if not is_valid_objectid(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Temperature not found"
        )
    if not db.temperatures.find_one({"_id": ObjectId(id)}):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Temperature not found"
        )
    if not is_valid_objectid(temperature.idOras):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid city ID format"
        )
    if not db.cities.find_one({"_id": ObjectId(temperature.idOras)}):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
    db.temperatures.update_one({"_id": ObjectId(id)}, {"$set": temperature.dict()})
    return {"message": "Temperature updated successfully"}


@router.get("/cities/{id_oras}")
def get_temperatures_by_city(
    id_oras: str,
    from_: Optional[str] = Query(None, alias="from"),
    until: Optional[str] = Query(None),
):
    if not is_valid_objectid(id_oras):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )

    query = {"idOras": id_oras}

    if from_:
        try:
            from_datetime = datetime.strptime(from_, "%Y-%m-%d")
            query["timestamp"] = {"$gte": from_datetime}
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid 'from' format. Use 'yyyy-mm-dd' (e.g., 2024-12-15)",
            )

    if until:
        try:
            until_datetime = datetime.strptime(until, "%Y-%m-%d")
            if "timestamp" not in query:
                query["timestamp"] = {}
            query["timestamp"]["$lte"] = until_datetime
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid 'until' format. Use 'yyyy-mm-dd' (e.g., 2024-12-15)",
            )

    temperatures = list(db.temperatures.find(query))
    if not temperatures:
        return []

    return [
        {
            "id": str(t["_id"]),
            "valoare": t["valoare"],
            "timestamp": t["timestamp"].strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        for t in temperatures
    ]


@router.get("/countries/{id_tara}")
def get_temperatures_by_country(
    id_tara: str,
    from_: Optional[str] = Query(None, alias="from"),
    until: Optional[str] = Query(None),
):
    if not is_valid_objectid(id_tara):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Country not found"
        )

    cities = list(db.cities.find({"idTara": id_tara}, {"_id": 1}))
    if not cities:
        return []

    city_ids = [str(city["_id"]) for city in cities]
    query = {"idOras": {"$in": city_ids}}

    if from_:
        try:
            from_datetime = datetime.strptime(from_, "%Y-%m-%d")
            query["timestamp"] = {"$gte": from_datetime}
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid 'from' format. Use 'yyyy-mm-dd' (e.g., 2024-12-15)",
            )

    if until:
        try:
            until_datetime = datetime.strptime(until, "%Y-%m-%d")
            if "timestamp" not in query:
                query["timestamp"] = {}
            query["timestamp"]["$lte"] = until_datetime
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid 'until' format. Use 'yyyy-mm-dd' (e.g., 2024-12-15)",
            )

    temperatures = list(db.temperatures.find(query))

    if not temperatures:
        return []
    return [
        {
            "id": str(t["_id"]),
            "valoare": t["valoare"],
            "timestamp": t["timestamp"].strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        for t in temperatures
    ]
