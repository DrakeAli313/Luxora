from pymongo.collection import Collection
from bson import ObjectId

class ListingModel:
    def __init__(self, collection: Collection):
        self.collection = collection

    def create_listing(self, data: dict) -> str:
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def get_listing(self, listing_id: str) -> dict:
        return self.collection.find_one({"_id": ObjectId(listing_id)})
