from datetime import datetime, date
from scheduling.availability import Availability
from scheduling.lesson import Lesson

class AvailabilityTable:

    def __init__(self, initialData):
        self.roomData = {}
        self.preprocessData(initialData)

    def __str__(self):
        return str(self.data)

    def preprocessData(self, data):
        documentsFromMongo = data
        
        # each doc is unique to a single date
        for doc in documentsFromMongo:

            docDate = datetime.fromisoformat(doc['date']).date()
            rooms = list(doc['rooms'])
            self.roomData.update({docDate: {}})

            for room in rooms:
                roomSchedule = doc['schedules'][room]
                self.roomData[docDate].update({room: []})

                for availability in roomSchedule:
                    self.roomData[docDate][room].append(Availability({
                        'location': room,
                        'start': availability['start'],
                        'duration': availability['duration']
                    }))

    def __getitem__(self, index):

        if isinstance(index, Lesson):
            return self.getAvailabilityByLesson(index)
        elif isinstance(index, date):
            return self.getAvailabilityByDate(index)
        else:    
            raise TypeError('index argument to Availability Table must be a lesson object')

    def blockAvailability(self, lesson, room):

        if not isinstance(lesson, Lesson):
            raise TypeError('1st argument (lesson) must be a lesson object')
        
        if self[lesson] == [] or room not in self[lesson]:
            raise KeyError('2nd Arg is not a valid room option to book for this lesson')


        roomSchedule = self.roomData[lesson['start'].date()][room]
        for availability in roomSchedule:
            
            if availability.canFit(lesson):
                result = availability.splitOnLesson(lesson)

                if isinstance(result, tuple):
                    a, b = result
                    roomSchedule.append(a)
                    roomSchedule.append(b)
                else:
                    roomSchedule.append(result)
                break
            
    def getAvailabilityByLesson(self, lesson):
        # index is a lesson dict. return all rooms available to this lesson

        availableRooms = []
        for room, schedule in self.roomData[lesson['start'].date()].items():
            for availability in schedule:

                if availability.canFit(lesson):
                    availableRooms.append(room)
        
        return availableRooms
    
    def getAvailabilityByDate(self, index):
        rooms = self.roomData[index].keys()
        return rooms
    


