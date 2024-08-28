from fastapi import APIRouter, Depends, HTTPException
import httpx
from typing import List
from app.config.security import verify_admin

router = APIRouter()

HOTEL_SERVICE_URL = "https://8001-marwanachba-bookinghote-o7em0h8zkzw.ws-eu115.gitpod.io"

@router.get("/hotels", response_model=List[dict])
async def get_hotels():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{HOTEL_SERVICE_URL}/hotels")
        return response.json()

@router.post("/hotels", response_model=dict, dependencies=[Depends(verify_admin)])
async def add_hotel(name: str, address: str, rooms: int):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{HOTEL_SERVICE_URL}/hotels",
            params={"name": name, "address": address, "rooms": rooms},
        )
        return response.json()

@router.delete("/hotels/{hotel_id}", dependencies=[Depends(verify_admin)])
async def delete_hotel(hotel_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{HOTEL_SERVICE_URL}/hotels/{hotel_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Hotel not found")
        return {"message": "Hotel deleted"}
