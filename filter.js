var filterCount = 0;
var weekday = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"];

function detectTimeSupport(){
    var i = document.createElement("input");
    i.setAttribute("type", "time");
    return i.type !== "text";
}

function fixUnsupportedTime(e){
    if(!detectTimeSupport()){
        var u = document.getElementById("FilterDiv");
        var inputList= u.getElementsByTagName("INPUT");
        for( var i = inputList.length -1; i >= 0; i--){
            if("time" == inputList[i].getAttribute("type")){
                inputList[i].value = "hh:mm";
            }
        }
    }
}

  function createFilterEntry(userView, machineView){
    result = '<div id="filterdiv';
    result+= filterCount;
    result+= '"><h1 style="font-size: 12px">';
    result += userView;
    result += '&nbsp;<img src="remove.png" onclick="removeCourse(filterdiv';
    result += filterCount;
    result += ')"></h1><input type="hidden" name="afilter';
    result += filterCount;
    result += '" value="';
    result += machineView;
    result += '"></div>';
    filterCount++;
    
    document.getElementById("filters").innerHTML += result;
  }
  
  //Process input
  function isTime(time){ //string: time
    if(time.length != 5 || time[2] != ':')
        return false;
    var hours = time.substring(0,2);
    var minutes = time.substring(3,5);
    if  (isNaN(hours) || isNaN(minutes))
        return false;
    return true;
  }
  
  function getTimeLimit(optionSet){ // returns the data in the timeLimit option set
    var res =  optionSet.getElementsByTagName("INPUT")[0].value.substring(0, 5);
    if( isTime(res) )
        return res;
    else
        return;
  }
  
  function getIntervalData(optionSet){
   var elements = optionSet.getElementsByTagName("INPUT");
    var data = [];
    for (var max = 3, i = 0; i < max; i++){
        time = elements[i].value.substring(0, 5);
        if( ! isTime(time))
            return;
        data.push(time);
    }
    return data;
  }
  
  //Create filters: function(OptionSet)
  function createLLimit(optionSet){
    input = getTimeLimit(optionSet);
    if (!input)
      return;
    return ["Hora mínima "+ input + " ", "ll "+ input + " "];
  }
  function createULimit(optionSet){
    input = getTimeLimit(optionSet);
    if (!input)
      return;
    return ["Hora máxima "+ input + " ", "ul "+ input + " "];
  }
  function createInterval(optionSet){
    data = getIntervalData(optionSet);
    if(!data)
        return;
    return ["Intervalo de duração " + data[0] + " entre as " + data[1] + " e as " + data[2] + " ", "it " + data[0] + " "+ data[1] + " "+ data[2] + " "];
  }
  
  function createFreeDay(OptionSet){
    return ["Dia livre ", "fd "];
  }
  
  function createChosenDays(optionSet){
    inputDays = optionSet.children;
    var result = "";
    
    for(var max = inputDays.length, i = 0; i < max; i++){
        if (inputDays[i].checked == true)
            result += weekday[i] + " ";
    }
    if (result == "")
        return;
    return ["nos dias: " + result, "scd "+ result ];
  }
  
  function createNumberDays(optionSet){
    var nDays = optionSet.getElementsByTagName("INPUT")[0].value;
    if( !(!isNaN(nDays) && nDays > 0 && nDays < 7))
        return;
    return ["em "+ nDays + " dias ", "snd "+ nDays + " "];
  }
  
  function createAllDays(OptionSet){
      return ["em todos os dias ", "snd "+ 6 + " "];
  }
  
  //Options to show depending on the chosen type of limit
  var dictOption = { "LLimit":"TimeLimit", "ULimit": "TimeLimit", "Interval": "Interval", "FreeDay":"FreeDay"};
  //Factory (functions) for each possbile option
  var dictCreate = { "LLimit":createLLimit, "ULimit": createULimit, "Interval": createInterval, "FreeDay": createFreeDay, "ChosenDays":createChosenDays, "nDays": createNumberDays, "allDays": createAllDays };
  //Options to show depending on the chosen scope of limit
  var dictScope = { "ChosenDays":"chosenDays", "nDays": "numberDays", "allDays":"allDays" };
  
  //Interface
  function changeOptionSet(selected, optionSetParent){
    var OptionSets = optionSetParent.children;
    for(var i = OptionSets.length -1; i>= 0; i--){
        if(OptionSets[i].className == "OptionSet"){
          if (OptionSets[i].id == selected)
            OptionSets[i].style.display = "inline";
          else
            OptionSets[i].style.display = "none";
        }
    }
  }
  
  function changeFilterOptions(){
    var selected = dictOption[FilterType.options[FilterType.selectedIndex].value];
    if(selected == "FreeDay")
        FilterSelectType();
    changeOptionSet(selected, FilterOptions);
  }
  
  function changeFilterScopeOptions(){
    var selected = dictScope[FilterScope.options[FilterScope.selectedIndex].value];
    console.log(selected);
    if(selected == "allDays")
        FilterSelectTime();
    changeOptionSet(selected, ScopeOptions);
  }
  
  function filterClear(){
    var inputs = document.getElementById("FilterInput").getElementsByTagName("INPUT");
    
    for (var max = inputs.length, i = 0; i < max; i++){
        inputs[i].value = "";
        inputs[i].checked = false;
    }
    
    FilterType.selectedIndex = "-1";
    FilterScope.selectedIndex = "-1";
    changeOptionSet(null, FilterOptions);
    changeOptionSet(null, ScopeOptions);
    
    fixUnsupportedTime();
    
    document.getElementById("FilterSelect1").style.display = "none";
    document.getElementById("FilterSelect2").style.display = "none";
    document.getElementById("FilterSelect3").style.display = "none";
    return;
  }
  
  function filterStart(){
    document.getElementById("FilterSelect1").style.display = "block";
  }
  
  
  function FilterSelectType(){
    document.getElementById("FilterSelect2").style.display = "block";
  }
  
  function FilterSelectTime(){
    document.getElementById("FilterSelect3").style.display = "block";
  }
  
  //Process Filter
function processFilter(){
    var filter = FilterType.options[FilterType.selectedIndex].value //Id of the chosen option
    var options = document.getElementById(dictOption[filter]); //Html element with the settings 
    var data = dictCreate[filter](options);
    if (!data)
        return;
    var scope = FilterScope.options[FilterScope.selectedIndex].value
    var options = document.getElementById(dictScope[scope]);
    var data2  = dictCreate[scope](options);
    if (!data2)
        return;
    data[0] += data2[0];
    data[1] += data2[1];
    createFilterEntry(data[0], data[1]);
    
    filterClear();
}

window.onload = filterClear;