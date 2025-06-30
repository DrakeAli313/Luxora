from fastapi import APIRouter, Depends
from schemas.listing import ListingSchema
from db import get_listing_collection
from models.listing import ListingModel

router = APIRouter()

@router.post("/listings")
def create_listing(data: ListingSchema, coll=Depends(get_listing_collection)):
    listing_model = ListingModel(coll)
    listing_id = listing_model.create_listing(data.dict())
    return {
        "status": "success",
        "listing_id": listing_id,
        "message": "🏡 Listing created successfully! You're one step closer to helping someone find their dream home. 🌟"
    }

@router.get("/listings/{listing_id}")
def get_listing(listing_id: str, coll=Depends(get_listing_collection)):
    listing_model = ListingModel(coll)
    data = listing_model.get_listing(listing_id)
    if not data:
        return {
        "status": "not found",
        "message": "⚠️ No listing found. Please check your listing ID and try again."}
    

    data["_id"] = str(data["_id"])
    return {
        "status": "success",
        "data": data,
        "message": "✨ Here's your listing! Keep going — every detail helps someone make the right decision. 🏠"
    }


@router.get("/listings/category/{category_name}")
def get_listings_by_category(category_name: str, coll=Depends(get_listing_collection)):
    valid_categories = ["Villas", "Luxury", "Apartments"]
    if category_name not in valid_categories:
        return {
            "status": "error",
            "message": f"Invalid category. Choose from {valid_categories}"
        }

    listings = list(coll.find({"category": category_name}))
    for item in listings:
        item["_id"] = str(item["_id"])

    return {
        "status": "success",
        "category": category_name,
        "results": listings,
        "message": f"📂 Showing listings under {category_name} category."
    }
