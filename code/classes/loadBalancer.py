import heapq



class LoadBalancer:

    def __init__(self, rooms):
        self.heap = heapq.heapify([room for room in rooms])
    
    def isEmpty(self):
        return len(self.heap) == 0
    
    def peek(self):
        return self.heap[0] 
    
    def pop(self):
        del self.heap[0]
    
    def insert(self, item, priority):
        heapq.heappush(self.heap, Room(item, priority))

    def pushPop(self, item, priority):
        heapq
    
class Room:

    def __init__(self, roomName, remainingCapacity):
        self.roomName = roomName
        self.remainingCapacity = remainingCapacity
    
    def __lt__(self, other):
        return self.remainingCapacity > other.remainingCapacity
    