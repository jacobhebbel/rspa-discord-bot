import scheduling.roomAssignment as RA
import util

def testInsertWithNoConflict():
    """
    Tests processing non-conflicting lesson
    """
    lessonA = {
        'date': '1/1/2000',
        'time': '13:00',
        'isFullHour': True
    }
    lessonB = {
        'date': '1/2/2000', # note the different dates, implying they shouldn't conflict
        'time': '13:30',
        'isFullHour': False
    }
    
    lessons = [lessonA]
    doesConflict = RA.checkForConflict(newLesson=lessonB, existingLessons=lessons)
    print('Test1 result:', doesConflict == False)
    return doesConflict == False

def testInsertWithConflict():
    """
    Tests processing conflicting lesson
    """
    lessonA = {
        'date': '1/1/2000',
        'time': '13:00',    
        'isFullHour': True  # this lesson goes from 13:00 to 14:00
    }   
    lessonB = {
        'date': '1/1/2000', # the dates are the same this time
        'time': '13:30',    
        'isFullHour': False
    }   

    lessons = [lessonA]
    doesConflict = RA.checkForConflict(newLesson=lessonB, existingLessons=lessons)
    print('Test2 result:', doesConflict == True)
    return doesConflict == True

def testStatusAfterNoConflictInsert():
    """
    Tests lesson fields are updated properly
    """

    lessonA = {
        'date': '1/1/2000',
        'time': '13:00',
        'isFullHour': True,
        'status': util.status['secured']
    }
    lessonB = {
        'date': '1/2/2000', # note the different dates, implying they shouldn't conflict
        'time': '13:30',
        'isFullHour': False,
        'status': util.status['pending']
    }
    
    lessons = [lessonA]
    doesConflict = RA.checkForConflict(newLesson=lessonB, existingLessons=lessons)
    RA.updateLessonFields(lessonB, doesConflict)
    print('Test3 result:', lessonB['status'] == util.status['secured'])
    return lessonB['status'] == util.status['secured']

    
def testStatusAfterConflictInsert():
    lessonA = {
        'date': '1/1/2000',
        'time': '13:00',    
        'isFullHour': True,  # this lesson goes from 13:00 to 14:00
        'status': util.status['secured']
    }   
    lessonB = {
        'date': '1/1/2000', # the dates are the same this time
        'time': '13:30',    
        'isFullHour': False,
        'status': util.status['pending']
    }   

    lessons = [lessonA]
    doesConflict = RA.checkForConflict(newLesson=lessonB, existingLessons=lessons)
    RA.updateLessonFields(lessonB, doesConflict)
    print('Test4 result:', lessonB['status'] == util.status['conflicted'])
    return lessonB['status'] == util.status['conflicted']

def main():

    results = [testInsertWithNoConflict(), testInsertWithConflict(), testStatusAfterNoConflictInsert(), testStatusAfterConflictInsert()]
    totalTests = len(results)
    numPassed = sum(int(res) for res in results)
    
    print(f'Test Results:\t{numPassed} / {totalTests} passed')

if __name__ == '__main__':
    main()