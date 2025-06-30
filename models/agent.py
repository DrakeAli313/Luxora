from bson import ObjectId
from typing import List
from datetime import datetime

class AgentModel:
    def __init__(self, coll):
        self.coll = coll

    def add_agent_to_city(self, city: str, agent: dict):
        agent["created_at"] = datetime.utcnow()
        self.coll.update_one(
            {"city": city},
            {"$push": {"agents": agent}},
            upsert=True
        )
        return agent

    def get_agents_by_city(self, city: str) -> List[dict]:
        data = self.coll.find_one({"city": city})
        if not data:
            return []
        return data.get("agents", [])

    def get_all_cities(self) -> List[str]:
        return self.coll.distinct("city")
    
    
    def update_agent(self, agent_id: str, update_data: dict):
        return self.coll.update_one(
            {"_id": ObjectId(agent_id)},
            {"$set": update_data}
        )

    def get_agent_by_id(self, agent_id: str):
        return self.coll.find_one({"_id": ObjectId(agent_id)})

    def get_all_agents(self) -> List[dict]:
        cursor = self.coll.find()
        result = []
        for city_doc in cursor:
            city = city_doc.get("city")
            agents = city_doc.get("agents", [])
            for agent in agents:
                result.append({
                    "city": city,
                    **agent,
                    "_id": str(agent.get("_id", ObjectId()))
                })
        return result
