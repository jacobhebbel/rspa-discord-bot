from scheduling.roomBalancer import RoomBalancer as RB
import util
from datetime import timedelta

def testInit():
    from datetime import timedelta
    data = {
        'Room A': timedelta(hours=5),
        'Room B': timedelta(hours=4),
        'Room C': timedelta(seconds=1)
            }
    
    rb = RB(data)
    return True

def testAddItem():

    data = {
        'Room A': timedelta(hours=5),
        'Room B': timedelta(hours=4),
        'Room C': timedelta(hours=3),
        'Room D': timedelta(hours=2)
            }
    
    rb = RB(data)

    rb.addItem('Room E', timedelta(hours=1))
    return rb.topItem() == ('Room E', timedelta(hours=1))

def testPopItem():
    data = {
        'Room A': timedelta(hours=5),
        'Room B': timedelta(hours=4),
        'Room C': timedelta(hours=3),
        'Room D': timedelta(hours=2)
            }
    
    rb = RB(data)
    rb.popItem()

    return rb.topItem() == ('Room C', timedelta(hours=3))

def testIncrementKey():
    
    data = {
        'Room A': timedelta(hours=5),
        'Room B': timedelta(hours=4),
        'Room C': timedelta(hours=3),
        'Room D': timedelta(hours=2)
            }
    
    rb = RB(data)

    rb.incrementKey('Room D', timedelta(minutes=30))
    print(rb.topItem())
    return rb.topItem() == ('Room D', timedelta(hours=2, minutes=30))

def main():

    results = [testInit(), testAddItem(), testPopItem(), testIncrementKey()]
    util.printTestResults(results)

if __name__ == '__main__':
    main()