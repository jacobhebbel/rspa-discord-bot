from scheduling.roomSolver import RoomSolver
from datetime import datetime, timedelta
import util

global rs
rs = None



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

    lessonA = {
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
    }
    lessonB = {
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
    }
    lessonC = {
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
    }
    
    rs = RoomSolver([doc1, doc2, doc3], [lessonA, lessonB, lessonC])

    return True
    

def testAssignIncomingLesson():
    return False

def testDistributeSecuredLessons():
    return False

def testDistributeConflictedLessons():
    return False

def main():

    results = [testInit(), testAssignIncomingLesson(), testDistributeSecuredLessons(), testDistributeConflictedLessons()]
    util.printTestResults(results)

if __name__ == '__main__':
    main()