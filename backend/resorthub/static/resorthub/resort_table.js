function overlay(desc) {    
    el = document.getElementById("overlay");
    document.getElementById("resort_description").innerHTML = desc;
    el.style.visibility = (el.style.visibility == "visible" ) ? "hidden" : "visible";
}

function compare_or_favorite_resorts(compareFlag) {
    alert("I get here");
    let checkboxes = document.getElementsByTagName("input");
    let selected = get_selected_boxes(checkboxes);
    
    if (compareFlag){
        alert("I will perform compare on resorts "+selected);
        return(selected)

    } else {
        alert("I will perform favorite on resorts "+selected);
        window.location.replace('/resorthub/');
    }
}

function get_selected_boxes(checkboxes){
    let selected_boxes = [];
    for (let i=0, len=checkboxes.length; i<len; i++){
            if (checkboxes[i].checked){
                selected_boxes.push(i);
            }   
    }
    return(selected_boxes);
}
