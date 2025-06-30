from pydantic import BaseModel, Field
from typing import Optional, List

class ListingSchema(BaseModel):
    title: str
    total_price: float
    total_area: float
    location: str
    bathrooms: int
    garages: bool
    features: Optional[List[str]] = [],
    category: str = Field(..., description="One of: Villas, Luxury, Apartments")


class ListingResponse(ListingSchema):
    id: str
