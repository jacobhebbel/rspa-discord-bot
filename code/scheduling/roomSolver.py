from datetime import datetime
import util

class RoomSolver:

    def __init__(self, data):
        from scheduling.lesson import Lesson
        from scheduling.roomBalancer import RoomBalancer
        from scheduling.availabilityTable import AvailabilityTable as AT
        
        self.date = datetime.fromisoformat(data['date'])
        self.lessons = [Lesson(lesson) for lesson in util.getLessons(filter={'date': data['date']})]
        self.at = AT(data)
        self.rb = RoomBalancer(data['capacities'])

    def assignIncomingLesson(self, incoming):
        from scheduling.lesson import Lesson
        if not isinstance(incoming, Lesson):
            incoming = Lesson(incoming)
        
        conflictingLessons = [lesson for lesson in self.lessons if (lesson['status'] is util.status['secured']) and incoming.conflictsWith(lesson)]
        return conflictingLessons == []

    def distributeSecuredLessons(self):
        import heapq as hq

        securedLessons = [lesson for lesson in self.lessons if lesson['status'] is util.status['secured']][:]
        availability, balancer = self.at, self.rb
        orderedLessons = self.buildLessonHeap(securedLessons, availability)
        lessonToRoom = {}
        
        while orderedLessons != []:
            lesson, availableRooms = hq.heappop(orderedLessons)

            bestRoom = self.getBestRoom(balancer, availableRooms)
            balancer.decrementKey(bestRoom, lesson['duration'])

            lessonToRoom.update({lesson: bestRoom})

        return lessonToRoom

    def buildLessonHeap(lessons, at):
        import heapq as hq

        heap = hq.heapify([])
        for lesson in lessons:
            rooms = at[lesson]
            priority = len(rooms)   # builds a minimum priority queue
            hq.heappush((priority, (lesson, rooms)))
    
        return heap

    def getBestRoom(balancer, rooms):

        bestRoom, capacityRemaining = None
        temp = []
        while balancer.size() > 0 and bestRoom not in rooms:
            bestRoom, capacityRemaining = balancer.topItem()
            temp.append((bestRoom, capacityRemaining))
            balancer.popItem()
        
        for room, capacity in temp:
            balancer.addItem(room, capacity)

        if room in rooms:
            return room
        else:
            ### I don't know how we get here, so probably should throw an error
            raise Exception(f'Did not find any of {rooms} inside load balancer; logic error')


    def distributeConflictedLessons(self):

        variables = [lesson for lesson in self.lessons if lesson['status'] is util.status['conflicted']]
        
        domains = self.at
        variableToDomains = {v: [(v['start'], v['duration'], room) for room in domains[v]] for v in variables}
        
        reducedDomains = self.domainReduction(variableToDomains)
        roomAssignments = self.backtrackAlgorithm(assignment={}, variables=reducedDomains.keys(), variableToDomains=reducedDomains)
        mapping = self.updateLessonObjects(roomAssignments)
        return mapping
    
    # implementation of basic AC3
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
                for vz in variables:                    # gets shared rooms via set intersection
                    if (vz != vx) and (vz != vy) and set(rooms[vx]) & set(rooms[vz]):
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
            
    def updateLessonObjects(self, mapping):
        pass
