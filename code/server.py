from flask import Flask, redirect, url_for, request
import * as util from utils

server = Flask(__name__)

@server.route('/addLesson', methods=['POST'])
def receiveAndProcessLesson():
    data = request.get_json()
    lesson = data['lesson']

    result = util.validateLesson(lesson)
    if result.validated == False:
        return f'Missing required fields {result.fields}', 400
    
    succeeded = util.processLesson(lesson)
    if succeeded == True:
        return f'Lesson was added with status: {lesson['status']}', 200
    else:
        return 'Lesson failed to be added, try again', 500
    