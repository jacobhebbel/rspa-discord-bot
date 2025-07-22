import util
def getLessons(filter):
    db = util.getDatabaseConnection('lessons')
    return db.find(filter)

def findRoomForLesson(lesson, availableRooms):

    # getting datetime objects from lessons for intuitive comparisons
    lessonDatetime = util.lessonToDateTime(lesson)
    lessonDate, lessonTime = lessonDatetime.date(), lessonDatetime.time()
    lessonDuration = time(minute=60) if lesson['isFullHour'] else time(minute=30)
    
    openRoom = None
    for room in availableRooms:
        if lessonDate in room.keys():
            # means this room has availability on this day

            for time, duration in room:
                if time < lessonTime and time + duration > lessonTime + lessonDuration:
                    # means the room has an availability that covers the lesson start and duration
                    openRoom = room
                    break
    
    return openRoom

def distributeConflictedLessons(availableRooms):

    conflictedLessons = getLessons(filter={'status': util.status['conflicted']})
    for lesson in conflictedLessons:

        # available room
        room = findRoomForLesson(lesson)

        if room is None:
            raise NotImplementedError
            # alert teacher that their lesson could not be secured; send future availability
            # update lesson status to incompatible in database

        else:
            raise NotImplementedError
            # alert teacher that their lesson was secured
            # update lesson status to secured, assign room to lesson, update database



    

