from oauth2client.service_account import ServiceAccountCredentials
import discord
import gspread
import os

from dotenv import load_dotenv
load_dotenv(override=True)

def getSheetsClient():
    jsonKey = os.getenv('GOOGLE_AUTH_KEY')
    budgetSheet = os.getenv('GOOGLE_SHEET_NAME')
    scopes = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(jsonKey, scopes)
    client = gspread.authorize(creds)
    sheet = client.open(budgetSheet).sheet1
    return sheet

def getDiscordClient():
    TOKEN = os.getenv('DISCORD_TOKEN')
    client = discord.Client()
    raise NotImplementedError

def addLesson(teacherName, teacherPronouns, rate,
              duration, building, roomNumber, date, time):
    # writes to an empty row with the given information
    # generates a unique lessonID number for this entry
    # throws an error if building / roomNumber doesn't exist
    raise NotImplementedError
def bookLesson(studentName, studentPronouns, lessonID, isMember):
    # writes to the row matching the lessonID
    # should throw an error if another student's name is there
    raise NotImplementedError
def getAvailability(filters: dict):
    # gets all rows that match the filters
    raise NotImplementedError
def cancelLesson(name, lessonID, isTeacher):
    # if student: remove all student-type fields from the matching row
    # if teacher: delete the whole row
    raise NotImplementedError
def deleteOldRows(date):
    # deletes all rows with dates before or matching the given date
    raise NotImplementedError
def main():
    raise NotImplementedError
    # 1. initialize both clients
    # 2. wait for commands then call functions