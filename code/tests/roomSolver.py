from scheduling.roomSolver import RoomSolver
from datetime import datetime, timedelta
import util

global rs
rs = None



def testInit():
    
    doc1 = {
        'date': datetime(2000, 1, 1).isoformat(),
        'rooms': ['WH - 323', 'RU - 5502', 'DCC - 327A', 'WH - 110'],
        'isCurrent': True,
        'schedules': {
            'WH - 323': [
                {'start': datetime(2000, 1, 1, 9, 30).isoformat(),'duration': timedelta(minutes=150).seconds}, 
                {'start': datetime(2000, 1, 1, 14).isoformat(), 'duration': timedelta(minutes=240).seconds}
            ],
            'RU - 5502': [
                {'start': datetime(2000, 1, 1, 8).isoformat(),'duration': timedelta(minutes=1440).seconds}
            ],
            'DCC - 327A': [
                {'start': datetime(2000, 1, 1, 18).isoformat(),'duration': timedelta(minutes=120).seconds}
            ],
            'WH - 110': [
                {'start': datetime(2000, 1, 1, 10, 30).isoformat(), 'duration': timedelta(minutes=30).seconds},
                {'start': datetime(2000, 1, 1, 13).isoformat(), 'duration': timedelta(minutes=90).seconds}
            ]
        },
        'timeBooked': {
            'WH - 323': timedelta(minutes=390).seconds,
            'RU - 5502': timedelta(minutes=1440).seconds,
            'DCC - 327A': timedelta(minutes=120).seconds,
            'WH - 110': timedelta(minutes=120).seconds
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
        'timeBooked': {
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
        'timeBooked': {
            'WH - 110': 85*60,
            'WH - 326': 95*60,
            'DCC - 327B': 165*60,
            'RU - 5502': 14*60*60
        }
    }

    rs = RoomSolver([doc1, doc2, doc3])
    return True

def testAssignIncomingLesson():
    from scheduling.lesson import Lesson
    roomSchedule = {
        'date': datetime(2000, 1, 1).isoformat(),
        'rooms': ['WH - 323', 'RU - 5502', 'DCC - 327A', 'WH - 110'],
        'isCurrent': True,
        'schedules': {
            'WH - 323': [
                {'start': datetime(2000, 1, 1, 9, 30).isoformat(),'duration': timedelta(minutes=150).seconds}, 
                {'start': datetime(2000, 1, 1, 14).isoformat(), 'duration': timedelta(minutes=240).seconds}
            ],
            'RU - 5502': [
                {'start': datetime(2000, 1, 1, 8).isoformat(),'duration': timedelta(minutes=1440).seconds}
            ],
            'DCC - 327A': [
                {'start': datetime(2000, 1, 1, 18).isoformat(),'duration': timedelta(minutes=120).seconds}
            ],
            'WH - 110': [
                {'start': datetime(2000, 1, 1, 10, 30).isoformat(), 'duration': timedelta(minutes=30).seconds},
                {'start': datetime(2000, 1, 1, 13).isoformat(), 'duration': timedelta(minutes=90).seconds}
            ]
        },
        'timeBooked': {
            'WH - 323': timedelta(minutes=390).seconds,
            'RU - 5502': timedelta(minutes=1440).seconds,
            'DCC - 327A': timedelta(minutes=120).seconds,
            'WH - 110': timedelta(minutes=120).seconds
        }
    }


    lessonA = Lesson({   # this lesson will fit within the RU block and be considered 'secured'
        'id': '1',
        'teacherId': 'jacobAsInt',
        'studentId': '',
        'hasStudent': False,
        'packageId': '',
        'isPackage': False,
        'start': datetime(2000, 1, 1, 10).isoformat(),
        'duration': timedelta(minutes=30).seconds,
        'building': '',
        'room': '',
        'hasRoom': False,
        'status': util.status['pending']
    })
    
    lessonB = Lesson({   # this lesson will datetime conflict with the previous; it will be marked as 'conflicted'
        'id': '2',
        'teacherId': 'hopeAsInt',
        'studentId': '',
        'hasStudent': False,
        'packageId': '',
        'isPackage': False,
        'start': datetime(2000, 1, 1, 10).isoformat(),
        'duration': timedelta(minutes=60).seconds,
        'building': '',
        'room': '',
        'hasRoom': False,
        'status': util.status['pending']
    })

    lessonC = Lesson({   # this lesson will fit within the RU block and be considered 'secured', however should be distributed to a different room
        'id': '3',
        'teacherId': 'armyAsInt',
        'studentId': '',
        'hasStudent': False,
        'packageId': '',
        'isPackage': False,
        'start': datetime(2000, 1, 1, 15).isoformat(),
        'duration': timedelta(minutes=30).seconds,
        'building': '',
        'room': '',
        'hasRoom': False,
        'status': util.status['pending']
    })

    rs = RoomSolver([roomSchedule])
    securedLessons = []
    
    for lesson in [lessonA, lessonB, lessonC]:
        rs.assignIncomingLesson(lesson, securedLessons)
        
        if lesson['status'] == util.status['secured']:
            securedLessons.append(lesson)  

    return (lessonA['status'] == util.status['secured']
            and lessonB['status'] == util.status['conflicted']
            and lessonC['status'] == util.status['secured']
        )

def testDistributeSecuredLessons():
    from scheduling.lesson import Lesson
    roomSchedule = {
        'date': datetime(2000, 1, 1).isoformat(),
        'rooms': ['WH - 323', 'RU - 5502', 'DCC - 327A', 'WH - 110'],
        'isCurrent': True,
        'schedules': {
            'WH - 323': [
                {'start': datetime(2000, 1, 1, 9, 30).isoformat(),'duration': timedelta(hours=2, minutes=30).seconds}, 
                {'start': datetime(2000, 1, 1, 14).isoformat(), 'duration': timedelta(hours=4).seconds}
            ],
            'RU - 5502': [
                {'start': datetime(2000, 1, 1, 8).isoformat(),'duration': timedelta(hours=6).seconds}
            ],
            'DCC - 327A': [
                {'start': datetime(2000, 1, 1, 18).isoformat(),'duration': timedelta(hours=2).seconds}
            ],
            'WH - 110': [
                {'start': datetime(2000, 1, 1, 10).isoformat(), 'duration': timedelta(hours=1).seconds},
                {'start': datetime(2000, 1, 1, 13).isoformat(), 'duration': timedelta(hours=1, minutes=30).seconds}
            ]
        },
        'timeBooked': {
            'WH - 323': timedelta(minutes=0).seconds,
            'RU - 5502': timedelta(minutes=0).seconds,
            'DCC - 327A': timedelta(minutes=0).seconds,
            'WH - 110': timedelta(minutes=0).seconds
        }
    }

    # none of these lessons will datetime conflict.
    # the objective is to distribute them evenly across their available rooms
    # such as to minimize the average difference in hoursBooked across the options
    # this optimization will favor equal use of all rooms instead of overbooking RU

    lessonA = Lesson({
        'id': '1',
        'teacherId': 'jacobAsInt',
        'studentId': '',
        'hasStudent': False,
        'packageId': '',
        'isPackage': False,
        'start': datetime(2000, 1, 1, 10).isoformat(),
        'duration': timedelta(minutes=30).seconds,
        'building': '',
        'room': '',
        'hasRoom': False,
        'status': util.status['secured']
    })
    
    lessonB = Lesson({
        'id': '2',
        'teacherId': 'hopeAsInt',
        'studentId': '',
        'hasStudent': False,
        'packageId': '',
        'isPackage': False,
        'start': datetime(2000, 1, 1, 11).isoformat(),
        'duration': timedelta(minutes=60).seconds,
        'building': '',
        'room': '',
        'hasRoom': False,
        'status': util.status['secured']
    })

    lessonC = Lesson({
        'id': '3',
        'teacherId': 'armyAsInt',
        'studentId': '',
        'hasStudent': False,
        'packageId': '',
        'isPackage': False,
        'start': datetime(2000, 1, 1, 15).isoformat(),
        'duration': timedelta(minutes=60).seconds,
        'building': '',
        'room': '',
        'hasRoom': False,
        'status': util.status['secured']
    })

    rs = RoomSolver([roomSchedule])

    securedLessons = [lessonA, lessonB, lessonC]
    rs.distributeSecuredLessons(securedLessons)

    
    return (lessonA['location'] == 'WH - 110') and (lessonB['location'] == 'RU - 5502') and (lessonC['location'] == 'WH - 323')

def testDistributeConflictedLessons():

    # features of conflicted lesson algo
    # 1. domain reduction with AC3
    # 2. forward checking optimization
    # 3. backward checking algo for assignment
    
    # how this works:
    # 1. lessons are variables, Availability objs are domains.
    # 2. make a mapping of a variable to its possible domains
    # 3. use AC-3 to delete domains that result in an incomplete mapping
    # 4. use backtracking to assign variables. use Most Constrained Variable heuristic. Use foward checking after each assignment to catch bad attempts early
    # 5. no load balancing is happening for picking the right domain; could be implemented but not needed

    from scheduling.lesson import Lesson
    roomSchedule = {
        'date': datetime(2000, 1, 1).isoformat(),
        'rooms': ['WH - 323', 'RU - 5502', 'DCC - 327A', 'WH - 110'],
        'isCurrent': True,
        'schedules': {
            'WH - 323': [
                {'start': datetime(2000, 1, 1, 9, 30).isoformat(),'duration': timedelta(hours=2, minutes=30).seconds}, 
                {'start': datetime(2000, 1, 1, 14).isoformat(), 'duration': timedelta(hours=4).seconds}
            ],
            'RU - 5502': [
                {'start': datetime(2000, 1, 1, 8).isoformat(),'duration': timedelta(hours=6).seconds}
            ],
            'DCC - 327A': [
                {'start': datetime(2000, 1, 1, 18).isoformat(),'duration': timedelta(hours=2).seconds}
            ],
            'WH - 110': [
                {'start': datetime(2000, 1, 1, 10).isoformat(), 'duration': timedelta(hours=1).seconds},
                {'start': datetime(2000, 1, 1, 13).isoformat(), 'duration': timedelta(hours=1, minutes=30).seconds}
            ]
        },
        'timeBooked': {
            'WH - 323': timedelta(minutes=0).seconds,
            'RU - 5502': timedelta(minutes=0).seconds,
            'DCC - 327A': timedelta(minutes=0).seconds,
            'WH - 110': timedelta(minutes=0).seconds
        }
    }

    lessonA = Lesson({
        'id': '1',
        'teacherId': 'jacobAsInt',
        'studentId': '',
        'hasStudent': False,
        'packageId': '',
        'isPackage': False,
        'start': datetime(2000, 1, 1, 13).isoformat(),
        'duration': timedelta(minutes=30).seconds,
        'building': '',
        'room': '',
        'hasRoom': False,
        'status': util.status['conflicted']
    })
    
    lessonB = Lesson({
        'id': '2',
        'teacherId': 'hopeAsInt',
        'studentId': '',
        'hasStudent': False,
        'packageId': '',
        'isPackage': False,
        'start': datetime(2000, 1, 1, 13).isoformat(),
        'duration': timedelta(minutes=60).seconds,
        'building': '',
        'room': '',
        'hasRoom': False,
        'status': util.status['conflicted']
    })

    lessonC = Lesson({
        'id': '3',
        'teacherId': 'armyAsInt',
        'studentId': '',
        'hasStudent': False,
        'packageId': '',
        'isPackage': False,
        'start': datetime(2000, 1, 1, 13, 30).isoformat(),
        'duration': timedelta(minutes=60).seconds,
        'building': '',
        'room': '',
        'hasRoom': False,
        'status': util.status['conflicted']
    })

    rs = RoomSolver([roomSchedule])
    rs.distributeConflictedLessons([lessonA, lessonB, lessonC])
    print([lessonA['location'], lessonB['location'], lessonC['location']])
    

    return True

def main():

    results = [testInit(), testAssignIncomingLesson(), testDistributeSecuredLessons(), testDistributeConflictedLessons()]
    util.printTestResults(results)

if __name__ == '__main__':
    main()