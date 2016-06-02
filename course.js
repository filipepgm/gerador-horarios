var courseCount = 0;

function showErrorMessage() { document.getElementById("errorMessage").style.visibility = "visible" }
function hideErrorMessage() { document.getElementById("errorMessage").style.visibility = "hidden" }

function processCourseURL() {
if (courseURL.value == '')
  return
var xmlhttp = new XMLHttpRequest();
xmlhttp.onreadystatechange = function() {
  if (xmlhttp.readyState==4 && xmlhttp.status==200) {
    if (xmlhttp.responseText == '')
      showErrorMessage();
    else {
      hideErrorMessage();
      document.getElementById("courseURL").value = "";
      document.getElementById("courses").innerHTML += xmlhttp.responseText;
    }
  }
}

courseCount++;
var encodedURL = encodeURIComponent(document.getElementById("courseURL").value);
xmlhttp.open("POST", "process_course_url.php", true);
xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
xmlhttp.send("course_id="+courseCount + "&url="+encodedURL);
}

function removeCourse(course) { course.innerHTML = "" }

function courseTypeChange(modifiedType){
    checks = document.getElementById(modifiedType).children;
    for (var i = checks.length -1; i >= 0; i--){
        checks[i].children[0].disabled = !checks[i].children[0].disabled;
    }
}