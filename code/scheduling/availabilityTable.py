import util
from datetime import datetime, date, time, timedelta
class AvailabilityTable:

    def __init__(self, initialData):
        self.data = initialData
        self.preprocessData()

    def preprocessData(self):

        def parseDate(strDate):
            arrDate = strDate.split('/')
            return date(month=int(strDate[0]), day=int(strDate[1]), year=int(strDate[2]))
        
        def parseSlot(slot, docDate):
            strStart, strDuration = slot['start'], slot['duration']
            arrStart = strStart.split(':')
            return datetime.combine(date=docDate, time=time(hour=int(arrStart[0]), minute=int(arrStart[1]))), timedelta(minutes=int(strDuration))
        

        dataFromMongo = self.data
        self.data = {}

        '''
        Initial data is a series of mongo docs with date, time, and room
        '''

        # each doc is unique to a single date
        for document in dataFromMongo:
            docDate = parseDate(document['date'])
            self.data.insert({docDate: []})

            rooms = document['rooms']
            for room, availability in rooms.items():
                self.data[docDate].insert({room: []})

                # now looping thru each room's openings
                for slot in availability:    
                    slotDatetime, slotTimeDelta = parseSlot(slot)
                    self.data[room].append((slotDatetime, slotTimeDelta))


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
