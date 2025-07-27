import util
class AvailabilityTable:

    def __init__(self, initialData):
        self.data = initialData
        self.preprocessData()

    def preprocessData(self):
        initialData = self.data
        self.data = {}

        for frame in initialData:
            date = frame['date']
            self.data.insert({date: frame['rooms'] if frame['rooms'] else []})

    def __getitem__(self, index):
        # index is a lesson dict. return all rooms available to this lesson
        lessonStart, lessonDuration = util.lessonToDateTime(index), util.durationToTimeDelta(index)
        availableRooms = []

        if lessonStart.date() not in self.data.keys():
            return []
        
        rooms = self.data[lessonStart.date()]
        for room, (start, duration) in rooms:
            if (start < lessonStart) and (start + duration > lessonStart + lessonDuration):
                availableRooms.append((room.split(' - ')))
        
        return availableRooms
