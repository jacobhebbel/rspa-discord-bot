import util

class RoomSolver:

    def __init__(self, date):
        filter = {'date': date.strf('%Y-%m-%d')}
        self.lessons = util.getLessons(filter=filter)
        self.at = util.makeAvailabilityTable(filter)

    def filterRooms():
        pass

    def distributeConflictedRooms(self):
        
        # implementation of basic AC3
        def domainReduction(domains):
            variables = domains.keys()
            rooms = self.at

            work = [(vx, vy) for vx in variables for vy in variables if vx != vy]
            while work is not []:
                vx, vy = work.pop()
                Dx, Dy = domains[vx][:], domains[vy]
                updateArcs = False

                for dx in Dx:
                    updateArcs = all(util.lessonsConflict(dx, dy) for dy in Dy)
                    
                if updateArcs:
                    for vz in variables:
                        if (vz != vx) and (vz != vy) and any(roomX == roomZ for roomX in rooms[vx] for roomZ in rooms[vz]):
                            work.append((vx, vz))

                    
            pass

        def backtrackAlgorithm(mapping, isFinished, ):
            pass

        domains = self.at
        mapping = {}
        inverseMapping = {}

        variables = [lesson for lesson in self.lessons if lesson['status'] is util.status['conflicted']]
        variables = sorted(variables, key=len(domains[v] for v in variables))


                     
    def backtrackAlgorithm():

    def distributeSecuredRooms():
        pass