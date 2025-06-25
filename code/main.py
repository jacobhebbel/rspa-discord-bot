from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from random import randint
from discord.ext import commands
import gspread
import os

from dotenv import load_dotenv
load_dotenv(override=True)

# useful for catching specific errors
class ValidationError(Exception):
    pass

VALID_COLUMNS = ['LessonID', 'Date', 'Time', 'Duration', 'Building Name', 'Room Number', 'Lesson Rate', 
                'Teacher Name', 'Teacher Pronouns', 'Teacher Discord', 
                'Student Name', 'Student Pronouns', 'Student Discord', 'isMember']
VALID_LOCATIONS = {
        'West': ['323', '110', '326'],
        'DCC': ['327A', '327B', '327C'],
        'Union': ['5507']
    }

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
    """returns a discord client using discord library"""
    TOKEN = os.getenv('DISCORD_TOKEN')
    bot = commands.Bot(command_prefix='!')
    return bot

# these bots should always be active *maybe not the planner*
planner = getSheetsClient()
bot = getDiscordClient()



# utility functions that directly reference the sheets api or have no abstraction
def getAllLessons():
    """returns all rows with a lessonID"""
    lessons = [lesson for lesson in planner.get_all_records() if lesson['lessonID'] != '']
    return lessons

def getLessonsFromTodayOnwards():
    """returns list of lessons happening today and future days"""
    today = datetime.today().strftime('%Y-%m-%d')
    # get all rows where lessonID is not blank and studentName is blank
    activeLessons = [lesson for lesson in planner.get_all_records() 
                        if lesson['lessonID'] != '' 
                        and lesson['date'] >= today]
    return activeLessons

def getRowNumberByLessonID(lessonID, lessonList=getAllLessons()):
    """
    returns the 0-based row number of an entry associated with a lessonID.
    throws an error if the lessonID is not in the provided lessonList
    throws an error if lessonList is empty or not type list
    """
    if not (isinstance(list, lessonList) and len(lessonList) > 0):
        raise RuntimeError('lessonList object either not a list or is empty')
    for i, row in enumerate(lessonList):
        if row['lessonID'] == lessonID:
            return i + 2
    raise ValueError('lessonID not found')

def getRowsByUserID(userID):
    raise NotImplementedError

def generateLessonID():
    """returns a randint that doesn't exist inside lessonID"""
    existingIDs = [row['lessonID'] for row in planner.get_all_records()]
    id = randint(1, 999999)
    while id in existingIDs:
        id = randint(1, 999999)
    return id

def writeTeacherInfoToSchedule(date, time, duration, building, room, rate,
                               name, pronouns, handle):
    """takes teacher data, finds an empty row, and writes to the spreadsheet"""
    rowNumber = getRowNumberByLessonID(None)
    lessonID = generateLessonID()
    values = [[lessonID, date, time, duration, building, room, rate, name, pronouns, handle, ]]
    planner.update(values, f'A{rowNumber}:J{rowNumber}')

def writeStudentInfoToSchedule(lessonID, name, pronouns, handle, isMember):
    """takes student data, finds booking by lessonID, and writes to the spreadsheet"""
    rowNumber = getRowNumberByLessonID(lessonID)
    values = [[name, pronouns, handle, isMember]]
    planner.update(values, f'K{rowNumber}:N{rowNumber}')

def userHasRole(ctx, roleName):
    """returns true / false if a user has a role"""
    return any(role.name.lower() == roleName.lower() for role in ctx.author.roles)

def getTeachers():
    """returns all teachers as a set of dictionaries"""
    global VALID_COLUMNS
    names = planner.col_values(VALID_COLUMNS.index('Teacher Name') + 1)
    pronouns = planner.col_values(VALID_COLUMNS.index('Teacher Pronouns') + 1)
    handles = planner.col_values(VALID_COLUMNS.index('Teacher Discord') + 1)

    teachers = {{
        'name': names[i],
        'pronouns': pronouns[i],
        'handle': handles[i]
    } for i in range(1, len(names))}
    return teachers
        
def getStudents():
    """returns all students as a set of dictionaries"""
    global VALID_COLUMNS
    names = planner.col_values(VALID_COLUMNS.index('Student Name') + 1)
    pronouns = planner.col_values(VALID_COLUMNS.index('Student Pronouns') + 1)
    handles = planner.col_values(VALID_COLUMNS.index('Student Discord') + 1)

    students = {{
        'name': names[i],
        'pronouns': pronouns[i],
        'handle': handles[i]
    } for i in range(1, len(names))}
    return students

def deleteLesson(lessonID):
    """finds a row by lessonID and sets all values to blanks"""
    rowNumber = getRowNumberByLessonID(lessonID)
    planner.update([['']*14], f'A{rowNumber}:N{rowNumber}')

def deleteBooking(lessonID):
    """finds a row by lessonID and sets all student values to blanks"""
    rowNumber = getRowNumberByLessonID(lessonID)
    planner.update([['']*4], f'K{rowNumber}:N{rowNumber}')

def deleteOldLessons():
    """
    deletes all entries over a month old in 1 api call\n
    documentation: https://docs.gspread.org/en/latest/user-guide.html#clear-a-worksheet
    """
    oneMonthAgo = (datetime.today() - relativedelta(months=1)).strftime('%Y-%m-%d')
    rangesToDelete = [f"A{rowNumber + 2}:Z{rowNumber + 2}" for rowNumber, lesson in enumerate(planner.get_all_records()) if lesson['date'] < oneMonthAgo]
    planner.batch_clear(rangesToDelete)





# validation functions check states of variables
def validateFilters(filter):
    """returns true if all keys in a filter are valid"""
    global VALID_COLUMNS
    if any(key not in VALID_COLUMNS for key in filter.keys()):
        raise ValidationError(f'filter keys {[key for key in filter.keys()]} references a key that isnt a valid column. valid columns: {[key for key in VALID_COLUMNS]}')

def confirmLessonExists(lessonID):
    """returns true if the lessonID matches any future lesson"""
    allLessonIDs = [lesson['LessonID'] for lesson in getLessonsFromTodayOnwards()]
    if lessonID not in allLessonIDs:
        raise ValidationError('LessonID does not match any lesson')

def confirmLessonIsAvailable(lessonID):
    """returns true if the lessonID matches any future available lesson"""
    availableLessonIDs = [lesson['LessonID'] for lesson in getLessonsFromTodayOnwards() if lesson['Student Name'] == '']
    if lessonID not in availableLessonIDs:
        raise ValidationError('RSPA does not allow booking a lesson < 1 week from the current date.')

def confirmLocationExists(building, roomNumber):
    """checks locations match hardcoded valid combinations"""
    global VALID_LOCATIONS
    if not (building in VALID_LOCATIONS.keys() and roomNumber in VALID_LOCATIONS[f'{building}']):
        raise ValidationError(f'RSPA do not have permission to book {building} {roomNumber}')
        
def confirmUserAddedThisLesson(handle, lessonID):
    """throws if this handle did not add this lesson"""
    lesson = [lesson for lesson in getAllLessons() if lesson['LessonID'] == lessonID]
    if lesson['Teacher Handle'] != handle:
        raise ValidationError('You may only cancel lessons you added')
    
def confirmUserBookedThisLesson(handle, lessonID):
    """throws if this handle did not book this lesson"""
    lesson = [lesson for lesson in getAllLessons() if lesson['lessonID'] == lessonID]
    if lesson['Student Handle'] != handle:
        raise ValidationError('You may only cancel lessons you booked')

### need to add feature that ensures lesson time ###
### validates wrt a building's accepted hours ###
def validateLesson(building, roomNumber,
                   date, time, duration):
    """returns true if a lesson's location validates\n
    and doesn't conflict with existing lessons"""

    confirmLocationExists(building, roomNumber)
    def startTime(date_, time_):
        return datetime.strptime(f"{date_} {time_}", "%Y-%m-%d %H:%M")
    def endTime(date__, time__, duration__):
        return startTime(date__, time__) + timedelta(minutes=int(duration__))

    conflictingLessons = [lesson for lesson in getLessonsFromTodayOnwards()
                          if lesson['date'] == date
                          and lesson['building'] == building
                          and lesson['roomNumber'] == roomNumber
                          and not (startTime(date, time) >= endTime(lesson['date'], lesson['time'], lesson['duration'])
                               or endTime(date, time, duration) <= startTime(lesson['date'], lesson['time']))]
    
    if conflictingLessons:
        raise ValidationError(f'This lesson conflicts with an existing lesson')

def validateBooking(lessonID):
    """checks that a lesson is free to book"""
    aWeekFromNow = (datetime.today() + relativedelta(weeks=1)).strftime('%Y-%m-%d')
    availableLessons = [lesson['lessonID'] for lesson in getLessonsFromTodayOnwards()
                        if lesson['date'] >= aWeekFromNow
                        and lesson['Student Name'] == '']
    if all(lessonID != lesson['LessonID'] for lesson in availableLessons):
        raise ValidationError('This lesson is already booked by another student')

def validateSchedule(handle, showBookings, showLessons):
    """throws ValidationError if anything doesn't check out"""
    teacherHandles = [teacher['handle'] for teacher in getTeachers()]
    studentHandles = [student['handle'] for student in getStudents()]

    if showBookings and handle not in studentHandles:
        raise ValidationError('User handle has not booked a lesson within the last month')
    if showLessons and handle not in teacherHandles:
        raise ValidationError('User handle has not added a lesson within the last month')



# abstract functions that group utility functions together
def tryAddLesson(date, time, duration, building, room, rate,
                    name, pronouns, handle):
    """
    takes teacher data, validates it, and writes to the record
    returns a success and message variables
    """
    try:
        validateLesson(building, room, 
                       date, time, duration)
        writeTeacherInfoToSchedule(date, time, duration, building, room, rate,
                                   name, pronouns, handle)
        return (True, 'Successfully added your lesson')
    except ValidationError as e:
        return (False, e.message)

def tryCancelLesson(lessonID, handle):
    """checks that the lesson exists, this handle added it, and then cancels the lesson"""
    try:
        confirmLessonExists(lessonID)
        confirmUserAddedThisLesson(handle, lessonID)
        deleteLesson(lessonID)
        return (True, f'Lesson {lessonID} successfully cancelled')
    except ValidationError as e:
        return (False, e.message)
        
def tryBookLesson(lessonID, name, pronouns, handle, isMember):
    """
    takes student data, validates it, and writes to the record
    returns a success and message variables
    """
    try:
        validateBooking(lessonID)
        writeStudentInfoToSchedule(lessonID, name, pronouns, handle, isMember)
        return (True, 'Successfully booked your lesson')
    except ValidationError as e:
        return (False, e.message)

def tryCancelBooking(lessonID, handle):
    """checks that the lesson exists & the user made this booking then cancels it"""
    try:
        confirmLessonExists(lessonID)
        confirmUserBookedThisLesson(handle, lessonID)
        deleteBooking(lessonID)
        return (True, f'Booking {lessonID} successfully cancelled')
    except ValidationError as e:
        return (False, e.message)

def tryGetSchedule(handle, showBookings=False, showLessons=False, showPast=False):
    """gets all events applicable to the arguments"""
    futureLessons = [lesson for lesson in getLessonsFromTodayOnwards() if lesson['Teacher Handle'] == handle]
    pastLessons = [lesson for lesson in getAllLessons() if lesson['Teacher Handle'] == handle and lesson not in futureLessons]
    futureBookings = [booking for booking in getLessonsFromTodayOnwards() if booking['Student Handle'] == handle]
    pastBookings = [booking for booking in getAllLessons() if booking['Student Handle'] == handle and booking not in futureBookings]

    schedule = {}
    if showPast:
        if showBookings:
            schedule.update('futureBookings', futureBookings)
            schedule.update('pastBookings', pastBookings)
        if showLessons:
            schedule.update('futureLessons', futureLessons)
            schedule.update('pastLessons', pastLessons)
    else:
        if showBookings:
            schedule.update('futureBookings', futureBookings)
        if showLessons:
            schedule.update('futureLessons', futureLessons)
    
    return schedule





# bot functions. each name is a command users type.
@bot.event()
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def addLesson(ctx, name: str, pronouns: str, rate: float,
                    building: str, room: str, date: str, time: str, duration: int):
    """teacher command to post a lesson"""
    if not userHasRole(ctx, 'teacher'):
        await ctx.send('You don\'t have the proper role to access this command')
    else:
        success, msg = tryAddLesson(date, time, duration,
                                    building, room, rate, 
                                    name, pronouns, ctx.author.id)
        if not success:
            print('failed an add lesson')
        await ctx.send(msg)

@bot.command()
async def bookLesson(ctx, name: str, pronouns: str, lessonID: str):
    """student command to book an available lesson"""
    isMember = False
    if userHasRole(ctx, 'Voting Member'):
        isMember = True
    else:
        success, msg = tryBookLesson(lessonID, name, pronouns, ctx.author.id, isMember)
        if not success:
            print('failed a book lesson')
        await ctx.send(msg)

@bot.command()
async def cancelLesson(ctx, lessonID: str):
    """cancel command used by teachers"""
    if not userHasRole(ctx, 'teacher'):
        await ctx.send('must be a teacher to access this command')
    else:
        success, msg = tryCancelLesson(lessonID, ctx.author.id)
        if not success:
            print('failed cancelLesson')
        await ctx.send(msg)

@bot.command()
async def cancelBooking(ctx, lessonID: str):
    """cancel booking command used by students"""
    success, msg = tryCancelBooking(lessonID, ctx.author.id)
    if not success:
        print('failed cancel booking')
    await ctx.send(msg)

@bot.command()
async def schedule(ctx, showBookings, showLessons, showPast):
    """prints all lessons & bookings"""
    result = tryGetSchedule(ctx.author.id, showBookings, showLessons, showPast)
    s = ''
    for key in result.keys:
        s += str(key) + ':\n\n'
        for lesson in result[f'{key}']:
            s += 'Date: ' + str(lesson['Date']) + '\tTime: ' + str(lesson['Time'])
            s += 'Location: ' + str(lesson['Building Name']) + ' ' + str(lesson['Room Number'])
            s += 'Duration: ' + str(lesson['Duration']) + '\tRate: ' + str(lesson['Rate'])
            s += 'Teacher: ' + str(lesson['Teacher Name']) + '\tDiscord: ' + str(lesson['Teacher Handle'])
            s += 'Student: ' + str(lesson['Student Name']) + '\tDiscord: ' + str(lesson['Student Handle'])
            s += '--------------------\n'
    await ctx.send(s)
    
def main():
    raise NotImplementedError
    # 1. initialize both clients
    # 2. wait for commands then call functions