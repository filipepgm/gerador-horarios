from tt_generator import *

#Condition: check(tt, shift)
#It is always assumed that tt already respects the condition

#in how many days is condition met
#is condition met on x days

class FreeNDays:
    def __init__(self, nDays):
        self.nDays = nDays
    def check(self, tt, shift):
        busy_days = []
        for weekday in tt.lessons:
            if tt.lessons[weekday]:
               busy_days.append(weekday)
        for slot in shift.slots:
            if not slot.day in busy_days:
                busy_days.append(slot.day)
        if len(busy_days) > 6- self.nDays:
            return False
        else:
            return True
            
class FreeCDays:
    def __init__(self, chosen_days):
        self.free_days = chosen_days  
    def check(self, tt, shift):
        for slot in shift.slots:
            if slot.day in self.free_days:
                return False
        return True


class Interval :
    def __init__(self, lowerLimit, upperLimit, lenght):
        self.lowerLimit = lowerLimit
        self.upperLimit = upperLimit
        self.lenght = lenght

    def slotOutOfBounds(self, slot, lowerLimit, upperLimit):
        return not slot.end.is_after(lowerLimit) or not slot.start.is_before(upperLimit)

    def slotOutOfLimits(self, slot):
        return self.slotOutOfBounds(slot, self.lowerLimit, self.upperLimit)
    
    def check_day(self, weekday, tt, slot_list):
        time_increment = Time(0,30)
        start = self.lowerLimit.copy()
        end = start.add(self.lenght)
        
        while not end.is_after(self.upperLimit):
            bOk = True
            for slot in tt.lessons[weekday]:
                if not self.slotOutOfBounds(slot, start, end):
                    bOk = False
                    break
            if not bOk:
                start.increment(time_increment)
                end.increment(time_increment)
                continue
            for slot in slot_list:
                if slot.day == weekday and not self.slotOutOfBounds(slot, start, end):
                    bOk = False
                    break
            if not bOk:
                start.increment(time_increment)
                end.increment(time_increment)
            else:
                return True
        return False

class IntervalCDays(Interval):
    def __init__(self, chosen_days, lowerLimit, upperLimit, lenght):
        Interval.__init__(self, lowerLimit, upperLimit, lenght)
        self.valid_days = chosen_days
        
    def slotOutOfLimits(self, slot):
        return not (slot.day in self.valid_days) or Interval.slotOutOfLimits(self, slot)
        
    def check(self, tt, shift):
        slot_of_interest = []
        days_to_check = []
        #add days to check. Other days are assumed to respect the condition
        for slot in shift.slots:
            if not self.slotOutOfLimits(slot):
                slot_of_interest.append(slot)
                if not slot.day in days_to_check:
                    days_to_check.append(slot.day)
                    
        for weekday in days_to_check:
            if not self.check_day(weekday, tt, slot_of_interest):
                return False
        return True
        
class IntervalNDays(Interval):
    def __init__(self, nDays, lowerLimit, upperLimit, lenght):
        Interval.__init__(self, lowerLimit, upperLimit, lenght)
        self.nDays = nDays

    def check(self, tt, shift):
        slot_of_interest = []
        nOk_days = 7
        for slot in shift.slots:
            if not self.slotOutOfLimits(slot):
                slot_of_interest.append(slot)
        
        if not slot_of_interest:
            return True
        for weekday in range(Weekday.MONDAY, Weekday.SUNDAY):
            if not self.check_day(weekday, tt, slot_of_interest):
                nOk_days-=1
                if nOk_days < self.nDays:
                    return False
        return True

#limit any x days
class LimitDays:
    def __init__(self, nDays, time):
        self.limit = time
        self.nDays = nDays
    
    def slotInLimit(self, slot):
        raise NotImplementedError("Abstract method")
    
    def check(self, tt, shift):
        validDays = range(Weekday.MONDAY, Weekday.SUNDAY) #days where the condition is met
        nLenght = len(validDays)
        bOutOfLimits = False
        for slot in shift.slots:
            if slot.day in validDays :
                if not self.slotInLimit(slot):
                    bOutOfLimits = True
                    validDays.remove(slot.day)
        if not bOutOfLimits: #if none of the new slots fail the condition, tt will be as valid as it was before
            return True
        for i in xrange(len(validDays) -1, -1, -1):
            weekday = validDays[i]
            for slot in tt.lessons[weekday]: #check how many days meet the condition
                if not self.slotInLimit(slot):
                    validDays.remove(slot.day)
                    break

        if len(validDays) < self.nDays:
            return False
        else:
            return True
            
class LowerLimitNDays(LimitDays):
    def __init__(self,nDays, time):
        LimitDays.__init__(self,nDays, time)
    
    def slotInLimit(self, slot):
        return not slot.start.is_before(self.limit)

class UpperLimitNDays(LimitDays):
    def __init__(self,nDays, time):
        LimitDays.__init__(self,nDays, time)
    
    def slotInLimit(self, slot):
        return not slot.end.is_after(self.limit)
        
        
class LimitCDays:
    def __init__(self, chosen_days, limit):
        self.limit = limit
        self.chosen_days = chosen_days
        
    def slotInLimit(self, slot, time):
        raise NotImplementedError("Abstract method")
        
    def check(self, tt, shift):
        for slot in shift.slots:
            if slot.day in self.chosen_days :
                if not self.slotInLimit(slot, self.limit):
                    return False
        return True

class LowerLimitCDays(LimitCDays):
    def __init__(self,chosen_days, limit):
        LimitCDays.__init__(self, chosen_days, limit)
    
    def slotInLimit(self, slot, time):
        return not slot.start.is_before(time)

class UpperLimitCDays (LimitCDays):
    def __init__(self,chosen_days, limit):
        LimitCDays.__init__(self,chosen_days, limit)
    
    def slotInLimit(self, slot, time):
        return not slot.end.is_after(time)