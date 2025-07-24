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
    raise NotImplementedError

@server.route('/myLessons', methods=['GET'])
def getUserLessons():
    # 1. pull discord handle and get their mongo entry from the 'teachers' collection
    # 2. if they're blacklisted, notify them that they're ineligible to give lessons and must contact eboard
    # 3. use their teacher id to pull all lesson docs from the 'lessons' collection
    # 4. organize the response into a visually-appealing format
    # 4. -> possible sections: "upcoming", "unpaid", "this week", "recent status change"
    raise NotImplementedError