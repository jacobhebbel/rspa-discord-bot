import scheduling.availabilityTable as AT
import util

def testBuildingTable():

    date1 = '1/1/2000'
    date2 = '1/2/2000'
    date3 = '1/3/2000'

    availability1 = {
        'West Hall - 323': [('08:00', '35'), ('13:00', '50')],
        'Rensselaer Union - 5502': [('08:00', '720')],
        'DCC - 327A': [('13:00', '35'), ('17:50', '130')]
    }

    availability2 = {
        'West Hall - 327': [('09:15', '35'), ('18:00', '50')],
        'Rensselaer Union - 5502': [('08:00', '720')],
        'DCC - 327C': [('13:00', '35'), ('17:50', '130')]
    }

    availability3 = {
        'West Hall - 110': [('08:00', '35'), ('13:00', '50')],
        'West Hall - 326': [('08:00', '60'), ('14:00', '35')],
        'DCC - 327B': [('13:00', '35'), ('17:50', '130')]
    }

    roomData = {
        date1: availability1,
        date2: availability2,
        date3: availability3
    }

    at1 = AT(roomData)
    at2 = AT({date3: availability3})

def testIndexOperatorAvailableLesson():

    date = '1/1/2000'
    availability = {
        'West Hall - 323': [('08:00', '35'), ('13:00', '50')],
        'DCC - 327A': [('13:00', '35'), ('17:50', '130')]
    }
    roomData = {date: availability}

    at = AT(roomData)
    availableLesson = {
        'date': '1/1/2000',
        'time': '08:00',
        'isFullHour': False,
        'status': util.status['conflicted']
    }

    availability = at[util.lessonToDateTime(availableLesson)][util.durationToTimeDelta(availableLesson)]
    return availability == ['West Hall - 323']

def testIndexOperatorUnavailableLesson():

    date = '1/3/2000'
    availability = {
        'West Hall - 110': [('08:00', '35'), ('13:00', '50')],
        'West Hall - 326': [('08:00', '60'), ('14:00', '35')],
        'DCC - 327B': [('13:00', '35'), ('17:50', '130')]
    }
    roomData = {date: availability}

    at = AT(roomData)
    unavailableLesson = {
        'date': '1/3/2000',
        'time': '12:00',
        'isFullHour': True,
        'status': util.status['secured']
    }

    availability = at[util.lessonToDateTime(unavailableLesson)][util.durationToTimeDelta(unavailableLesson)]
    return availability == []