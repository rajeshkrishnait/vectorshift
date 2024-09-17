from fastapi import FastAPI
from typing import List, Dict
from networkx import DiGraph, is_directed_acyclic_graph
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

class Node(BaseModel):
    id: str
    type: str
    position: Dict[str, float]
    data: Dict[str, Any]  # Adjust types if needed

class Edge(BaseModel):
    source: str
    target: str
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to a list of allowed origins for production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)
@app.post("/pipelines/parse")
async def parse_pipeline(nodes: List[Node], edges: List[Edge]):
    num_nodes = len(nodes)
    num_edges = len(edges)
    
    # Create a directed graph
    graph = DiGraph()
    
    # Add nodes and edges to the graph
    for node in nodes:
        graph.add_node(node.id)
    for edge in edges:
        graph.add_edge(edge.source, edge.target)
    
    # Check if the graph is a DAG
    is_dag = is_directed_acyclic_graph(graph)
    
    return {"num_nodes": num_nodes, "num_edges": num_edges, "is_dag": is_dag}
