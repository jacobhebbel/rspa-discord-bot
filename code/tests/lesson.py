import util
from datetime import datetime, timedelta
from scheduling.lesson import Lesson

'''
Each lesson object is initialized with a dictionary similar to the result of calling mongo for a lesson document
'''

global lessonA
global lessonB
global lessonC

lessonA, lessonB, lessonC = None, None, None




def testInit():
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
        'datetime': datetime(2000, 1, 1, 9).isoformat(),
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
        'datetime': datetime(2000, 1, 1, 8).isoformat(),
        'duration': timedelta(minutes=60).seconds,
        'building': 'West Hall',
        'room': '323',
        'hasRoom': True,
        'status': util.status['pending'],
    })

    return isinstance(lessonA, Lesson) and isinstance(lessonB, Lesson) and isinstance(lessonC, Lesson)

def testIndex():
    global lessonA

    expected = 'West Hall - 323'
    observed = lessonA['location']
    return expected == observed


def testDatetimeConflict():
    global lessonA, lessonB, lessonC

    doesConflict, doesNotConflict = True, False

    return (
        (lessonA.datetimeConflict(lessonB) == doesNotConflict) and (lessonB.datetimeConflict(lessonA) == doesNotConflict) and 
        (lessonA.datetimeConflict(lessonC) == doesConflict) and (lessonC.datetimeConflict(lessonA) == doesConflict)
    )

def testRoomConflict():
    global lessonA, lessonB, lessonC

    doesConflict, doesNotConflict = True, False

    return (
        (lessonA.roomConflict(lessonB) == doesNotConflict) and (lessonB.roomConflict(lessonA) == doesNotConflict) and
        (lessonA.roomConflict(lessonC) == doesConflict) and (lessonC.roomConflict(lessonA) == doesConflict)
    )

def testToDatabase():
    global lessonA, lessonB, lessonC
    
    dataA = {
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
    dataB = {
        'id': '2',
        'teacherId': 'hope',
        'studentId': '',
        'hasStudent': False,
        'packageId': '',
        'isPackage': False,
        'datetime': datetime(2000, 1, 1, 9).isoformat(),
        'duration': timedelta(minutes=30).seconds,
        'building': 'West Hall',
        'room': '326',
        'hasRoom': True,
        'status': util.status['secured'],
    }
    dataC = {
        'id': '3',
        'teacherId': 'Army',
        'studentId': '',
        'hasStudent': False,
        'packageId': '',
        'isPackage': False,
        'datetime': datetime(2000, 1, 1, 8).isoformat(),
        'duration': timedelta(minutes=60).seconds,
        'building': 'West Hall',
        'room': '323',
        'hasRoom': True,
        'status': util.status['pending'],
    }

    return lessonA.toDatabase() == dataA and lessonB.toDatabase() == dataB and lessonC.toDatabase() == dataC

def testFitsInside():
    raise NotImplementedError

def main():

    results = [testInit(), testIndex(), testDatetimeConflict(), testRoomConflict(), testToDatabase()]
    util.printTestResults(results)

if __name__ == '__main__':
    main()