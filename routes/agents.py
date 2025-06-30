from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from pymongo.collection import Collection
from datetime import datetime
from uuid import uuid4
from db import get_listing_collection, get_db
from models.agent import AgentModel
from utils.upload import UploadImage

router = APIRouter()

@router.post("/agents/upload")
async def upload_agent(
    city: str = Form(...),
    name: str = Form(...),
    profession: str = Form(...),
    image: UploadFile = File(...),
    coll: Collection = Depends(get_listing_collection),
    db = Depends(get_db)
):
    # ✅ Get log collection
    log_coll = db.get_collection("cdn_contents")

    # ✅ Upload image with log collection
    image_url = UploadImage.upload_to_digital_ocean(image, "agents", log_coll)
    
    # # ✅ Upload the image to DigitalOcean
    # image_url = UploadImage.upload_to_digital_ocean(image, "agents")

    if not image_url:
        raise HTTPException(status_code=500, detail="Image upload failed.")

    # ✅ Prepare agent object
    agent = {
        "agent_id": str(uuid4()),  # 🔥 Add this line here
        "image": image_url,
        "name": name,
        "profession": profession,
        "created_at": datetime.utcnow()
    }

    # ✅ Save agent in MongoDB using the model
    agent_model = AgentModel(coll)
    agent_model.add_agent_to_city(city, agent)

    return {
        "status": "success",
        "message": f"Agent added successfully under city: {city}",
        "agent": agent
    }

@router.get("/agents/by-city/{city_name}")
def get_agents_by_city(city_name: str, coll: Collection = Depends(get_listing_collection)):
    city_doc = coll.find_one({"city": city_name})

    if not city_doc:
        raise HTTPException(status_code=404, detail=f"No agents found for city: {city_name}")

    agents = city_doc.get("agents", [])

    return {
        "status": "success",
        "city": city_name,
        "total_agents": len(agents),
        "agents": agents
    }


# ✅ GET agent by ID
@router.get("/agents/{agent_id}")
def get_agent(agent_id: str, coll: Collection = Depends(get_listing_collection)):
    agent_model = AgentModel(coll)
    data = agent_model.get_agent_by_id(agent_id)
    if not data:
        raise HTTPException(status_code=404, detail="Agent not found")
    data["_id"] = str(data["_id"])
    return {"status": "success", "data": data}

# ✅ PUT update agent
@router.put("/agents/{agent_id}/update")
async def update_agent(
    agent_id: str,
    name: str = Form(None),
    profession: str = Form(None),
    city: str = Form(None),
    image: UploadFile = File(None),
    coll: Collection = Depends(get_listing_collection),
    db = Depends(get_db)
):
    update_fields = {}

    if name:
        update_fields["name"] = name
    if profession:
        update_fields["profession"] = profession
    if city:
        update_fields["city"] = city

    if image:
        log_coll = db.get_collection("cdn_contents")
        image_url = UploadImage.upload_to_digital_ocean(image, "agents", log_coll)
        if not image_url:
            raise HTTPException(status_code=500, detail="Image upload failed.")
        update_fields["image"] = image_url

    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update.")

    agent_model = AgentModel(coll)
    result = agent_model.update_agent(agent_id, update_fields)

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Agent not found.")

    return {"status": "success", "message": "Agent updated successfully"}