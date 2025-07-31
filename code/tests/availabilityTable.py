from scheduling.availabilityTable import AvailabilityTable as AT
import util


def testBuildingTable():

    date1 = '1/1/2000'
    date2 = '1/2/2000'
    date3 = '1/3/2000'

    availability1 = {
        'West Hall - 323': [{'start': '08:00','duration': '35'}, {'start': '13:00', 'duration': '50'}],
        'Rensselaer Union - 5502': [{'start': '08:00','duration': '720'}],
        'DCC - 327A': [{'start': '13:00','duration': '35'}, {'start': '17:50', 'duration': '130'}]
    }

    availability2 = {
        'West Hall - 327': [{'start': '09:15', 'duration': '35'}, {'start': '18:00', 'duration': '50'}],
        'Rensselaer Union - 5502': [{'start': '08:00', 'duration': '720'}],
        'DCC - 327C': [{'start': '13:00', 'duration': '35'}, {'start': '17:50', 'duration': '130'}]
    }

    availability3 = {
        'West Hall - 110': [{'start': '08:00', 'duration': '35'}, {'start': '13:00', 'duration': '50'}],
        'West Hall - 326': [{'start': '08:00', 'duration': '60'}, {'start': '14:00', 'duration': '35'}],
        'DCC - 327B': [{'start': '13:00', 'duration': '35'}, {'start': '17:50', 'duration': '130'}]
    }

    roomData = {
        date1: availability1,
        date2: availability2,
        date3: availability3
    }

    at1 = AT(roomData)
    at2 = AT({date3: availability3})

    # print(at1)
    # print(at2)
    return True

def testIndexOperatorAvailableLesson():

    date = '1/1/2000'
    availability = {
        'West Hall - 323': [{'start': '08:00', 'duration': '35'}, {'start': '13:00', 'duration': '50'}],
        'DCC - 327A': [{'start': '13:00', 'duration': '35'}, {'start': '17:50', 'duration': '130'}]
    }
    roomData = {date: availability}

    at = AT(roomData)
    availableLesson = {
        'date': '1/1/2000',
        'time': '08:00',
        'isFullHour': False,
        'status': util.status['conflicted']
    }

    availability = at[availableLesson]
    return availability == ['West Hall - 323']

def testIndexOperatorUnavailableLesson():

    date = '1/3/2000'
    availability = {
        'West Hall - 110': [{'start': '08:00', 'duration': '35'}, {'start': '13:00', 'duration': '50'}],
        'West Hall - 326': [{'start': '08:00', 'duration': '60'}, {'start': '14:00', 'duration': '35'}],
        'DCC - 327B': [{'start': '13:00', 'duration': '35'}, {'start': '17:50', 'duration': '130'}]
    }
    roomData = {date: availability}

    at = AT(roomData)
    unavailableLesson = {
        'date': '1/3/2000',
        'time': '12:00',
        'isFullHour': True,
        'status': util.status['secured']
    }

    availability = at[unavailableLesson]
    return availability == []



def testBlockFunctionNoAvailability():
    # has no availabilities, tries booking anyways
    data = {'1/1/2000': {
        'West Hall - 323': [{'start': '08:00','duration': '35'}, {'start': '13:00', 'duration': '50'}],
        'DCC - 327A': [{'start': '13:00','duration': '35'}, {'start': '17:50', 'duration': '130'}]
        }
    }
    lesson3 = {     
        'date': '1/1/2000',
        'time': '08:00',
        'isFullHour': True
    }
    at = AT(data)
    flag = False
    try:
        at.blockAvailability(lesson3, 'DCC - 327A')
    except KeyError:
        flag = True
    finally:
        return flag

def testBlockFunctionWrongRoom():
    # tries taking a room not available, raises KeyError
    data = {'1/1/2000': {
        'West Hall - 323': [{'start': '08:00','duration': '35'}, {'start': '13:00', 'duration': '50'}],
        'DCC - 327A': [{'start': '13:00','duration': '35'}, {'start': '17:50', 'duration': '130'}]
        }
    }

    at = AT(data)
    lesson = {
        'date': '1/1/2000',
        'time': '08:00',
        'isFullHour': False
    }
    at = AT(data)
    flag = False
    
    try:
        at.blockAvailability(lesson, 'DCC - 327A')
    except KeyError:
        flag = True
    finally:
        return flag

def testBlockFunctionGeneral2():
    # has availability, splits the opening into two while blocking out the middle
    from datetime import timedelta
    data = {'1/1/2000': {
        'West Hall - 323': [{'start': '08:00','duration': '35'}, {'start': '13:00', 'duration': '50'}],
        'DCC - 327A': [{'start': '13:00','duration': '35'}, {'start': '17:50', 'duration': '130'}]
        }
    }
    lesson4 = {     
        'date': '1/1/2000',
        'time': '18:00',
        'isFullHour': True
    }
    at = AT(data)
    
    rooms = at[lesson4]
    at.blockAvailability(lesson4, rooms[0])
    
    updatedBookingA = {'start': util.lessonToDatetime(lesson4) - timedelta(minutes=10), 'duration': timedelta(minutes=10)}
    updatedBookingB = {'start': util.lessonToDatetime(lesson4) + util.lessonToTimedelta(lesson4), 'duration': timedelta(hours=1)}

    roomSchedule = at.data[util.lessonToDatetime(lesson4).date()][rooms[0]]
    return (updatedBookingA in roomSchedule) and (updatedBookingB in roomSchedule)

def testBlockFunctionGeneral1():
    from datetime import timedelta
    data = {'1/1/2000': {
        'West Hall - 323': [{'start': '08:00','duration': '35'}, {'start': '13:00', 'duration': '50'}],
        'DCC - 327A': [{'start': '13:00','duration': '35'}, {'start': '17:50', 'duration': '130'}]
        }
    }

    at = AT(data)
    lesson = {         # takes the 8am slot in WH 323, no slot added beforehand, 5 min slot added after
        'date': '1/1/2000',
        'time': '08:00',
        'isFullHour': False
    }

    rooms = at[lesson]
    
    at.blockAvailability(lesson, rooms[0])
    
    roomSchedule = at.data[util.lessonToDatetime(lesson).date()][rooms[0]]
    updatedBooking = {'start': util.lessonToDatetime(lesson) + util.lessonToTimedelta(lesson), 'duration': timedelta(minutes=5)}
    return updatedBooking in roomSchedule


def main():

    results = [testBuildingTable(), testIndexOperatorAvailableLesson(), testIndexOperatorUnavailableLesson(), 
               testBlockFunctionGeneral1(), testBlockFunctionGeneral2(), testBlockFunctionWrongRoom(), testBlockFunctionNoAvailability()]
    util.printTestResults(results)

if __name__ == '__main__':
    main()