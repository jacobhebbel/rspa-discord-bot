import util
from datetime import datetime, timedelta
from scheduling.lesson import Lesson

lessonA = Lesson({
    'start': datetime(2000, 1, 1, 8, 30),
    'end': datetime(2000, 1, 1, 9),
    'duration': timedelta(minutes=30)
})


def testInit():
    raise NotImplementedError

def testIndex():
    raise NotImplementedError

def testDatetimeConflict():
    raise NotImplementedError

def testFullConflict():
    raise NotImplementedError

def testFitsInside():
    raise NotImplementedError

def main():

    results = []
    util.printTestResults(results)

if __name__ == '__main__':
    main()