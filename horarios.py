import sys
import urllib
from tt_parser import *
from tt_generator import *
from tt_prettyprinter import *
from tt_errorprinter import *
from tt_conditions import *

def is_url(arg):
    return arg[0:4] == "http"
    
def is_shiftId(arg, block):
    split1 = len(block.parent_course.name)
    split2 = split1 + len(block.category)
    return arg[0: split1] == block.parent_course.name and arg[split1 : split2] == block.category and arg[split2:].isdigit()
    
def is_limit_id(arg):
    return arg in ["ll", "ul", "it", "fd"]
    
def is_limit_scope(arg):
    return arg in ["scd", "snd"]

    
def create_day_list(args):
    days = []
    for arg in args:
        weekday = parse_day(day)
        if weekday:
            days.append() 
        else:
            return
    return days
    
def create_time_limit(args):
    if len(args) == 1:
        return  time_from_str(args[0])
        
def create_time_interval(args):
    if len(args) == 3:
        result=[]
        for arg in args:
            time = time_from_str(arg)
            if time:
                result.append(time)
            else:
                return
        if not (result[1].add(result[0])).is_after(result[2]):
            return result
    
    
def make_condition(limit_id, limit_args, scope_id, scope_args): #DEV TODO
    if "scd" == scope_id:
        days = []
        for arg in scope_args:
            weekday = parse_day(arg)
            if not weekday is None:
                days.append(weekday) 
            else:
                return
        #
        if "ll" == limit_id:
            time = create_time_limit(limit_args)
            if time:
                return LowerLimitCDays(days, time)
        
        elif "ul" == limit_id:
            time = create_time_limit(limit_args)
            if time:
                return UpperLimitCDays(days, time)
        
        elif "it" == limit_id:
            time = create_time_interval(limit_args)
            if time:
                return IntervalCDays(days, time[1], time[2], time[0])
        
        elif "fd" == limit_id:
            if not limit_args:
                return FreeCDays(days)
        else:
            return
        
    elif "snd" == scope_id:
        if 1 ==len(scope_args):
            try:
                days = int(scope_args[0])
                #days+=1#sunday is NOT considered by the generator
            except ValueError:
                return
        else:
            return
        
        if "ll" == limit_id:
            time = create_time_limit(limit_args)
            if time:
                return LowerLimitNDays(days, time)
        
        elif "ul" == limit_id:
            time = create_time_limit(limit_args)
            if time:
                return UpperLimitNDays(days, time)
        
        elif "it" == limit_id:
            time = create_time_interval(limit_args)
            if time:
                return IntervalNDays(days, time[1], time[2], time[0])
        
        elif "fd" == limit_id:
            if not limit_args:
                return FreeNDays(days)
        else:
            return
    else:
        return

def conditionFactory(description):
    descriptors = description.split()
    size = len(descriptors)
    if size < 1 or not is_limit_id(descriptors[0]):
        return
    i = 1
    while not is_limit_scope(descriptors[i]) and i < size:
        i+= 1
    if i >= size-1:
        return
    return make_condition(descriptors[0], descriptors[1:i], descriptors[i], descriptors[i+1:])

    
#main

lesson_blocks = []
nArgs = len(sys.argv)
error_processing_args = False
i = 1
arg = urllib.unquote(sys.argv[i])
condition_list = []
while i< nArgs:#each arg is one filter
    arg = urllib.unquote_plus(sys.argv[i])
    if is_url(arg):
        break
    condition = conditionFactory(arg)
    if condition :
        condition_list.append(condition)
    else:
        error_processing_args = True
    i += 1
    
while i < nArgs:
    arg = urllib.unquote(sys.argv[i])
    if is_url(arg):
        current_course = HTMLCourseParser(arg).parse()
        i += 1
    else:
        current_block = current_course.get_block_by_category(arg)
        lesson_blocks.append(current_block)
        i+=1
        chosen_shifts = []
        while i < nArgs and is_shiftId(sys.argv[i], current_block):
            chosen_shifts.append(sys.argv[i])
            i+=1
        lesson_blocks[-1].filter_shifts(chosen_shifts)


generator = TimetableGenerator(condition_list, 100) #add control over number of timetables? (make sure to have a maximum)
generator.generate_timetables(lesson_blocks)

generator.generated.sort(key=Timetable.total_time)

if generator.generated:
    printer = HTMLPrettyPrinter()
    printer.print_timetables(generator.generated, generator.total_combinations)
else:
    printer = HTMLErrorPrinter()
    printer.print_no_timetables()
