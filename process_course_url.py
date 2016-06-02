import sys
import urllib
from tt_parser import *
from tt_generator import *
from tt_prettyprinter import *

course_id = int(sys.argv[1])
url = urllib.unquote(sys.argv[2])

parser = HTMLCourseParser(url)
course = parser.parse()

html_result = "<div id='coursediv" + str(course_id) + "' >"
html_result += "<img src='line.png' />"
html_result += "<h1 class='mtop0 mbottom03 cnone' style='font-size: 14px'><a target='_blank' href='%s'>%s</a>" % (course.url, course.long_name)
html_result += "<span class='greytxt' style='font-size: 10px;'> (%s)</span>" % (course.name)
html_result += "&nbsp&nbsp<img src='remove.png' onclick='removeCourse(coursediv" + str(course_id) + ")' />"
html_result += "</h1>"
html_result += "<input type='hidden' name='course%i' value='%s'>" \
               % (course_id, course.url)

block_id = 0
sorted_blocks = sorted(course.lesson_blocks, key=lambda x: x.category, reverse=True)
for block in sorted_blocks:
    block_id += 1
    html_result += "<p>" #DEV Estetica!
    html_result += '<span style="diplay: block; float: left; width: 50px">'
    html_result += "<input onchange='courseTypeChange(\"course%itype%i\")' type='checkbox' name='course%itype%i' value='%s'  checked>%s&nbsp;" \
                   % (course_id, block_id, course_id, block_id, block.category, block.category)
    html_result += "</span><span id ='course%itype%i'>" % (course_id, block_id)
    option_id = 0
    block.shifts.sort(key=lambda shift: shift.name)
    for shift in block.shifts: #shift checkboxes:
        option_id += 1
        label =  ""
        #sort slots
        shift.slots.sort(key= lambda x: x.day)
        for slot in shift.slots:
            label += "%s %s %s %s&#013;" % (Weekday.strrep(slot.day), slot.start, slot.end, slot.room)
        html_result += "<span title= '%s'><input type='checkbox' name='course%itype%ioption%i' value='%s' checked>%s&nbsp;</span>" \
                       % (label, course_id, block_id, option_id,shift.name, shift.name[-2:])
    html_result += "</span></p>"

html_result += "</div>"

print html_result
