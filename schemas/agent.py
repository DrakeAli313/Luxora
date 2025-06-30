from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class AgentData(BaseModel):
    image: HttpUrl
    name: str
    profession: str

class CityAgentRequest(BaseModel):
    city: str
    agents: List[AgentData]


class AgentUpdateSchema(BaseModel):
    name: Optional[str]
    profession: Optional[str]
    city: Optional[str]