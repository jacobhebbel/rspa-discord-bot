import heapq
from datetime import timedelta

class RoomBalancer:

    def __init__(self, roomCapacities):
        self.heap = [Room(room, capacity) for room, capacity in roomCapacities.items()]
        heapq.heapify(self.heap)
        
    def isEmpty(self):
        return self.heap == []
    
    def topItem(self):
        return self.heap[0].roomName, self.heap[0].remainingCapacity
    
    def pop(self):
        del self.heap[0]
    
    def decrementKey(self, room, duration: timedelta):

        for item in self.heap:
            roomName = item.roomName
            if roomName == room:
                item.remainingCapacity -= duration
                break

    def add(self, room, capacity):
        heapq.heappush(Room(room, capacity))

    
class Room:

    def __init__(self, roomName, remainingCapacity: timedelta):
        self.roomName = roomName
        self.remainingCapacity = remainingCapacity
    
    def __lt__(self, other: timedelta):
        return self.remainingCapacity > other.remainingCapacity
    