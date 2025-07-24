from datetime import time
from classes.loadBalancer import LoadBalancer
from classes.availabilityTable import AvailabilityTable
import util

def findRoomForLesson(lesson, availability):

    # getting datetime objects from lessons for intuitive comparisons
    lessonDatetime = util.lessonToDateTime(lesson)
    lessonDate, lessonStart = lessonDatetime.date(), lessonDatetime.time()
    lessonDuration = time(minute=60) if lesson['isFullHour'] else time(minute=30)
    
    openRoom = None
    datesWithAvailability = dateToAvailability.keys()
    if lessonDate not in datesWithAvailability:
        return None
    
    for room in dateToAvailability[lessonDate]:
        for openingStart, openingDuration in room:
            # start time and duration of an opening for a given room
            
            if openingStart < lessonStart and openingDuration > lessonDuration:
                # means the room has an availability that covers the lesson start and duration

                # updating availableRooms to block out this lesson
                timeUntilLessonStart = lessonStart - openingStart
                timeAfterLessonEnd = openingDuration - lessonDuration

                # update the table
                room.update({openingStart: timeUntilLessonStart})
                room.update({lessonStart + lessonDuration: timeAfterLessonEnd})
                
                openRoom = room
                break
    
    return openRoom

def distributeConflictedLessons():

    conflictedLessons = util.getLessons(filter={'status': util.status['conflicted']})
    availability = util.makeAvailabilityTable()

    for lesson in conflictedLessons:

        lessonDatetime = util.lessonToDateTime(lesson)
        lessonDuration = util.lessonDurationToDateTime(lesson)
        # available room
        rooms = availability[lessonDatetime][lessonDuration]

        if rooms == []:
            raise NotImplementedError
            # alert teacher that their lesson could not be secured; send future availability
            # update lesson status to incompatible in database

        else:
            raise NotImplementedError
            # alert teacher that their lesson was secured
            # update lesson status to secured, assign room to lesson, update database

def distributeSecuredLessons():

    securedLessons = getLessons(filter={'status': util.status['secured'], 'building': ''})
    # plan: use a greedy algorithm for simple lesson distribution (guaranteed to work bc all lessons matching the filter don't conflict with each other)
    # optimizations for evenly distributing room use: 
    # -> make a variable Map[time][duration] = [available rooms] for a time complexity optimization
    # -> count the hours of use remaining per day in each room; try to minimze variance of use across rooms
    # -> distribute bigger lessons first bc they're harder to place
    # -> count number of room uses in a day as another way to break ties

    """
    Ideal implementation: can index a date and time then see which rooms are mapped to it

    dayToAvailability[date] = {
                                building: {
                                            time: duration,
                                            time: duration
                                            },
                                building: {}
                            }
    """
    dateToAvailability = util.getDateToAvailabilityTable()
    for lesson in securedLessons:

        lessonDatetime = util.lessonToDateTime(lesson)
        availableRooms = dateToAvailability[lessonDatetime.date()]

        balancer = LoadBalancer()
        for room in availableRooms:
            roomAvailability = sum(duration for duration in room.values())
            balancer.insert(room, roomAvailability)
    
    
    raise NotImplementedError