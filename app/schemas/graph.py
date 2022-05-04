from typing import List,Optional
from pydantic import BaseModel

class GrafoRota(BaseModel):
    source: str
    target: str
    distance: int
    grafo_id: Optional[int] = None

class Grafo(BaseModel):
    data: List[GrafoRota] = []