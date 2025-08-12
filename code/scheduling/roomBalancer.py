import heapq
from datetime import timedelta

class RoomBalancer:

    def __init__(self, roomToHoursBooked):
        self.heap = [(hoursBooked, room) for room, hoursBooked in roomToHoursBooked.items()]
        heapq.heapify(self.heap)
        
    def isEmpty(self):
        return self.heap == []
    
    def topItem(self):
        return self.heap[0]
    
    def popItem(self):
        del self.heap[0]
    
    def incrementKey(self, room, duration: timedelta):

        for item in self.heap:
            hoursBooked, roomName = item

            if roomName == room:
                hoursBooked += duration.seconds
                break
    
    def addItem(self, room, hoursBooked):
        heapq.heappush((hoursBooked, room))
    