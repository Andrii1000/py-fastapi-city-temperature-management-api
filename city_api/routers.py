# app/api/cities.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city_api import schemas, crud
from dependencies import get_db


router = APIRouter()


@router.post("/cities/", response_model=schemas.CityList)
async def create_city(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_city(db=db, city=city)


@router.get("/cities/", response_model=list[schemas.CityList])
async def read_cities(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    cities = await crud.get_cities(db, skip=skip, limit=limit)
    return cities


@router.delete("/cities/{city_id}", response_model=schemas.CityList)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.delete_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/cities/{city_id}", response_model=schemas.CityList)
async def update_city(city_id: int, city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    db_city = await crud.update_city(db=db, city_id=city_id, city_update=city)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city
