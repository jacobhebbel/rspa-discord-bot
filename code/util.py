db = None
status = {
    'pending': 1,
    'conflicted': 2,
    'impossible': 3,
    'secured': 4,
    'confirmed': 5,
    'booked': 6,
    'filled': 7,
    'past': 8,
    'paid': 9
}

def printTestResults(results):
    GREEN, RED, RESET = '\033[92m', '\033[91m', '\033[0m'
    
    totalTests = len(results)
    numPassed = sum(int(res) for res in results)

    print(f'Test Results:\t{numPassed} / {totalTests} passed\n')

    for i, res in enumerate(results):
        color = GREEN if res else RED
        status = 'pass' if res else 'fail'
        print(f'Result of Test {i + 1}:\t{color}{status}{RESET}')

def getDatabaseConnection(collection):
    global db

    if db is None:
        setClient()

    return db[collection]

def setClient():
    from pymongo import MongoClient
    import os

    mongoClient = MongoClient(os.getenv('DB'))
    global db
    db = mongoClient['scheduling']

def lessonToDatetime(lesson):
    from datetime import datetime
    # assume a formatting function is applied to the lesson variable
    # when the object passes the validation function (happens prior in execution)
    lessonDate = lesson['date'].split('/')
    lessonTime = lesson['time'].split(':')
    
    if len(lessonDate) != 3 or len(lessonTime) != 2:
        raise Exception("Lesson date/time arguments are not initialized")
    
    return datetime(int(lessonDate[2]), int(lessonDate[0]), int(lessonDate[1]), int(lessonTime[0]), int(lessonTime[1], 0))

def lessonToTimedelta(lesson):
    from datetime import timedelta

    return timedelta(hours=1) if lesson['isFullHour'] else timedelta(minutes=30)

def lessonsConflict(lessonA, lessonB):

    # uses datetime objects to intuitively compare events 
    datetimeA, datetimeB = lessonToDatetime(lessonA), lessonToDatetime(lessonB)
    durationA, durationB = lessonToTimedelta(lessonA), lessonToTimedelta(lessonB)

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
    from scheduling.availabilityTable import AvailabilityTable

    db = getDatabaseConnection('rooms')
    data = db.find()
    return AvailabilityTable(data)

def updateLessonFields(lesson, fieldToValue):
    for field, value in fieldToValue.items():
        lesson[field] = value