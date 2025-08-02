import util

class RoomValidator:

    def __init__(self):
        pass

    """
    Validates a lesson that it has certain fields initialized. Re-formats from a human-friendly format to a machine-friendly one
    """
    def validateLesson(self, lesson):

        result = {'validated': True, 'missingFields': []}

        requiredFields = ['discord', 'date', 'time', 'isMonthly', 'isFullHour', 'building', 'room']
        lessonFields = lesson.keys()

        missingFields = []
        for field in requiredFields:
            if field not in lessonFields:
                missingFields.append(field)

        if missingFields != []:
            result['validated'] = False
            result['missingFields'] = missingFields
            return result
        
        self.validateDate(lesson, missingFields)
        self.validateTime(lesson, missingFields)

        if missingFields != []:
            result['validated'] = False
            result['missingFields'] = missingFields

        self.formatLesson(lesson)
        return result

    def validateDate(self, lesson, missingFields):
        date = lesson['date']
        date = date.split('/')
        if len(date) != 3:
            missingFields.append('date')
            return
        
        if len(date[0]) != 2 or int(date[0]) > 12 or int(date[0]) < 1:
            missingFields.append('date')
        
        if len(date[1]) != 2 or int(date[1]) > 31 or int(date[1]) < 1:
            missingFields.append('date')
        
        if len(date[2]) != 4 or int(date[2]) < 2025:
            missingFields.append('date')

        return

    def validateTime(self, lesson, missingFields):
        time = lesson['time']
        time = time.split(':')
        if len(time) != 2:
            missingFields.append('time')
            return
        
        if len(time[0]) != 2 or int(time[0]) > 24 or int(time[0]) < 0:
            missingFields.append('time')
        
        if len(time[1]) != 2 or int(time[1]) > 59 or int(time[1]) < 0:
            missingFields.append('time')
        
        return

    def formatLesson(self, lesson):
        
        # fields that need to be added
        lesson.update({'teacherId': util.getTeacherFromDiscord(lesson['discord'])})
        lesson.update({'status': util.status['pending']})
        lesson.update({'studentId': 0})
