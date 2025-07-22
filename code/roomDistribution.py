import util
def getLessons(filter):
    db = util.getDatabaseConnection('lessons')
    return db.find(filter)

def findRoomForLesson(lesson, availableRooms):

    # getting datetime objects from lessons for intuitive comparisons
    lessonDatetime = util.lessonToDateTime(lesson)
    lessonDate, lessonStart = lessonDatetime.date(), lessonDatetime.time()
    lessonDuration = time(minute=60) if lesson['isFullHour'] else time(minute=30)
    
    openRoom = None
    for room in availableRooms:
        if lessonDate in room.keys():
            # means this room has availability on this day
            
            for time, duration in room:
                # time is a time in the day and duration is how long the room is open from that time key

                if time < lessonStart and time + duration > lessonStart + lessonDuration:
                    # means the room has an availability that covers the lesson start and duration

                    # updating availableRooms to block out this lesson
                    room.update({time: lessonStart - time})
                    room.update({lessonStart + lessonDuration: duration - (lessonStart + lessonDuration)})
                    openRoom = room
                    break
    
    return openRoom

def distributeConflictedLessons(availableRooms):

    conflictedLessons = getLessons(filter={'status': util.status['conflicted']})
    for lesson in conflictedLessons:

        # available room
        room = findRoomForLesson(lesson, availableRooms)

        if room is None:
            raise NotImplementedError
            # alert teacher that their lesson could not be secured; send future availability
            # update lesson status to incompatible in database

        else:
            raise NotImplementedError
            # alert teacher that their lesson was secured
            # update lesson status to secured, assign room to lesson, update database

def distributeSecuredLessons(availableRooms):

    securedLessons = getLessons(filter={'status': util.status['secured'], 'building': ''})
    # plan: use a greedy algorithm for simple lesson distribution (guaranteed to work bc all lessons matching the filter don't conflict with each other)
    # optimizations for evenly distributing room use: 
    # -> make a variable Map[time][duration] = [available rooms] for a time complexity optimization
    # -> count the hours of use remaining per day in each room; try to minimze variance of use across rooms
    # -> distribute bigger lessons first bc they're harder to place
    # -> count number of room uses in a day as another way to break ties
    raise NotImplementedError