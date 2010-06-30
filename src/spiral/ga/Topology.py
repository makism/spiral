"""
    
"""


import random



class Topology (object):
    """
    
    """
    
    def __init__ (self, Islands, Name):
        # All islands
        self._Islands = Islands
        
        # Total islands
        self._total = len (self._Islands)
        
        # Keep track of each Island`s neighbours
        self._Neighbours = dict ()
        
        # Topology name
        self._topologyName = Name
        
    def __str__ (self):
        return "%s, with %d nodes" % (self._topologyName, self._total)
        
    def getNeighbours (self, IslandId):
        if IslandId in self._Neighbours.keys ():
            return self._Neighbours[IslandId]
        else:
            return None
    

class Ring (Topology):
    """
    
    """
    
    def __init__ (self, Islands, Bidirectional=False):
        Topology.__init__ (self, Islands, "Ring Topology")
        
        self.Bidirectional = Bidirectional      
        
        for i in range (0, self._total):
            curr = self._Islands[i]
            next = None
            prev = None
            id   = curr.cId
            self._Neighbours[id] = list ()
            
            if self.Bidirectional:
                if i==0:
                    prev = self._Islands [self._total-1]
                else:
                    prev = self._Islands [i-1]
                
                self._Neighbours[id].append (prev)
            
            if i == self._total - 1:
                next = self._Islands [0]
            else:
                next = self._Islands [i+1]
            
            self._Neighbours[id].append (next)
    

class Line (Topology):
    """
    
    """
    
    def __init__ (self, Islands, Bidirectional=False):
        Topology.__init__ (self, Islands, "Line Topology")
        
        self.Bidirectional = Bidirectional
        
        for i in range (0, self._total):
            curr = self._Islands[i]
            next = None
            prev = None
            id   = curr.cId
            self._Neighbours[id] = list ()
            
            if self.Bidirectional:
                if i > 0:
                    prev = self._Islands [i-1]
                    self._Neighbours[id].append (prev)
            
            if i < self._total-1:
                next = self._Islands[i+1]
                self._Neighbours[id].append (next)
    

class Grid (Topology):
    """
    
    """
    
    def __init__ (self, Islands, Rows, Cols, CalculateNeighbours=True):
        Topology.__init__ (self, Islands, "Grid (%dx%d) Topology" % (Rows, Cols))
        
        if Rows * Cols < len (Islands):
            raise Exception, "The grid is too small"
        
        self._Rows = Rows
        self._Cols = Cols
        self._Map  = list ()
        
        # Create the map - "neighberhood" ;)
        idx = 0
        for r in range (0, self._Rows):
            self._Map.append (list ())
            
            for c in range (0, self._Cols):
                try:
                    self._Map[r].append (self._Islands[idx].cId)
                except:
                    self._Map[r].append (None)
                
                idx += 1        
        
        if CalculateNeighbours:
            # Calculate the neighbours
            for r in range (0, self._Rows):
                for c in range (0, self._Cols):
                    current_id = self._Map[r][c]
                    
                    if current_id is not None:
                        neighbours = list ()
                        
                        self._Neighbours[current_id] = list ()
                        
                        
                        id = None
                        try:
                            if c+1 < self._Cols:
                                id = self._Map[r][c+1]
                                neighbours.append (self._Islands[id])
                        except:
                            pass
                        
                        id = None
                        try:
                            if c-1 >= 0:
                                id = self._Map[r][c-1]
                                neighbours.append (self._Islands[id])
                        except:
                            pass
                        
                        id = None
                        try:
                            if r+1 < self._Rows:
                                id = self._Map[r+1][c]
                                neighbours.append (self._Islands[id])
                        except:
                            pass
                        
                        id = None
                        try:
                            if r-1 >= 0 :
                                id = self._Map[r-1][c]
                                neighbours.append (self._Islands[id])
                        except:
                            pass
                        
                        self._Neighbours[current_id].extend(neighbours)
   
                
class Grid3D (Grid):
    """
    
    """
    
    def __init__ (self, Islands, Rows, Cols):
        Grid.__init__ (self, Islands, Rows, Cols, False)
        
        self._topologyName = "Three Dimensional Grid Topology"
        
        if Rows * Cols != len(Islands) or Rows != Cols:
            raise Exception, "Cannot create 3D Grid"    
        
        # Calculate the neighbours
        for r in range (0, self._Rows):
            for c in range (0, self._Cols):
                current_id = self._Map[r][c]
                
                if current_id is not None:
                    neighbours = list ()
                    
                    self._Neighbours[current_id] = list ()
                    
                    id = None
                    try:
                        if c+1 < self._Cols:
                            id = self._Map[r][c+1]
                        else:
                            id = self._Map[r][0]
                        neighbours.append (self._Islands[id])
                    except:
                        pass
                    
                    id = None
                    try:
                        if c-1 >= 0:
                            id = self._Map[r][c-1]
                        else:
                            id = self._Map[r][self._Cols-1]
                        neighbours.append (self._Islands[id])
                    except:
                        pass
                    
                    id = None
                    try:
                        if r+1 < self._Rows:
                            id = self._Map[r+1][c]
                        else:
                            id = self._Map[0][c]
                        neighbours.append (self._Islands[id])
                    except:
                        pass
                    
                    id = None
                    try:
                        if r-1 >= 0 :
                            id = self._Map[r-1][c]
                        else:
                            id = self._Map[self._Rows-1][c]
                        neighbours.append (self._Islands[id])
                    except:
                        pass
                    
                    self._Neighbours[current_id].extend(neighbours)
    

class FullMesh (Topology):
    """
    
    """
    
    def __init__ (self, Islands):
        Topology.__init__ (self, Islands, "Full Mesh Topology")
        
        for i in range (0, self._total):
            current_id = self._Islands[i].cId
            self._Neighbours[current_id] = list ()
            
            for x in range (0, self._total):
                id = self._Islands[x].cId
                
                if id != current_id:
                    self._Neighbours[current_id].append (self._Islands[x])
            

class PartiallyFullMesh (Topology):
    """
    
    """
    
    def __init__ (self, Islands, Rows, Cols, MaxWidth=2):
        Topology.__init__ (self, Islands, "Partially Full Mesh Topology")
    

class RandomMesh (Topology):
    """
    
    """
    
    def __init__ (self, Islands, MaxLinks=2):
        Topology.__init__ (self, Islands, "Random Mesh Topology")
        
        if MaxLinks > self._total:
            raise Exception, "Cannot create so many links"
               
        self._maxLinks = MaxLinks
        
        for i in range (0, self._total):
            current_id = self._Islands [i].cId
            self._Neighbours [current_id] = list ()    
            
            member = self._Islands [random.randint (0, self._total-1)]
            for x in range (0, self._maxLinks):
                while member in self._Neighbours [current_id] or \
                      member.cId == current_id:
                    member = self._Islands [random.randint (0, self._total-1)]
                
                self._Neighbours [current_id].append (member)
    
