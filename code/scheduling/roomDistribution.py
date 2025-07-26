import util

def assignLessonsToRooms(lessonToRoom):
    for lesson, roomTuple in lessonToRoom.items():
        
        # at this point in the program, the lesson object has already been preprocessed
        # all we have to do is set the room assignment in lesson and update the date document corresponding to lesson
        # Additionally, update lesson's status to confirmed

        building, room = roomTuple
        lesson['building'], lesson['room'] = building, room
        lesson['status'] = util.status['confirmed']

def distributeConflictedLessons():

    conflictedLessons = util.getLessons(filter={'status': util.status['conflicted']})
    availability = util.makeAvailabilityTable()
    lessonToRoom = {}

    for lesson in conflictedLessons:

        lessonDatetime = util.lessonToDateTime(lesson)
        lessonDuration = util.lessonDurationToTime(lesson)
        
        # available rooms
        rooms = availability[lessonDatetime][lessonDuration]

        if rooms == []:
            lessonToRoom.insert({lesson: None})

        else:
            assignedRoom = rooms[0]
            availability.blockSlot(lesson, assignedRoom)
            lessonToRoom.insert({lesson: assignedRoom})

    return lessonToRoom

        

def distributeSecuredLessons():

    securedLessons = util.getLessons(filter={'status': util.status['secured'], 'building': ''})
    availability = util.makeAvailabilityTable()
    dateToBalancer = util.makeLoadBalancers()
    lessonToRoom = {}

    for lesson in securedLessons:

        lessonDatetime = util.lessonToDateTime(lesson)
        availableRooms = availability[lessonDatetime.date()]
        balancer = dateToBalancer[lessonDatetime.date()]

        # temp holds values from the pq after we pop them for re-insertion
        optimalRoom, hoursRemaining = None, 0
        temp = []

        # loop thru the priority queue and take the first optimal room thats available
        while optimalRoom not in availableRooms and not balancer.isEmpty():
            optimalRoom, hoursRemaining = balancer.popTop()
            temp.append((optimalRoom, hoursRemaining))
            
        # means default room is the only one available
        if optimalRoom is None:
            lessonToRoom.insert({lesson: availableRooms[0]})

        else:
            
            # room assignment logic for the variables
            roomIndex = temp.index((optimalRoom, hoursRemaining))
            lessonToRoom.insert({lesson: optimalRoom})
            availability.blockOut(lesson, optimalRoom)
            
            # updating the pq through the temp index; reducing the hours remaining for the optimal room
            newHoursRemaining = hoursRemaining - util.lessonDurationToTime(lesson)
            temp[roomIndex] = (optimalRoom, newHoursRemaining)
        
        balancer.insert(item for item in temp) # adds everything back to the pq

    return lessonToRoom
