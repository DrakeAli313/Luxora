from pydantic import BaseModel, EmailStr

class ListingEmailRequest(BaseModel):
    listing_id: str
    receiver_email: EmailStr
