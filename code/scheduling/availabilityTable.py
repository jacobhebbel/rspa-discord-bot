import util
from datetime import datetime, date, time, timedelta
class AvailabilityTable:

    def __init__(self, initialData):
        self.data = initialData
        self.preprocessData()

    def __str__(self):
        return str(self.data)

    def preprocessData(self):

        def parseDate(strDate):
            arrDate = strDate.split('/')
            return date(month=int(arrDate[0]), day=int(arrDate[1]), year=int(arrDate[2]))
        
        def parseSlot(slot, docDate):
            strStart, strDuration = slot['start'], slot['duration']
            arrStart = strStart.split(':')
            return datetime.combine(date=docDate, time=time(hour=int(arrStart[0]), minute=int(arrStart[1]))), timedelta(minutes=int(strDuration))
        

        dataFromMongo = self.data
        self.data = {}

        # each doc is unique to a single date
        for strDate in dataFromMongo.keys():
            docDate = parseDate(strDate)
            self.data.update({docDate: {}})

            rooms = dataFromMongo[strDate]
            for room, availability in rooms.items():
                self.data[docDate].update({room: []})

                # now looping thru each room's openings
                for slot in availability:    
                    slotDatetime, slotTimedelta = parseSlot(slot, docDate)
                    self.data[docDate][room].append({'start': slotDatetime, 'duration': slotTimedelta})


    def __getitem__(self, index):

        if isinstance(index, dict) and all(key in index.keys() for key in ['date', 'time', 'isFullHour']):
            return self.getAvailabilityByLesson(index)
        elif isinstance(index, date):
            return self.getAvailabilityByDatetime(index)
        else:    
            raise TypeError('index argument to Availability Table must be a lesson dictionary')

    def blockAvailability(self, lesson, room):
        
        if not (isinstance(lesson, dict) and all(key in lesson.keys() for key in ['date', 'time', 'isFullHour'])):
            raise TypeError('1st argument (lesson) must be a lesson dictionary')
        
        if self[lesson] == [] or room not in self[lesson]:
            raise KeyError('2nd Arg is not a valid room option to book for this lesson')

        lessonStart, lessonDuration = util.lessonToDatetime(lesson), util.lessonToTimedelta(lesson)
        roomSchedule = self.data[util.lessonToDatetime(lesson).date()][room]
        for availability in roomSchedule:
            start, duration = availability['start'], availability['duration']
            if (start <= lessonStart) and (start + duration >= lessonStart + lessonDuration):

                timeBefore = lessonStart - start
                timeAfter = (start + duration) - (lessonStart + lessonDuration)

                # updates the entry to end as the new event starts
                if timeBefore > timedelta(0):
                    availability['duration'] = timeBefore
                else:
                    roomSchedule.remove(availability)

                # if time remains in the availability, add a new entry representing the elapsed time
                if timeAfter > timedelta(0):
                    roomSchedule.append({'start': lessonStart + lessonDuration, 'duration': timeAfter})
                else:
                    continue
                
                break


    
    def getAvailabilityByLesson(self, index):
        # index is a lesson dict. return all rooms available to this lesson

        lessonStart, lessonDuration = util.lessonToDatetime(index), util.lessonToTimedelta(index)
        availableRooms = []
        if lessonStart.date() not in self.data.keys():
            print('lessonStart not in keys')
            return []
        
        rooms = self.data[lessonStart.date()]
        for room, schedule in rooms.items():
            for availability in schedule:

                start, duration = availability['start'], availability['duration']
                if (start <= lessonStart) and (start + duration >= lessonStart + lessonDuration):
                    availableRooms.append(room)
        
        return availableRooms
    
    def getAvailabilityByDatetime(self, index):

        rooms = self.data[index]
        return rooms