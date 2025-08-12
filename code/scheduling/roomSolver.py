import util

class RoomSolver:

    def __init__(self, data):
        from scheduling.roomBalancer import RoomBalancer
        from scheduling.availabilityTable import AvailabilityTable as AT
        from datetime import datetime

        self.at = AT(data)
        self.dateToRBs = {datetime.fromisoformat(doc['date']).date(): RoomBalancer(doc['timeBooked']) for doc in data}


    # marks as secured / conflicted if it has a datetime conflict or not
    def assignIncomingLesson(self, incoming, securedLessons):

        from scheduling.lesson import Lesson
        if not isinstance(incoming, Lesson):
            raise Exception('assignIncomingLesson arg must be type lesson, is type', type(incoming))
        
        if securedLessons == []:
            incoming['status'] = util.status['secured']
        else:
            conflictingLessons = [lesson for lesson in securedLessons if incoming.datetimeConflict(lesson)]
            incoming['status'] = util.status['secured'] if conflictingLessons == [] else util.status['conflicted']

    # greedily assigns lessons to room availabilities using room balancers to even out usage
    def distributeSecuredLessons(self, securedLessons):
        import heapq as hq

        availabilityTable = self.at
        lessonToRoom = {}
        
        for lesson in securedLessons:
            print(f'Lesson at {lesson['start']} has these rooms available: {availabilityTable[lesson]}')

        for date in (availabilityTable.roomData).keys():

            work = self.buildLessonHeap(securedLessons, availabilityTable)
            balancer = self.dateToRBs[date]
        
            while work:
                priority, lesson, availableRooms = hq.heappop(work)

                bestRoom = self.getBestRoom(balancer, availableRooms)
                balancer.incrementKey(bestRoom, lesson['duration'])

                lessonToRoom.update({lesson: bestRoom})

        for lesson, roomAssignment in lessonToRoom.items():
            lesson['location'] = roomAssignment

        return lessonToRoom.keys()
    def buildLessonHeap(self, lessons: list, at):
        import heapq as hq

        heap = [((len(at[lessonObj]), idx), lessonObj, at[lessonObj]) for idx, lessonObj in enumerate(lessons)]
        hq.heapify(heap)

        return heap
    
    def getBestRoom(self, balancer, rooms):

        bestRoom, hoursBooked = None, None
        temp = []
        while not balancer.isEmpty() and bestRoom not in rooms:
            hoursBooked, bestRoom = balancer.topItem()
            temp.append((hoursBooked, bestRoom))
            balancer.popItem()
        
        for room, hoursBooked in temp:
            balancer.addItem(room, hoursBooked)

        if room in rooms:
            return room
        else:
            ### I don't know how we get here, so probably should throw an error
            raise Exception(f'Did not find any of {rooms} inside load balancer; logic error')

    # CSP for assigning conflicted lessons rooms. uses AC3 & forward checking heuristics to reduce search space
    def distributeConflictedLessons(self, conflictedLessons):

        variables = [lesson for lesson in conflictedLessons if lesson['status'] is util.status['conflicted']]
        
        domains = self.at
        variableToDomains = {v: [(v['start'], v['duration'], room) for room in domains[v]] for v in variables}
        
        reducedDomains = self.domainReduction(variableToDomains)
        roomAssignments = self.backtrackAlgorithm(assignment={}, variables=reducedDomains.keys(), variableToDomains=reducedDomains)
        mapping = self.updateLessonObjects(roomAssignments)
        return mapping
    def domainReduction(self, domains):
        variables = domains.keys()
        rooms = self.at

        work = [(vx, vy) for vx in variables for vy in variables if vx != vy]
        while work:
            vx, vy = work.pop()
            Dx, Dy = domains[vx], domains[vy]
            updateArcs = False

            for dx in Dx[:]:
                if not any(self.satisfiesConstraint(dx, dy) for dy in Dy):
                    Dx.remove(dx)
                    updateArcs = True
                
            if updateArcs:
                updateArcs = False
                for vz in variables:
                    if (vz != vx) and (vz != vy) and any(room in rooms[vz] for room in rooms[vx]):
                        work.append((vz, vx))
        
        return domains
    def backtrackAlgorithm(self, assignment, variables, variableToDomains):

        if len(assignment) == len(variables):
            return assignment
        
        work = [v for v in variables if v not in assignment.keys()]
        work = sorted(work, key=lambda v: len(self.at[v]))  # prioritizes lessons with fewest options first
        v = work[0]

        for domain in variableToDomains[v]:

            if all(self.satisfiesConstraint(domain, d) for d in assignment.values()):
                
                newAssignment = assignment.copy()
                newAssignment[v] = domain
                
                prunedDomains = {v: list(variableToDomains[v]) for v in work[1:]}
                if self.forwardCheck(domain, prunedDomains):
                
                    prunedDomains[v] = [domain]
                    result = self.backtrackAlgorithm(newAssignment, variables, prunedDomains)
                    if result is not None:
                        return result

        return None
    def satisfiesConstraint(self, domainA, domainB):
            startA, durationA, roomA = domainA
            startB, durationB, roomB = domainB
            endA, endB = startA + durationA, startB + durationB

            return not (roomA == roomB and startA < endB and startB < endA)
    def forwardCheck(self, domain, unassigned):

        for v, domains in unassigned.items():
            validDomains = [d for d in domains if self.satisfiesConstraint(domain, d)]
            
            if validDomains == []:
                return False
            else:
                unassigned[v] = validDomains
        
        return True

    # helper function that sets a lesson's fields after being assigned a room
    def updateLessonObjects(self, mapping):

        for lesson, room in mapping:
            lesson['location'] = room if room is not None else ''
            lesson['status'] = util.status['secured'] if room is not None else util.status['impossible']


