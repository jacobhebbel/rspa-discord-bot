from flask import Flask, redirect, url_for, request
import utils as util

server = Flask(__name__)

@server.route('/addLesson', methods=['POST'])
def receiveAndProcessLesson():
    data = request.get_json()
    lesson = data['lesson']

    result = util.validateLesson(lesson)
    if result['validated'] == False:
        return f'Fields missing and/or unformatted {result['missingFields']}', 400
    
    succeeded = util.processNewLesson(lesson)
    if succeeded == True:
        return f'Lesson was added with status: {lesson['status']}', 200
    else:
        return 'Lesson failed to be added, try again', 500

@server.route('/cancelLesson', methods=['GET'])
def cancelLesson():
    raise NotImplementedError

@server.route('/addBooking', methods=['POST'])
def addBooking():
    raise NotImplementedError

@server.route('/cancelBooking', methods=['GET'])
def cancelBooking():
    raise NotImplementedError

@server.route('/availableRooms', methods=['GET'])
def getAvailableRoomData():
    raise NotImplementedError

@server.route('/availableBookings', methods=['GET'])
def getAvailableBookingsData():
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

    # 1. reformat this data to be ready for db insertion
    # 2. insert this data into the database as a new document for each date
    # 3. give room assignments for conflicted lessons
    # 4. notify every teacher in this pool of their lesson's updated status
    # 5. distribute room assignments for secured lessons
    # 6. notify every teacher in this pool of their lesson's new room assignment