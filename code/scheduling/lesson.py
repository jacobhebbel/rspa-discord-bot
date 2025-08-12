from datetime import datetime, date, time, timedelta 
class Lesson:

    def __init__(self, args: dict):
        self.INVARIANT_FIELDS = ['id', 'teacherId', 'studentId', 'packageId', 'start', 'end', 'duration', 'location', 'status']
        
        '''
        assume a Lesson is only initialized from a database record.
        this record will have all fields either initialized or default valued, 
        so just go through the dict and assign everything

        However, there are some fields which could be condensed. the question is how to elegantly optimize this process
        '''
        
        # these fields change from the database record
        self.location, self.start, self.end = [], None, None

        for field, value in args.items():
            
            if field == 'building' or field == 'room':
                self.location.append(value)
            
            elif field == 'start':
                self.start = datetime.fromisoformat(value)
            
            elif field == 'duration':
                self.duration = timedelta(seconds=int(value))
            
            else:
                setattr(self, field, value)

        self.location = (' - ').join(self.location)
        self.end = self.start + self.duration

    def toDatabase(self):
        # turns into a str for db insertion
        DB_FIELDS = ['id', 'teacherId', 'studentId', 'hasStudent', 'datetime', 'duration', 'building', 'room', 'hasRoom', 'status', 'isPackage', 'packageId']
        
        return {
            'id': self.id,
            'teacherId': self.teacherId,
            'datetime': datetime.isoformat(self.start),
            'duration': self.duration.seconds,
            'status': self.status,
            'building': self.location.split(' - ')[0],
            'room': self.location.split(' - ')[1],
            'hasRoom': True if self.location != '' else False,
            'studentId': self.studentId,
            'hasStudent': True if self.studentId != '' else False,
            'isPackage': True if self.packageId != '' else False,
            'packageId': self.packageId,
        }
    
    def __getitem__(self, index):
        if index not in self.INVARIANT_FIELDS:
            return None
        
        return getattr(self, index)
    
    def __setitem__(self, index, value):
        if index not in self.INVARIANT_FIELDS:
            raise Exception
        setattr(self, index, value)
    
    def datetimeConflict(self, other):
        # returns t/f if this lesson conflicts with another
        thisDate, otherDate = self.start.date(), other.start.date()
        return (thisDate == otherDate) and ((self.start <= other.start and self.end >= other.start) or (other.start <= self.start and other.end >= self.start))

    def roomConflict(self, lesson):
        # returns t/f if this lesson conflicts with another
        return self.location == lesson.location
    
    def fitsInside(self, availability):
        # returns t/f if this lesson fits inside this availability
        thisDate, otherDate = self.start.date(), availability.start.date()
        return (thisDate == otherDate) and (availability.start <= self.start and availability.end >= self.end)
    