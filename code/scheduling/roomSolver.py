import util

class RoomSolver:

    def __init__(self, date):
        filter = {'date': date.strf('%Y-%m-%d')}
        self.lessons = util.getLessons(filter=filter)
        self.at = util.makeAvailabilityTable(filter)

    def assignIncomingLesson(self, incoming):
        conflictingLessons = [lesson for lesson in self.lessons if (lesson['status'] is util.status['secured']) and util.lessonsConflict(lesson, incoming)]
        return conflictingLessons == []

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

    def roomAssignment():
        pass

    def distributeSecuredRooms():
        pass