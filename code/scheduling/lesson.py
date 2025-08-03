from datetime import datetime, date, time, timedelta 
import util
class Lesson:

    def __init__(self, lesson: dict):
        # check here if the lesson object has all the fields it needs
        self.REQUIRED_FIELDS = ['teacherId', 'datetime', 'duration', 'status', 'location', 'studentId']
            
        self.teacherId = lesson['teacherId']
        self.start = datetime.fromisoformat(lesson['datetime'])
        self.duration = timedelta(minutes=60) if lesson['isFullHour'] else timedelta(minutes=30)
        self.end = self.start + self.duration
        self.status = lesson['status'] if lesson['status'] else util.status['pending']
        self.location = lesson['building'] + ' - ' + lesson['room']
        self.studentId = lesson['studentId'] if lesson['studentId'] else ''

    def __str__(self):
        # turns into a str for db insertion
        REQUIRED_FIELDS = ['teacherId', 'datetime', 'isFullHour', 'status', 'building', 'room', 'studentId']
        
        return str({
            'teacherId': self.teacherId,
            'datetime': datetime.isoformat(self.start),
            'isFullHour': True if self.duration > timedelta(minutes=30) else False,
            'status': self.status,
            'building': self.location.split(' - ')[0],
            'room': self.location.split(' - ')[1],
            'studentId': self.studentId
        })
    
    def __getitem__(self, index):
        if index not in self.REQUIRED_FIELDS:
            return None
        
        return self.index
        
    def hasDatetimeConflictWith(self, lesson):
        # returns t/f if this lesson conflicts with another
        thisDate, otherDate = self.start.date(), lesson.start.date()
        return (thisDate == otherDate) and (self.end > lesson.start or lesson.end > self.start)

    def hasDatetimeAndLocationConflictWith(self, lesson):
        # returns t/f if this lesson conflicts with another
        thisDate, otherDate = self.start.date(), lesson.start.date()
        thisLocation, otherLocation = self.location, lesson.location
        return ((thisLocation == otherLocation) and (thisDate == otherDate) and (self.end > lesson.start or lesson.end > self.start))
    
    def fitsInsideOf(self, availability):
        # returns t/f if this lesson fits inside this availability
        thisDate, otherDate = self.start.date(), availability.start.date()
        return (self.location == availability.location) and (thisDate == otherDate) and (availability.start() < self.start() and availability.end() > self.end())
    