from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session

from config.db import get_db
from models.index import graph as graph_model
from schemas.index import Grafo



graph_route = APIRouter()


# @graph_route.get("/graph/")
# async def read_graph( db: Session = Depends(get_db)):
#     db_graph = graph_model.get_graph(db)
#     if db_graph is None:
#         raise HTTPException(status_code=404, detail="Graph not found")
#     return db_graph

@graph_route.get("/graph/{graphId}")
async def read_graphs(graphId: int, db: Session = Depends(get_db)):
    db_graph = graph_model.get_graph(db, graph_id=graphId)
    if db_graph is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Graphs not found")
    return db_graph


@graph_route.post("/graph/", status_code=status.HTTP_201_CREATED)
async def write_graph(graph: Grafo, db: Session = Depends(get_db)):    
    result = graph_model.create_graph(db,graph)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ocorreu um erro ao criar grafo")
    return result 

@graph_route.get("/routes/{graphId}/from/{town1}/to/{town2}")
async def read_all_routes(graphId: int,town1: str, town2: str, maxStops:int = 0,db: Session = Depends(get_db) ):
    routes = graph_model.get_all_routes(db, graphId,town1,town2,maxStops)
    if routes is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Routes not found")
    return routes

@graph_route.get("/distance/{graphId}/from/{town1}/to/{town2}")
async def read_minimum_distance(graphId: int,town1: str, town2: str,db: Session = Depends(get_db) ):
    routes = graph_model.minimum_distance(db, graphId,town1,town2)
    if routes is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Distance not found")
    return routes

