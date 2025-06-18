from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from random import randint
import discord
import gspread
import os

from dotenv import load_dotenv
load_dotenv(override=True)


def getSheetsClient():
    """
    returns a google sheets client using gspread\n
    follows documentation indicated here: https://docs.gspread.org/en/latest/oauth2.html
    """
    keyPath = os.getenv('GOOGLE_AUTH_PATH')
    lessonSheet = os.getenv('GOOGLE_SPREADSHEET_NAME')
    lessons = os.getenv('GOOGLE_WORKSHEET_NAME')

    client = gspread.service_account(filename=keyPath)
    sheet = client.open(lessonSheet)
    return sheet.worksheet(lessons)

def getDiscordClient():
    """
    returns a discord client using discord library\n
    no progress on this so far :((((
    """
    TOKEN = os.getenv('DISCORD_TOKEN')
    client = discord.Client()
    raise NotImplementedError('need to develop discord client')

# these bots should always be active *maybe not the planner*
planner = getSheetsClient()
bot = getDiscordClient()

def getRowNumberByLessonID(lessonID):
    for i, row in enumerate(planner.get_all_records()):
        if row['lessonID'] == lessonID:
            return i + 2
    raise ValueError('lessonID not found')

def getActiveLessons():
    """
    returns list of future open lessons
    """
    today = datetime.today().strftime('%Y-%m-%d')
    # get all rows where lessonID is not blank and studentName is blank
    activeLessons = [lesson for lesson in planner.get_all_records() 
                        if lesson['lessonID'] != '' 
                        and lesson['date'] >= today]
    return activeLessons

def validateLocation(building, roomNumber):
    """checks locations match hardcoded valid combinations"""
    validCombinations = {
        'West': ['323', '110', '326'],
        'DCC': ['327A', '327B', '327C'],
        'Union': ['5507']
    }

    if building not in validCombinations.keys():
        return False
    if roomNumber not in validCombinations[f'{building}']:
        return False
    return True

def validateFilter(filterKeys):
    """checks if keys match hardcoded valid column names in the spreadsheet"""
    validKeys = ['TeacherName', 'Location', 'Duration', 'Price', 'Date', 'Time']
    for key in filterKeys:
        if key not in validKeys:
            return False
    return True

def isLessonAvailable(lessonID):
    """returns true if a lesson doesn't have a student"""
    availableLessonsIDs = [lesson['lessonID'] for lesson in getActiveLessons() if lesson['studentName'] == '']
    if lessonID in availableLessonsIDs:
        return True
    return False

def validateLesson(building, roomNumber,
                   duration, date, time):
    """returns true if a lesson's location validates\n
    and doesn't conflict with existing lessons"""

    if not validateLocation(building, roomNumber):
        return False
    
    def start(date_, time_):
        return datetime.strptime(f"{date_} {time_}", "%Y-%m-%d %H:%M")
    def end(date__, time__, duration__):
        return start(date__, time__) + timedelta(minutes=int(duration__))

    conflictingLessons = [lesson for lesson in getActiveLessons()
                          if lesson['date'] == date
                          and lesson['building'] == building
                          and lesson['roomNumber'] == roomNumber
                          and not (start(date, time) >= end(lesson['date'], lesson['time'], lesson['duration'])
                               or end(date, time, duration) <= start(lesson['date'], lesson['time']))]
    if conflictingLessons:
        return False
    return True

def validateBooking(lessonID):
    """checks that a lesson is free to book"""
    aWeekFromNow = (datetime.today() + relativedelta(weeks=1)).strftime('%Y-%m-%d')
    availableLessons = [lesson['lessonID'] for lesson in getActiveLessons()
                        if lesson['date'] >= aWeekFromNow]
    if lessonID in availableLessons:
        return True
    return False

def generateLessonID():
    """returns a randint that doesn't exist inside lessonID"""
    existingIDs = [row['lessonID'] for row in planner.get_all_records()]
    id = randint(1, 999999)
    while id in existingIDs:
        id = randint(1, 999999)
    return id

def addLesson(teacherName, teacherPronouns, rate,
              duration, building, roomNumber, date, time):
    """
    writes to an empty row with the given information\n
    generates a unique lessonID number for this entry\n
    throws an error if building / roomNumber doesn't exist\n
    throws an error if conflicts with other lessons
    """
    
    if not validateLesson(building, roomNumber):
        raise RuntimeError('building / room combination did not match valid rooms')
    
    rowNumber = getRowNumberByLessonID('')
    range = f'A{rowNumber}:I{rowNumber}'
    values = [teacherName, teacherPronouns, rate,
            duration, building, roomNumber, date, time]
    planner.update(range, [values])

def bookLesson(studentName, studentPronouns, lessonID, isMember):
    """
    writes to the row matching on lessonID\n
    fills in the student-type fields\n
    throws error if lessonID is already booked\n
    throws error if lesson is < 1 week away
    """  
    if not validateBooking(lessonID):
        raise RuntimeError('the lesson corresponding to this id has already been booked')
    rowNumber = getRowNumberByLessonID(lessonID)
    range = f'J{rowNumber}:L{rowNumber}'
    values = [studentName, studentPronouns, isMember]
    planner.update(range, [values])

def getAvailability(filters: dict):
    """
    returns all rows based on filter args; essentially\n
    WHERE filterKey (col in table) = filterKey's Value\n
    throw an error if a key is not a column name
    """
    lessons = [
        lesson for lesson in getActiveLessons()
        if all(str(lesson.get(key, '')).lower() == str(filters[key]).lower() for key in filters)]
    
    raise NotImplementedError('this needs to be worked on')

def doCancel(lessonID, isTeacher):
    rowNumber = getRowNumberByLessonID(lessonID)
    if isTeacher:
        planner.batch_clear([f'{rowNumber}:{rowNumber}'])
    else:
        planner.batch_clear([f'J{rowNumber}:L{rowNumber}'])

def cancelBooking(lessonID):
    """used by students to cancel their booking"""
    doCancel(lessonID, False)

def cancelLesson(lessonID):
    """used by teachers to cancel a lesson"""
    doCancel(lessonID, True)

def deleteOldLessons():
    """
    deletes all entries over a month old in 1 api call\n
    documentation: https://docs.gspread.org/en/latest/user-guide.html#clear-a-worksheet
    """
    oneMonthAgo = (datetime.today() - relativedelta(months=1)).strftime('%Y-%m-%d')
    rangesToDelete = [f"A{rowNumber + 2}:Z{rowNumber + 2}" for rowNumber, lesson in enumerate(planner.get_all_records()) if lesson['date'] < oneMonthAgo]
    planner.batch_clear(rangesToDelete)

def main():
    raise NotImplementedError
    # 1. initialize both clients
    # 2. wait for commands then call functions