class Graph:
  class Vertex:

    def __init__(self, x):
      self._element = x
  
    def element(self):
      return self._element
  
    def __str__(self):
      return str(self._element)
    
  class Edge:

    def __init__(self, origin, destination):
      self._origin = origin
      self._destination = destination
  
    def endpoints(self):
      return (self._origin, self._destination)
  
    def opposite(self, v):
      if not isinstance(v, Graph.Vertex):
        raise TypeError('v mora biti instanca klase Vertex')
      if self._destination == v:
        return self._origin
      elif self._origin == v:
        return self._destination
      raise ValueError('v nije čvor ivice')
  
    def element(self):
      return self._element
  
    def __str__(self):
      return '({0},{1})'.format(self._origin,self._destination)
    
  def __init__(self):
    self._outgoing = {}
    self._incoming = {} 

  def _validate_vertex(self, v):
    if not isinstance(v, self.Vertex):
      raise TypeError('Očekivan je objekat klase Vertex')
    if v not in self._outgoing:
      raise ValueError('Vertex ne pripada ovom grafu.')

  def vertex_count(self):
    return len(self._outgoing)

  def vertices(self):
    return self._outgoing.keys()

  def edge_count(self):
    total = sum(len(self._outgoing[v]) for v in self._outgoing)
    return total 

  def edges(self):
    result = set()       
    for secondary_map in self._outgoing.values():
      result.update(secondary_map.values())   
    return result

  def get_vertex(self, x):
    all_vertex = self._outgoing.keys()
    for vertex in all_vertex:
      if vertex._element == x:
        return vertex
    return None
  
  def get_edge(self, u, v):
    self._validate_vertex(u)
    self._validate_vertex(v)
    return self._outgoing[u].get(v)

  def degree(self, v, outgoing=True):   
    self._validate_vertex(v)
    adj = self._outgoing if outgoing else self._incoming
    return len(adj[v])
  
  def incoming_vertexes(self, v):
    edges = self._incoming[v]
    return edges.keys()
    
  def incident_edges(self, v, outgoing=True):   
    self._validate_vertex(v)
    adj = self._outgoing if outgoing else self._incoming
    for edge in adj[v].values():
      yield edge

  def insert_vertex(self, x=None):
    v = self.Vertex(x)
    self._outgoing[v] = {}
    self._incoming[v] = {}      
    return v
      
  def insert_edge(self, u, v):
    if self.get_edge(u, v) is not None:     
      raise ValueError('u and v are already adjacent')
    e = self.Edge(u, v)
    self._outgoing[u][v] = e
    self._incoming[v][u] = e



