from flask import Flask, request
from scheduling.roomSolver import RoomSolver as Assigner
from scheduling.roomValidator import RoomValidator as Validator
import util

server = Flask(__name__)

@server.route('/addLesson', methods=['POST'])
def receiveAndProcessLesson():
    data = request.get_json()
    lesson = data['lesson']

    result = Validator.validateLesson(lesson)
    if result['validated'] == False:
        return f'Fields missing and/or unformatted {result['missingFields']}', 400
    
    succeeded = Assigner.assignIncomingLesson(lesson)
    if succeeded:
        return f'Lesson was added with status: {lesson['status']}', 200
    else:
        return 'Lesson failed to be added, try again', 500

@server.route('/cancelLesson', methods=['GET'])
def cancelLesson():
    # 1. pull user info from request and get their mongo doc from the 'teachers' collection
    # 2. if they're blacklisted, inform them that they cannot interact with the program until they meen with eboard
    # 3. if the lesson id doesn't match anything, tell them the id didn't match an existing lesson
    # 4. cancel the lesson and update mongodb
    # 5. affirm that the lesson was cancelled
    # 6. if the lesson was booked, inform the student unless the date of the lesson had already passed 
    raise NotImplementedError

@server.route('/addBooking', methods=['POST'])
def addBooking():
    # 1. pull user info from request and get their mongo doc from the 'teachers' collection
    # 2. if they're blacklisted, inform them that they cannot interact with the program until they meen with eboard
    # 3. if the id doesn't match an existing lesson, inform the user that the id didn't match anything
    # 4. if the id matches an already booked / past lesson inform the user that this lesson is unable to be booked
    # 5. else, book the lesson and update mongo
    # 6. respond to the user that the lesson was booked
    # 7. notify the teacher that the lesson was booked
    raise NotImplementedError

@server.route('/cancelBooking', methods=['GET'])
def cancelBooking():
    # 1. pull user info from request and get their mongo doc from the 'teachers' collection
    # 2. if they're blacklisted, inform them that they cannot interact with the program until they meen with eboard
    # 3. if the booking id doesn't match an existing entry, tell the user that the entry doesn't exist
    # 4. if the booking has already happened, inform the user that bookings cannot be cancelled after they happen
    # 5. if the booking happens that day, inform the user that bookings cannot be cancelled day of and that they should ask the teacher to pull the lesson
    # 6. else, cancel it
    # 7. respond to the command affirming the booking was cancelled
    # 8. inform the teacher the student cancelled the booking
    raise NotImplementedError

@server.route('/availableRooms', methods=['GET'])
def getAvailableRoomData():
    # 1. pull user info from request and get their mongo doc from the 'teachers' collection
    # 2. if they're blacklisted, inform them that they cannot interact with the program until they meen with eboard
    # 3. pull all the documents from the 'rooms' collection, filter by date.
    # 4. respond in a visually-appealing format, maybe with an image file?
    raise NotImplementedError

@server.route('/availableBookings', methods=['GET'])
def getAvailableBookingsData():
    # 1. pull user info from request and get their mongo doc from the 'students' collection
    # 2. if they're blacklisted, inform them that they cannot interact with the program until they meet with eboard
    # 3. pull all docs in the lessons collection and filter out: past lessons, lessons within 1 week of NOW(), lessons with assigned students
    # 4. organize this information into a visually appealing format, possible image of a calendar? mention teacher info & rate, lesson length, date & time
    raise NotImplementedError

@server.route('/myBookings', methods=['GET'])
def getUserBookings():
    # 1. pull user info from request; discord bot has already verified role permissions
    # 2. get user's entry from the 'students' collection in mongo
    # 3. if they're blacklisted, respond that they aren't eligible for lessons and have to contact eboard
    # 4. using their id pull all lessons matching that id
    # 5. breaking this data down is now subjective, but it can be organized by the lesson's status & date
    # 5. -> lesson date is useful to know 'when' their lesson is
    # 5. -> lesson status helps them know if they still need to pay for it
    # 5. -> most important fields: location, teacher, price, date & time, duration, status 
    raise NotImplementedError

@server.route('/myLessons', methods=['GET'])
def getUserLessons():
    # 1. pull discord handle and get their mongo entry from the 'teachers' collection
    # 2. if they're blacklisted, notify them that they're ineligible to give lessons and must contact eboard
    # 3. use their teacher id to pull all lesson docs from the 'lessons' collection
    # 4. organize the response into a visually-appealing format
    # 4. -> possible sections: "upcoming", "unpaid", "this week", "recent status change"
    raise NotImplementedError

@server.route('/uploadSchedule', methods=['POST'])
def uploadScheduleData():
    data = request.get_json()
    schedule = data['schedule']
    availabilityTable = util.uploadScheduleData(schedule)
    RD.

    



    # 1. reformat this data to be ready for db insertion
    # 2. insert this data into the database as a new document for each date
    # 3. give room assignments for conflicted lessons
    # 4. notify every teacher in this pool of their lesson's updated status
    # 5. distribute room assignments for secured lessons
    # 6. notify every teacher in this pool of their lesson's new room assignment