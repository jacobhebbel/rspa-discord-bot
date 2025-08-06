from scheduling.availabilityTable import AvailabilityTable as AT
from scheduling.lesson import Lesson
from datetime import datetime, timedelta
import util

global lessonA, lessonB, lessonC
lessonA = Lesson({
    'id': '1',
    'teacherId': 'jacob',
    'studentId': '',
    'hasStudent': False,
    'packageId': '',
    'isPackage': False,
    'datetime': datetime(2000, 1, 1, 8, 30).isoformat(),
    'duration': timedelta(minutes=30).seconds,
    'building': 'West Hall',
    'room': '323',
    'hasRoom': True,
    'status': util.status['secured'],
})
lessonB = Lesson({
    'id': '2',
    'teacherId': 'hope',
    'studentId': '',
    'hasStudent': False,
    'packageId': '',
    'isPackage': False,
    'datetime': datetime(2000, 1, 2, 9).isoformat(),
    'duration': timedelta(minutes=30).seconds,
    'building': 'West Hall',
    'room': '326',
    'hasRoom': True,
    'status': util.status['secured'],
})
lessonC = Lesson({
    'id': '3',
    'teacherId': 'Army',
    'studentId': '',
    'hasStudent': False,
    'packageId': '',
    'isPackage': False,
    'datetime': datetime(2000, 1, 3, 8).isoformat(),
    'duration': timedelta(minutes=60).seconds,
    'building': 'West Hall',
    'room': '323',
    'hasRoom': True,
    'status': util.status['pending'],
})

global at
at = None

def testInit():

    doc1 = {
        'date': datetime(2000, 1, 1).isoformat(),
        'rooms': ['WH - 323', 'RU - 5502', 'DCC - 327A'],
        'isCurrent': True,
        'schedules': {
            'WH - 323': [
                {'start': datetime(2000, 1, 1, 8).isoformat(),'duration': timedelta(minutes=30).seconds}, 
                {'start': datetime(2000, 1, 1, 12).isoformat(), 'duration': timedelta(minutes=120).seconds},
                {'start': datetime(2000, 1, 1, 20).isoformat(), 'duration': timedelta(minutes=90).seconds}
            ],
            'RU - 5502': [
                {'start': datetime(2000, 1, 1, 8).isoformat(),'duration': timedelta(minutes=120).seconds}
            ],
            'DCC - 327A': [
                {'start': datetime(2000, 1, 1, 13).isoformat(),'duration': timedelta(minutes=35).seconds},
                {'start': datetime(2000, 1, 1, 17, 50).isoformat(), 'duration': timedelta(minutes=130).seconds},
            ]   
        },
        'capacities': {
            'WH - 323': 240*60,
            'RU - 5502': 120*60,
            'DCC - 327A': 165*60
        }
    }

    doc2 = {
        'date': datetime(2000, 1, 2).isoformat(),
        'isCurrent': True,
        'rooms': ['WH - 326', 'WH - 327', 'DCC - 327A', 'DCC - 327B', 'DCC - 327C'],
        'schedules': {
            'WH - 326': [
                {'start': datetime(2000, 1, 2, 8).isoformat(), 'duration': timedelta(minutes=120).seconds},
                {'start': datetime(2000, 1, 2, 12).isoformat(), 'duration': timedelta(minutes=120).seconds}
            ],
            'WH - 327': [
                {'start': datetime(2000, 1, 2, 8, 15).isoformat(), 'duration': timedelta(minutes=35).seconds},
                {'start': datetime(200, 1, 2, 18).isoformat(), 'duration': timedelta(minutes=50).seconds}
            ],
            'DCC - 327A': [
                {'start': datetime(2000, 1, 2, 12).isoformat(), 'duration': timedelta(minutes=120).seconds},
                {'start': datetime(2000, 1, 2, 16).isoformat(), 'duration': timedelta(minutes=90).seconds}
            ],
            'DCC - 327B': [
                {'start': datetime(2000, 1, 2, 10).isoformat(), 'duration': timedelta(hours=9).seconds}
            ],
            'DCC - 327C': [
                {'start': datetime(2000, 1, 2, 16).isoformat(), 'duration': timedelta(hours=3).seconds},
                {'start': datetime(2000, 1, 2, 13).isoformat(), 'duration': timedelta(minutes=35).seconds}
            ]
        },
        'capacities': {
            'WH - 326': 240*60,
            'WH - 327': 85*60,
            'DCC - 327A': 210*60,
            'DCC - 327B': 9*60*60,
            'DCC - 327C': (3*60 + 35)*60
        }
    }

    doc3 = {
        'date': datetime(2000, 1, 3).isoformat(),
        'isCurrent': True,
        'rooms': ['WH - 110', 'WH - 326', 'DCC - 327B', 'RU - 5502'],
        'schedules': {
            'WH - 110': [
                {'start': datetime(2000, 1, 3, 8).isoformat(), 'duration': timedelta(minutes=35).seconds},
                {'start': datetime(2000, 1, 3, 13).isoformat(), 'duration': timedelta(minutes=50).seconds}
            ],
            'WH - 326': [
                {'start': datetime(2000, 1, 3, 8).isoformat(), 'duration': timedelta(minutes=95).seconds},
                {'start': datetime(2000, 1, 3, 14).isoformat(), 'duration': timedelta(minutes=35).seconds}
            ],
            'DCC - 327B': [
                {'start': datetime(2000, 1, 3, 13).isoformat(), 'duration': timedelta(minutes=35).seconds},
                {'start': datetime(2000, 1, 3, 17, 50).isoformat(), 'duration': timedelta(minutes=130).seconds}
            ],
            'RU - 5502': [
                {'start': datetime(2000, 1, 3, 8).isoformat(), 'duration': timedelta(hours=14).seconds}
            ]
        },
        'capacities': {
            'WH - 110': 85*60,
            'WH - 326': 95*60,
            'DCC - 327B': 165*60,
            'RU - 5502': 14*60*60
        }
    }
    
    global at
    at = AT([doc1, doc2, doc3])

    return True

def testIndexWithLesson():
    global at, lessonA, lessonB, lessonC

    expectedA = ['RU - 5502']
    expectedB = ['WH - 326']
    expectedC = ['WH - 326', 'RU - 5502']

    resA, resB, resC = at[lessonA], at[lessonB], at[lessonC]

    return expectedA == resA and expectedB == resB and expectedC == resC

def testIndexWithDate():
    global at

    dateA, dateB, dateC = datetime(2000, 1, 1), datetime(2000, 1, 2), datetime(2000, 1, 3)
    expectedA = ['WH - 323', 'RU - 5502', 'DCC - 327A']
    expectedB = ['WH - 326', 'WH - 327', 'DCC - 327A', 'DCC - 327B', 'DCC - 327C']
    expectedC = ['WH - 110', 'WH - 326', 'DCC - 327B', 'RU - 5502']

    resA, resB, resC = at[dateA.date()], at[dateB.date()], at[dateC.date()]

    return expectedA == list(resA) and expectedB == list(resB) and expectedC == list(resC)

def testBlockAvailability():
    global at, lessonA, lessonB, lessonC

    roomsA, roomsB, roomsC = at[lessonA], at[lessonB], at[lessonC]
    roomA, roomB, roomC = roomsA[0], roomsB[0], roomsC[0]

    at.blockAvailability(lessonA, roomA)
    at.blockAvailability(lessonB, roomB)

    at.blockAvailability(lessonC, roomC)

    return (roomA not in at[lessonA]) and (roomB not in at[lessonB]) and (roomC not in at[lessonC])

def main():

    results = [testInit(), testIndexWithLesson(), testIndexWithDate(), testBlockAvailability()]
    util.printTestResults(results)

if __name__ == '__main__':
    main()