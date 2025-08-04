import util
import copy
from datetime import datetime, timedelta
from scheduling.lesson import Lesson
from scheduling.availability import Availability

'''
Each Availability object is initialized from a subsection of a dated schedule document
'''

global availability
availability = None

global lessonA
global lessonB
global lessonC
lessonA, lessonB, lessonC = None, None, None
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



def testInit():
    global availability

    availability = Availability({
        'location': 'West Hall - 323',
        'start': datetime(2000, 1, 1, 8, 30).isoformat(),
        'duration': timedelta(minutes=30).seconds
    })

    return isinstance(availability, Availability)

def testIndex():
    global availability
    copy_avail = copy.copy(availability)

    expected = 'West Hall - 326'
    copy_avail['location'] = expected
    observed = copy_avail['location']
    return expected == observed


def testCanFit():
    global availability
    global lessonA, lessonB, lessonC
    doesFit, doesNotFit = True, False

    print(availability.canFit(lessonA) == doesFit)
    print(availability.canFit(lessonB) == doesNotFit)
    print(availability.canFit(lessonC) == doesNotFit)

    return (availability.canFit(lessonA) == doesFit) and (availability.canFit(lessonB) == doesNotFit) and (availability.canFit(lessonC) == doesNotFit)

def testSplitOnLesson():
    global availability
    global lessonA, lessonB, lessonC


    availability['start'] -= timedelta(minutes=30)
    availability['duration'] = timedelta(hours=1, minutes=30)
    availability['end'] = availability['start'] + availability['duration']
    copyA, copyB, copyC = copy.copy(availability), copy.copy(availability), copy.copy(availability)

    resA, resB, resC = copyA.splitOnLesson(lessonA), copyB.splitOnLesson(lessonB), copyC.splitOnLesson(lessonC)
    return isinstance(resA, tuple) and isinstance(resB, Availability) and isinstance(resC, Availability)




def main():

    results = [testInit(), testIndex(), testCanFit(), testSplitOnLesson()]
    util.printTestResults(results)

if __name__ == '__main__':
    main()