from search import search

class Schedule:
    def __init__(self, sections=[]):
        self.sections = sections
        self._updateDays()
    
    def addSection(self, section):
        self.sections.append(section)
        self._updateDays()
    
    def removeSection(self, section):
        idx = self.sections.index(section)
        if idx != -1:
            self.sections.remove(self.sections[idx])

        self._updateDays()
    
    def detectTimeConflict(self):
        conflictClasses = []

        for sections in self.days.values():
            dayTimes = [] # Stores (startTime, endTime, section) for each class in the day

            for section in sections:
                timeRange = section._getAbsoluteTimeRange() # Returns (startTime, endTime)
                startTime = timeRange[0]

                # Look for time conflicts
                for time in dayTimes:
                    if time[0] <= startTime <= time[1] and (time[2], section) not in conflictClasses:
                        conflictClasses.append((time[2], section))
                
                # Add the time slot to the day 
                dayTimes.append((*timeRange, section))

        return conflictClasses

    def detectLabConflict(self):
        conflictSections = []

        for classSection in self.section:
            # Check if the class has a lab section 
            if (classSection.course.hasLabSection() or classSection.course.hasRecitationSection()): # and not (classSection.isLab() or classSection.isRecitation()):
                # Check to see if the class has a lab section scheduled
                for labSection in self.section:
                    if labSection.isLab() or labSection.isRecitation():
                        break
                else:
                    conflictSections.append(classSection)        

                
    
    def _updateDays(self):
        self.days = {
            'M': [],
            'T': [],
            'W': [],
            'R': [],
            'F': [],
        }

        # Add the section to each day
        for section in self.sections:
            if section.days == 'None':
                continue

            for day in section.days:
                self.days[day].append(section)

        
sections =  search('cs 100')[0].sections
sched = Schedule([sections[5], sections[6]])

sched.addSection(search('cs 495')[0].sections[0])
sched.addSection(search('cs 440')[0].sections[0])

for (c1, c2) in sched.detectTimeConflict():
    print(c1.course.cid, c2.course.cid)