import time
from icecream import ic
from python_redis.constants import SyncTime
from python_redis.persistence.db import *
from python_redis.models.graph_config import Vertex, Edge
import threading
# TODO: create persistence for graph
# ? figure out how to store in db
# ! important 


# (there will be a collection of vertices and a collection of edges, and value of is_directed, graphkey and is_weighted will be stored in meta collection)
class VerticesStore:
    # this store will keep track of the edges 
    def __init__(self, db: HardDatabase):
        
        self.db: HardDatabase = db
        self.lock: threading.RLock = threading.RLock()
        self.stop_event : threading.Event= threading.Event()
        self.dirty_edges: set[tuple[str, dict, str]] = set() # [start_key, end_key, weight, operation]
        self.storage: dict[str, dict] = dict()
        self.collection: Collection
        if self.db.check_collection_exist("Edge"):
            self.collection = self.db.new_collection("Edge")
            self.load_from_hard_db()
        
        else:
            self.collection= self.db.new_collection("Edge")

        edge_thread = threading.Thread(target= self.periodic_db_sync, args= (), daemon=True)
        edge_thread.start()

    def load_from_hard_db(self):
        for record in self.db.load_from_db(self.collection):
            pass
    
    def create_key(self,start: str, end: str):
        return f"{start}->{end}"
    
    
    def add_edge(self, start_vertex_key: Vertex.Vertex, end_vertex_key: Vertex.Vertex, weight: int):
        temp_dict = dict({
            "start_vertex": start_vertex_key.data,
            "end_vertex": end_vertex_key.data,  
            "weight": weight
        })
        with self.lock:
            self.dirty_edges.add((self.create_key(start_vertex_key.data, end_vertex_key.data),str( temp_dict), "c"))
    
    def remove_edge(self, start_vertex: Vertex.Vertex, end_vertex: Vertex.Vertex,weight: int):
        temp_dict = dict({
            "start_vertex": start_vertex.data,
            "end_vertex": end_vertex.data,  
            "weight": weight
        })
        with self.lock:
            self.dirty_edges.add((self.create_key(start_vertex.data, end_vertex.data),str( temp_dict), "d"))

    def periodic_db_sync(self):
        # * here now we have composite key and data dict can be stored in value
        while not self.stop_event.is_set(): 
            dirty_edge_snapshots:set
            with self.lock:
                dirty_edge_snapshots:set = set(self.dirty_edges)
                ic(dirty_edge_snapshots)
            if len(dirty_edge_snapshots) != 0:
                synced_items = set()
                
                for key,  item, operation in dirty_edge_snapshots:
                    
                    try:
                        if operation == "d":
                            ic(self.db.delete_key(key, self.collection))
                            synced_items.add((key , item, operation))
                            
                        else:
                            self.db.insert_and_update_key_val(key, item, self.collection)
                            synced_items.add((key, item , operation))
                    except Exception as e:
                        ic(e)
                with self.lock:
                    self.dirty_edges -=  synced_items
                del dirty_edge_snapshots
            time.sleep(SyncTime)


class GraphStore:
    def __init__(self, db:HardDatabase):
        ic.configureOutput(prefix="DEBUG: ", includeContext=True)
        self.vertices_store: VerticesStore =  VerticesStore(db)
        self.lock = threading.RLock()
        self.stop_event: threading.Event = threading.Event()

        self.db: HardDatabase = db
        self.dirty_vertices: set[tuple[str,str, str]] = set()# [key, value, operation]
        self.meta_collection: Collection = db.new_collection("meta")
        
        if self.db.check_collection_exist("GRAPH"): 
            self.collection = self.db.new_collection("GRAPH")
            
        else: 
            self.collection: Collection = self.db.new_collection("GRAPH")
        
        
        t = threading.Thread(target=self.periodic_db_sync, args=(), daemon=True)
        t.start()
    #TODO: in it at first vertices will be loaded from DB and then edges will be loaded.
    def get_key_name(self):
        obj= self.db.get_data_from_meta("GraphKeyName", self.meta_collection)
        if obj!= None:
            return obj["value"]
        else:
            return obj
    def update_key_name(self, key_name: str):
        self.db.insert_and_update_key_val("GraphKeyName", key_name, self.meta_collection)
    
    def update_is_directed(self, is_directed: bool):
        self.db.insert_and_update_key_val("GraphIsDirected", is_directed, self.meta_collection)
    
    def update_is_weighted(self, is_weighted: bool):
        self.db.insert_and_update_key_val("GraphIsWeighted", is_weighted, self.meta_collection)
    
    def add_edge(self,start: Vertex.Vertex, end: Vertex.Vertex, weight: int ):
        self.vertices_store.add_edge(start, end, weight)
        
    def remove_edge(self, start :Vertex.Vertex, end:Vertex.Vertex):
        self.vertices_store.remove_edge(start, end, 90)
    
    def add_vertex(self,vertex: Vertex.Vertex, key :str):
        with self.lock:
            self.dirty_vertices.add((  vertex.data.get(key),str(vertex.data) ,"c"))
    def remove_vertex(self,vertex: Vertex.Vertex, key :str):
        with self.lock:
            self.dirty_vertices.add((  vertex.data.get(key),str(vertex.data) ,"d"))
    
    def periodic_db_sync(self):

        while not self.stop_event.is_set():
            with self.lock:
                dirty_vertices_snapshots = set(self.dirty_vertices)
            if len(dirty_vertices_snapshots) != 0:
                synced_items = set()
                for key, data, operation in dirty_vertices_snapshots:
                    try:
                        if operation == "d":
                            ic(self.db.delete_key(key, self.collection))
                            synced_items.add((key, operation))
                            print(operation)
                        else:
                            self.db.insert_and_update_key_val(key, data, self.collection)
                            synced_items.add((key, data , operation))
                    except Exception as e:
                        ic(e)
                with self.lock:
                    self.dirty_vertices = self.dirty_vertices - synced_items
            time.sleep(SyncTime)