function overlay(desc) {    
    el = document.getElementById("overlay");
    document.getElementById("resort_description").innerHTML = desc;
    el.style.visibility = (el.style.visibility == "visible" ) ? "hidden" : "visible";
}
