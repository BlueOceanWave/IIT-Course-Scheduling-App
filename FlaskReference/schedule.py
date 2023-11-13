from search import search

class Schedule:
    def __init__(self, sections=[]):
        self.sections = sections
        self._updateDays()
    
    # Adds a section to the schedule
    def addSection(self, section):
        self.sections.append(section)
        self._updateDays()
    
    # Removes a section from the schedule
    def removeSection(self, section):
        idx = self.sections.index(section)
        if idx != -1:
            self.sections.remove(self.sections[idx])

        self._updateDays()
    
    # Returns list of conflict classes
    # Each conflict is a tuple of two sections
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

    # Returns a list of sections missing its lab/class
    def detectLabConflict(self):
        conflictSections = []

        for section1 in self.sections:
            is_section1_lab = section1.isLab() or section1.isRecitation()
            # print(section1.course.cid, is_section1_lab)

            # Check if the class has a lab section 
            if (section1.course.hasLabSection() or section1.course.hasRecitationSection()):
                # Check to see if the class has a lab section scheduled or vice versa
                for section2 in self.sections:
                    is_section2_lab = section2.isLab() or section2.isRecitation()
                    # print('  ', section2.course.cid, is_section2_lab, is_section1_lab^is_section2_lab)
                    if (section1.course == section2.course) and (is_section1_lab ^ is_section2_lab):
                        break
                else:
                    if section1 not in conflictSections:
                        conflictSections.append(section1)            

        return conflictSections
    
    # Update each day with its classes
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

        
# sections =  search('cs 330')[0].sections
# sched = Schedule([sections[0]])#, sections[6]])

# sched.addSection(search('cs 495')[0].sections[0])
# sched.addSection(search('cs 440')[0].sections[0])

# for (c1, c2) in sched.detectTimeConflict():
#     print(f'Time conflict: {c1.course.cid}, {c2.course.cid}')
# for c in sched.detectLabConflict():
#     print('Missing lab/class: ', c.course.cid)


print(search('cs 495')[0].sections[0].days)
print(search('cs 495')[0].sections[0].daysToIndex())