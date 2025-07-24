import datetime
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
        # index value is a tuple with a start time and duration
        if not isinstance(index, datetime):
            raise TypeError('Availability Table\'s first index must be a datetime object')
        
        return AvailabilityQuery(self.data, index)

        # represents the rooms available on this day
        
        
class AvailabilityQuery:

    def __init__(self, data, index):
        self.data = data
        self.datetime = index
    
    def __getitem__(self, index):
        
        if not isinstance(index, datetime.time):
            raise TypeError('Availability Table\'s second index must be a time object')

        lessonDate, lessonStart = self.datetime.date(), self.datetime.time()
        lessonDuration = index

        availableRooms = []
        for room, availabilities in self.data[lessonDate]:
            for openingStart, openingDuration in availabilities:

                if openingStart < (lessonStart + lessonDuration) < (openingStart + openingDuration):
                    availableRooms.append(room)
                    break

        return availableRooms
        


