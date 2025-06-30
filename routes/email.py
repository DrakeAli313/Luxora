from fastapi import APIRouter, Depends, HTTPException
from schemas.email import ListingEmailRequest
from db import get_listing_collection
from bson import ObjectId
from utils.mailer import send_listing_email

router = APIRouter()

@router.post("/send-listing-email")
def send_listing_info_email(data: ListingEmailRequest, coll=Depends(get_listing_collection)):
    listing = coll.find_one({"_id": ObjectId(data.listing_id)})

    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    # Build email body
    body = f"""
🏠 Listing Info:

Title: {listing.get('title')}
Price: ${listing.get('total_price')}
Area: {listing.get('total_area')} sq.ft.
Location: {listing.get('location')}
Bathrooms: {listing.get('bathrooms')}
Garages: {'Yes' if listing.get('garages') else 'No'}
Features: {', '.join(listing.get('features', []))}

Thanks for using our service!
Real Estate Team
"""

    send_listing_email(
        receiver_email=data.receiver_email,
        subject=f"Listing Details: {listing.get('title')}",
        body=body
    )

    return {"status": "success", "message": "Listing email sent successfully."}
