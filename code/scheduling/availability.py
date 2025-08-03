class Availability:

    def __init__(self, availability: dict):
        self.REQUIRED_FIELDS = ['start', 'end', 'duration', 'location']
        self.start = availability['start']
        self.end = availability['end']
        self.duration = availability['duration']
        self.location = availability['location']
        # has a location, start, end, and duration parameter
        raise NotImplementedError

    def __getitem__(self, index):
        if index not in self.REQUIRED_FIELDS:
            return None
        return self.index
    
    def canFit(self, lesson):
        # returns t/f if it can fit a lesson
        return (self.start < lesson.start) and (self.end > lesson.end)

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
                'start': lesson.end,
                'end': self.end,
                'duration': timeAfter,
                'location': self.location
                })
        
        elif timeBefore:
            self.end, self.duration = lesson.start, timeBefore
            return self
        
        else:
            self.start, self.duration = lesson.end, timeAfter
            return self
    
