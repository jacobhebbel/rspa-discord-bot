import util

class RoomSolver:

    def __init__(self, date):
        from scheduling.roomBalancer import RoomBalancer

        filter = {'date': date.strf('%Y-%m-%d')}
        self.lessons = util.getLessons(filter=filter)
        self.at = util.makeAvailabilityTable(filter)
        self.rb = RoomBalancer(util.getSchedule(date))

    def assignIncomingLesson(self, incoming):
        conflictingLessons = [lesson for lesson in self.lessons if (lesson['status'] is util.status['secured']) and util.lessonsConflict(lesson, incoming)]
        return conflictingLessons == []

    def distributeSecuredRooms(self):
        import heapq as hq

        securedLessons = [lesson for lesson in self.lessons if lesson['status'] is util.status['secured']][:]
        availability, balancer = self.at, self.rb
        orderedLessons = self.buildLessonHeap(securedLessons, availability)
        lessonToRoom = {}
        
        while orderedLessons != []:
            lesson, availableRooms = hq.heappop(orderedLessons)

            bestRoom = self.getBestRoom(balancer, availableRooms)
            lessonDuration = util.lessonToTimedelta(lesson)
            balancer.decrementKey(bestRoom, lessonDuration)

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
            balancer.pop()
        
        for room, capacity in temp:
            balancer.add(room, capacity)

        if room in rooms:
            return room
        else:
            ### I don't know how we get here, so probably should throw an error
            raise Exception(f'Did not find any of {rooms} inside load balancer; logic error')


    def distributeConflictedRooms(self):

        variables = [lesson for lesson in self.lessons if lesson['status'] is util.status['conflicted']]
        variables = sorted(variables, key=len(self.at[v] for v in variables))
        domains = self.at
        vToD = {v: (v['start'], v['duration'], room for room in domains[v]) for v in variables}
        self.domainReduction(vToD)
        self.roomAssignment(vToD)
    
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
                if all(util.lessonsConflict(dx, dy) for dy in Dy):
                    Dx.remove(dx)
                    updateArcs = True
                
            if updateArcs:
                updateArcs = False
                for vz in variables:                    # gets shared rooms via set intersection
                    if (vz != vx) and (vz != vy) and (set(rooms[vx] & set(rooms[vz]))):
                        work.append((vz, vx))
        
        return domains

