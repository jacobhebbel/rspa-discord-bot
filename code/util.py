from pymongo import MongoClient
from datetime import datetime, date, time, timedelta
from scheduling.availabilityTable import AvailabilityTable
from scheduling.loadBalancer import LoadBalancer
import os

db = None
status = {
    'pending': 1,
    'conflicted': 2,
    'incompatible': 3,
    'secured': 4,
    'confirmed': 5,
    'booked': 6,
    'filled': 7,
    'past': 8,
    'paid': 9
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
    
    return datetime(int(lessonDate[2]), int(lessonDate[0]), int(lessonDate[1]), int(lessonTime[0]), int(lessonTime[1], 0))

def durationToTimeDelta(lesson):
    return timedelta(hours=1) if lesson['isFullHour'] else timedelta(minutes=30)

def lessonsConflict(lessonA, lessonB):

    # uses datetime objects to intuitively compare events 
    datetimeA, datetimeB = lessonToDateTime(lessonA), lessonToDateTime(lessonB)
    durationA, durationB = durationToTimeDelta(lessonA), durationToTimeDelta(lessonB)

    # ensures A doesn't bleed into B's start and that B doesn't bleed into A's start
    return (datetimeA.date() == datetimeB.date()) and (datetimeA + durationA > datetimeB or datetimeB + durationB > datetimeA)

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

def makeLoadBalancers(dates):
    dateToBalancer = {}
    for date in dates:
        
        db = getDatabaseConnection('schedule')
        schedule = db.find_one(date)
        lb = LoadBalancer(schedule)
        dateToBalancer.insert({date: lb})
    
    return dateToBalancer
