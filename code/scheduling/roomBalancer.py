import heapq
from datetime import timedelta

class RoomBalancer:

    def __init__(self, roomToTimeBooked):
        self.heap = [(timeBooked.seconds, room) for room, timeBooked in roomToTimeBooked.items()]
        heapq.heapify(self.heap)
        
    def isEmpty(self):
        return self.heap == []
    
    def topItem(self):
        priority, room = self.heap[0][:]
        return room, timedelta(seconds=priority)
    
    def popItem(self):
        heapq.heappop(self.heap)
    
    def incrementKey(self, room, timeBooked: timedelta):
        
        temp = []
        priority, item = None, None
        
        while self.isEmpty() is False and item != room:
            priority, item = heapq.heappop(self.heap)
            
            if room == item:
                priority += timeBooked.seconds
            temp.append((priority, item))
            
        for item in temp:
            heapq.heappush(self.heap, item)
    
    def addItem(self, room, timeBooked: timedelta):
        heapq.heappush(self.heap, (timeBooked.seconds, room))
    