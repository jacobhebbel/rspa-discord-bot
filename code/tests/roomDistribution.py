import scheduling.roomDistribution as RD
import scheduling.availabilityTable as AT
from datetime import datetime, timedelta
import util

lessons = [
        {
            'start': datetime(2000, 1, 1, 11, 00),
            'duration': timedelta(minutes=60),
            'status': util.status['secured']
        },
        {
            'start': datetime(2000, 1, 1, 8, 30),
            'duration': timedelta(minutes=60),
            'status': util.status['conflicted']
        },
        {
            'start': datetime(2000, 1, 1, 17, 50),
            'duration': timedelta(minutes=30),
            'status': util.status['secured']
        }
    ]
availability = {
        'West Hall - 323': [{'start': '08:00','duration': '35'}, {'start': '13:00', 'duration': '50'}],
        'Rensselaer Union - 5502': [{'start': '08:00','duration': '720'}],
        'DCC - 327A': [{'start': '13:00','duration': '35'}, {'start': '17:50', 'duration': '130'}]
    }
at = AT({'1/1/2000': availability})

"""
Plan for testing Room Distribution algorithm

1. Identify function hierarchy; where does the distribution happen?

"""

def main():
    results = []
    util.printTestResults(results)

if __name__ == '__main__':
    main()