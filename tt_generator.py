class TimetableGenerator:

    def __init__(self, conditions, store_combinations):
        self.condition_list = conditions
        self.generated = []
        self.total_combinations = 0
        self.stored_combinations = store_combinations-1 #last index stored (+1 for number of combinations)

    def store_timetable(self, tt):
        self.total_combinations += 1
        tt.heuristic = tt.total_time()
        
        if len(self.generated) < self.stored_combinations:
            self.generated.append(tt)
        elif len(self.generated) == self.stored_combinations:
            self.generated.append(tt)
            self.move_worst_to_last()
        else:
            if tt.heuristic < self.generated[self.stored_combinations].heuristic:  # tt is better
                self.generated.pop(self.stored_combinations)
                self.generated.append(tt)
                self.move_worst_to_last()

    def move_worst_to_last(self):
        worst_heuristic = 0
        for timetable in self.generated:
            if timetable.heuristic > worst_heuristic:
                worst_heuristic = timetable.heuristic
                worst_tt = timetable
        self.generated.remove(worst_tt)
        self.generated.append(worst_tt)
    
    def generate_timetables(self, lesson_blocks):
        self.generate(Timetable(), lesson_blocks)

    def generate(self, timetable, lesson_blocks):
        if not lesson_blocks:
            self.store_timetable(timetable)
        else:
            next_lesson_block = lesson_blocks[0]
            for shift in next_lesson_block.shifts:
                if timetable.supports(shift, self.condition_list):
                    self.generate(timetable.append_shift(shift), lesson_blocks[1:])

class Timetable:
    def __init__(self):
        self.lessons = dict()
        for weekday in range(Weekday.MONDAY, Weekday.SUNDAY): #DEV vantagem em declarar por extenso?
            self.lessons[weekday] = []

    def append_shift(self, shift):
        new_timetable = Timetable()
        new_timetable.lessons = self.lessons.copy() #new dictionary, reference to the same lists
        for slot in shift.slots:
            new_timetable.lessons[slot.day] = new_timetable.lessons[slot.day] + [slot] #new list assigned to the day for each iteration
        return new_timetable

    def supports(self, shift, condition_list):
        for condition in condition_list: #DEV: trocar ciclos de verificacao? mais comum falhar uma condicao ou haver overlap?
            if not condition.check(self, shift) :
                return False
        for slot in shift.slots:
            for existing in self.lessons[slot.day]:
                if (slot.overlaps_with(existing)):
                    return False
        return True

    #def is_feasible(self):
    #    for slot in self.lessons:
    #        for other in self.lessons:
    #            if (slot is not other) and (slot.overlaps_with(other)):
    #                return False
    #    return True

    # heuristics for selecting timetables
    def total_time(self):
        result = 0
        for weekday in range(Weekday.MONDAY, Weekday.SUNDAY):
            daily_lessons = self.lessons[weekday]
            if daily_lessons:
                earliest_start = min([slot.start.minutes for slot in daily_lessons])
                latest_end = max([slot.end.minutes for slot in daily_lessons])
                interval = latest_end - earliest_start
                result += interval + 60
        return result
        

class Course(object):

    def __init__(self, name):
        self.name = name
        self.lesson_blocks = []

    def add_lesson_block(self, lesson_block):
        self.lesson_blocks.append(lesson_block)
        lesson_block.parent_course = self

    def get_block_by_category(self, category):
        for block in self.lesson_blocks:
            if block.category == category:
                return block

class LessonBlock:

    def __init__(self, category):
        self.category = category
        self.shifts = []

    def add_shift(self, shift):
        self.shifts.append(shift)
        shift.parent_lesson_block = self
        
    def filter_shifts(self, filter):
        for i in xrange(len(self.shifts)-1, -1, -1): #iterate backwards
            if not self.shifts[i].name in filter :
                self.shifts.pop(i)
                

class Shift:

    def __init__(self, name):
        self.name = name
        self.slots = []

    def add_lesson_slot(self, lesson_slot):
        self.slots.append(lesson_slot)
        lesson_slot.parent_shift = self

class LessonSlot:

    def __init__(self, day, start, end, room, classes):
        self.day = day
        self.start = start
        self.end = end
        self.room = room
        self.classes = classes

    def course_name(self):
        return self.parent_shift.parent_lesson_block.parent_course.name

    def lesson_category(self):
        return self.parent_shift.parent_lesson_block.category

    def overlaps_with(self, other):
        return self.day == other.day and \
               self.start.is_before(other.end) and \
               self.end.is_after(other.start)

class Weekday:
    @staticmethod
    def strrep(weekday):
        dictionary = {
            Weekday.MONDAY : 'Seg',
            Weekday.TUESDAY : 'Ter',
            Weekday.WEDNESDAY : 'Qua',
            Weekday.THURSDAY : 'Qui',
            Weekday.FRIDAY : 'Sex',
            Weekday.SATURDAY : 'Sab'}
        return dictionary[weekday]
    
    @staticmethod
    def allDays():
        return range(0,7)
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

class Time:

    def __init__(self, hour, minute):
        self.minutes = hour * 60 + minute

    def is_before(self, other):
        return self.minutes < other.minutes

    def is_after(self, other):
        return self.minutes > other.minutes
    
    def add(self, other):
        return Time(0,self.minutes + other.minutes)
    
    def increment(self, other):
        self.minutes += other.minutes
        
    def copy(self):
        return Time(0,self.minutes)
    
    def __str__(self):
        return "%d:%02d" % (self.minutes/60, self.minutes%60)

def time_from_str(str):
    if not len(str) == 5 or not str[2] == ":":
        return
    try:
        hour = int(str[0:2])
        minute = int(str[3:5])
    except ValueError:
        return
    if 0 <= hour and hour < 24 and 0 <= minute and minute < 60:
        return Time(hour, minute)
    else:
        return