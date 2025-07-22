from pymongo import MongoClient
from datetime import datetime, time
import os
db = None

def setClient():
    mongoClient = os.getenv('DB')
    global db
    db = mongoClient['scheduling']

def lessonToDateTime(lesson):

    # assume a formatting function is applied to the lesson variable
    # when the object passes the validation function (happens prior in execution)
    lessonDate = lesson['date'].split('/')
    lessonTime = lesson['time'].split(':')
    
    if len(lessonDate) != 3 or len(lessonTime) != 2:
        raise Exception("Lesson date/time arguments are not initialized")
    
    return datetime(lessonDate[2], lessonDate[0], lessonDate[1], lessonTime[0], lessonTime[1], 0)

def lessonsConflict(lessonA, lessonB):

    # uses datetime objects to intuitively compare events 
    datetimeA, datetimeB = lessonToDateTime(lessonA), lessonToDateTime(lessonB)
    durationA = time(minute=60) if lessonA['isFullHour'] else time(minute=30)
    durationB = time(minute=60) if lessonB['isFullHour'] else time(minute=30)
                                                                                    
                                                                                    # ensures A doesn't bleed into B's start
    return datetimeA + durationA > datetimeB or datetimeB + durationB > datetimeA   # and that B doesn't bleed into A's start
    

"""
Each request that comes in can be processed sequentially: validate, then observe if there are any date-time conflicts
Then I need to check for any date-time conflicts with each room. If one exists, insert into db with status "conflicted": else status is "secured"
"""

def processNewLesson(newLesson):

    global db
    if db is None: # connects to the database
        setClient()
    
    existingLessons = db['lessons'].find()
    doesConflict = False
    for lesson in existingLessons:  # checks every existing lesson for a time conflict
        if lessonsConflict(newLesson, lesson):
            doesConflict = True
            break
    
    lesson['status'] = 'conflicted' if doesConflict else 'secured'  # sets status based on flag
    id = db['lessons'].insert_one(lesson).inserted_id

    return id is not None   # returns True / False based on if the id exists (if exists implies operation succeeded)