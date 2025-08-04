from datetime import datetime, timedelta

class Availability:

    def __init__(self, args: dict):

        self.INVARIANT_FIELDS = ['start', 'end', 'duration', 'location']
        for field, value in args.items():
            setattr(self, field, value)

        self.start = datetime.fromisoformat(self.start)
        self.duration = timedelta(seconds=int(self.duration))
        self.end = self.start + self.duration


    def __getitem__(self, index):
        if index not in self.INVARIANT_FIELDS:
            return None
        return getattr(self, index)

    def __setitem__(self, index, value):
        if index not in self.INVARIANT_FIELDS:
            raise Exception
        setattr(self, index, value)
    
    def canFit(self, lesson):
        # returns t/f if it can fit a lesson
        return (self.start <= lesson.start) and (self.end >= lesson.end)

    def splitOnLesson(self, lesson):
        # fits the lesson into the availability
        # returns a new Availability object if needed

        if not self.canFit(lesson):
            raise Exception

        timeBefore = lesson.start - self.start
        timeAfter = self.end - lesson.end

        if timeBefore and timeAfter:
            self.duration, self.end = timeBefore, lesson.start

            return self, Availability({
                'start': lesson.end.isoformat(),
                'duration': timeAfter.seconds,
                'location': self.location
            })
        
        elif timeBefore:
            self.end, self.duration = lesson.start, timeBefore
            return self
        
        else:
            self.start, self.duration = lesson.end, timeAfter
            return self
    
