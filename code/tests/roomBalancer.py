from scheduling.roomBalancer import RoomBalancer as RB
import util

def testInitialization():
    from datetime import timedelta
    data = {
        'Room A': timedelta(hours=5),
        'Room B': timedelta(hours=4),
        'Room C': timedelta(seconds=1)
            }
    
    flag = True
    try:
        rb = RB(data)
        print(rb.heap)
    except:
        flag = False
    finally:
        return flag

def testOrdering():
    from datetime import timedelta
    data = {
        'Room A': timedelta(seconds=1),
        'Room B': timedelta(minutes=1),
        'Room C': timedelta(hours=1)
            }
    
    flag = True
    rb = RB(data)

    room, capacity = rb.topItem()
    rb.pop()

    if (room != 'Room C') or (capacity != timedelta(hours=1)):
        flag = False

    room, capacity = rb.topItem()
    rb.pop()

    if (room != 'Room B') or (capacity != timedelta(minutes=1)):
        flag = False

    room, capacity = rb.topItem()
    rb.pop()

    if (room != 'Room A') or (capacity != timedelta(seconds=1)):
        flag = False

    return flag

def testDecrementKey():
    from datetime import timedelta
    data = {
        'Room A': timedelta(seconds=1),
        'Room B': timedelta(minutes=1),
        'Room C': timedelta(hours=1)
    }
    
    rb = RB(data)

    rb.decrementKey('Room C', timedelta(minutes=30))
    room, capacity = rb.topItem()
    return capacity == timedelta(minutes=30)


def main():

    results = [testInitialization(), testOrdering(), testDecrementKey()]
    util.printTestResults(results)

if __name__ == '__main__':
    main()