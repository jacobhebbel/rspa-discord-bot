import scheduling.roomDistribution as RD
import scheduling.availabilityTable as AT
import util

def testAssignLessonsAllPossible():
    
    lessonA = {
        'date': '1/1/2000',
        'time': '13:00',
        'isFullHour': True,
        'status': util.status['conflicted']
    }

    lessonB = {
        'date': '1/1/2000',
        'time': '13:30',
        'isFullHour': False,
        'status': util.status['conflicted']
    }

    lessonC = {
        'date': '1/1/2000',
        'time': '08:30',
        'isFullHour': False,
        'status': util.status['conflicted']
    }
    conflictedLessons = [lessonA, lessonB, lessonC]

    roomAvailabilities = {
        'West Hall - 323': [('10:00', '35'), ('12:30', '115')],
        'DCC - 327A': [('07:00', '215', '16:00', '60')]
    }
    initialData = [{'1/1/2000': roomAvailabilities}]
    
    availability = AT(initialData)

