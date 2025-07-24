from pymongo import MongoClient
from datetime import datetime, time
from classes.availabilityTable import AvailabilityTable
import os

db = None
status = {
    'pending': 0,
    'conflicted': 1,
    'secured': 2,
    'incompatible': 3,
    'booked': 4,
    'past': 5,
    'paid': 6
}

def getDatabaseConnection(collection):
    global db

    if db is None:
        setClient()

    return db[collection]

def setClient():
    mongoClient = MongoClient(os.getenv('DB'))
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

"""performs a findOne on db for a matching handle in teachers collection"""
def getTeacherFromDiscord(handle):
    
    global db
    if db is None:
        setClient()

    filter = {'discord': handle}
    id = db['teachers'].find_one(filter).id
    return id

def getLessons(filter):
    db = getDatabaseConnection('lessons')
    return db.find(filter)

def makeAvailabilityTable():
    db = getDatabaseConnection('rooms')
    data = db.find()
    return AvailabilityTable(data)