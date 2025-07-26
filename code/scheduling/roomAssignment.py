import util

def updateLessonFields(lesson, doesConflict):
    lesson['status'] = util.status['conflicted'] if doesConflict else util.status['secured']  # sets status based on flag

def checkForConflict(newLesson, existingLessons):
    for lesson in existingLessons:  # checks every existing lesson for a time conflict
        if util.lessonsConflict(newLesson, lesson):
            return True
        
    return False

"""
Each request that comes in can be processed sequentially: validate, then observe if there are any date-time conflicts
Then I need to check for any date-time conflicts with each room. If one exists, insert into db with status "conflicted": else status is "secured"
"""
def processIncomingLesson(newLesson):

    db = util.getDatabaseConnection(collection='lessons')
    existingLessons = util.getLessons(filter={'status': util.status['secured']})
    doesConflict = checkForConflict(newLesson, existingLessons)
    
    newLesson['status'] = util.status['conflicted'] if doesConflict else util.status['secured']  # sets status based on flag
    id = db['lessons'].insert_one(newLesson).inserted_id

    return id is not None   # returns True / False based on if the id exists (if exists implies operation succeeded)



"""
Validates a lesson that it has certain fields initialized. Re-formats from a human-friendly format to a machine-friendly one
"""
def validateLesson(lesson):

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
    
    validateDate(lesson, missingFields)
    validateTime(lesson, missingFields)

    if missingFields != []:
        result['validated'] = False
        result['missingFields'] = missingFields

    formatLesson(lesson)
    return result

def validateDate(lesson, missingFields):
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

def validateTime(lesson, missingFields):
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

"""set lesson fields and update date/time fields"""
def formatLesson(lesson):
    
    # fields that need to be added
    lesson.update({'teacherId': util.getTeacherFromDiscord(lesson['discord'])})
    lesson.update({'status': util.status['pending']})
    lesson.update({'studentId': 0})
