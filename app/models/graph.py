from sqlalchemy import ForeignKey, Column
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.orm import relationship,deferred
import networkx as nx
from config.db import Base

class Graphs(Base):
    __tablename__ = 'Graphs'
    __table_args__= {
        'mysql_engine':'InnoDB'
    }
    id = Column(Integer, primary_key=True,index=True,autoincrement=True)
    data = relationship("Graphs_routes", back_populates="graph",lazy='joined')

class Graphs_routes(Base):
    __tablename__ = 'Graphs_routes'
    __table_args__= {
        'mysql_engine':'InnoDB'
    }
    id = Column(Integer, primary_key=True,index=True,autoincrement=True)
    source = Column(String(255))
    target = Column(String(255))
    distance = Column(Integer)
    grafo_id = deferred(Column(Integer,ForeignKey('Graphs.id'),index=True))
    graph = relationship("Graphs", back_populates="data")

#MyISAM nao suporta ForeignKey


def create_graph(db,graph):
    db_graph = Graphs()
    
    db.add(db_graph)
    db.commit()
    db.refresh(db_graph)

    db_route = formatting_route_graph(graph,db_graph.id)

    db.add_all(db_route)
    db.commit()
    
    result_raw  = db.query(Graphs).filter(Graphs.id == db_graph.id).first()
    result = formatting_graph_result(result_raw) 
    return result

def get_graph(db, graph_id = None):
    if graph_id:
        result_raw = db.query(Graphs).filter(Graphs.id == graph_id).first()
        if result_raw:
            result_raw = formatting_graph_result(result_raw)
            return result_raw
        else:
            return None
    else:
        result_raw = db.query(Graphs).all()
        if result_raw:
            result_raw = [formatting_graph_result(graphs)  for graphs in result_raw]
            return result_raw
        else: 
            return None

def formatting_route_graph(graph,db_graph_id):
    graph_data = graph.dict()
    for rota in graph_data['data']:
        rota['grafo_id'] = db_graph_id
        
    return [Graphs_routes(**rota) for rota in graph_data['data']]

def formatting_graph_result(result):
    
    [delattr(r, 'id') for r in result.data]
    for r in result.data:
        atributes = {}
        keys = ['source','target','distance']

        for atribute in keys:
            atributes[atribute] = getattr(r, atribute)
        
        [delattr(r, atribute) for atribute in keys]
        [setattr(r, atribute, atributes[atribute]) for atribute in keys]

    return result

def get_all_routes(db, graphId,town1,town2,maxStops):
    all_route = {"routes":[]}
    edges_raw = db.query(Graphs_routes).filter(Graphs_routes.grafo_id == graphId).all()
    edges = [(route.source,route.target,route.distance) for route in edges_raw]
    if len(edges) > 0 and town1 != town2 and contains_edges(edges,town1,town2):
        graph = nx.MultiDiGraph() # nx.Graph retorna Um grafo onde os sentidos são multilaterais
        graph.add_weighted_edges_from(edges)
        routes = list(nx.all_simple_paths(graph,source=town1,target=town2,cutoff = maxStops))
        [all_route["routes"].append({ "route": ''.join(map(str.upper, rota)),"stops": len(rota)-1}) for rota in routes]
    else : 
        return None
    return all_route

def minimum_distance(db,graphId,town1,town2):
    edges_raw = db.query(Graphs_routes).filter(Graphs_routes.grafo_id == graphId).all()
    edges = [(route.source,route.target,route.distance) for route in edges_raw]
    if len(edges) > 0 and town1 != town2 and contains_edges(edges,town1,town2):
        graph = nx.MultiDiGraph()
        graph.add_weighted_edges_from(edges)
        temp = graph.edges()
        path = nx.shortest_path(graph,source=town1,target=town2, weight='weight')
        distance = nx.shortest_path_length(graph,source=town1,target=town2, weight='weight')
        return {"distance":distance, "path" : path}
    return None

def contains_edges(edges,town1,town2):
    town1_edge = [True if edge[0] == town1 or edge[1] == town1 else False for edge in edges] 
    town2_edge = [True if edge[0] == town2 or edge[1] == town2 else False for edge in edges]
    if True in town1_edge and True in town2_edge:
        return True
    else:
        return False


