from fastapi import FastAPI

from routes.index import graph_route
from config.db import init_db

app = FastAPI()

# Dependency
@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(graph_route)
