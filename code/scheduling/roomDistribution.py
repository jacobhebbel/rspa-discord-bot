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
        
        # available rooms
        rooms = availability[lesson]

        if rooms == []:
            lessonToRoom.insert({lesson: None})

        else:
            assignedRoom = rooms[0]
            availability.blockAvailability(lesson, assignedRoom)
            lessonToRoom.insert({lesson: assignedRoom})

    return lessonToRoom


def buildLessonHeap(lessons, at):
    import heapq as hq

    heap = hq.heapify([])
    for lesson in lessons:
        rooms = at[lesson]
        priority = len(rooms)   # builds a minimum priority queue
        hq.heappush((priority, (lesson, rooms)))
    
    return heap
    

def makeRoomBalancers(dates):
    from scheduling.roomBalancer import RoomBalancer
    
    dateToBalancer = {}
    for date in dates:
        
        db = util.getDatabaseConnection('schedule')
        dateFilter = {'date': date.strftime('%m-%d-%Y')}
        schedule = db.find_one(filter=dateFilter)
        rb = RoomBalancer(schedule)
        dateToBalancer.insert({date: rb})
    
    return dateToBalancer

def getBestRoom(balancer, rooms):

    bestRoom, capacityRemaining = None
    temp = []
    while balancer.size() > 0 and bestRoom not in rooms:
        bestRoom, capacityRemaining = balancer.topItem()
        temp.append((bestRoom, capacityRemaining))
        balancer.pop()
    
    for room, capacity in temp:
        balancer.add(room, capacity)

    if room in rooms:
        return room
    else:
        ### I don't know how we get here, so probably should throw an error
        raise Exception(f'Did not find any of {rooms} inside load balancer; logic error')
    

def distributeSecuredLessons():
    import heapq as hq

    securedLessons = util.getLessons(filter={'status': util.status['secured'], 'building': ''})
    availability = util.makeAvailabilityTable()
    dateToBalancer = makeRoomBalancers(dates=set(util.lessonToDatetime(lesson).date()))
    orderedLessons = buildLessonHeap(securedLessons, availability)
    lessonToRoom = {}
    
    while orderedLessons != []:
        lesson, availableRooms = hq.heappop(orderedLessons)
        balancer = dateToBalancer[util.lessonToDatetime(lesson).date()]

        bestRoom = getBestRoom(balancer, availableRooms)
        lessonDuration = util.lessonToTimedelta(lesson)
        balancer.decrementKey(bestRoom, lessonDuration)

        lessonToRoom.update({lesson: bestRoom})

    return lessonToRoom
