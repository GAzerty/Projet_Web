

function demande_amis(){
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/friend/sendto", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    var inputs = document.getElementsByTagName("input");

    var csrf = "csrfmiddlewaretoken="+inputs.csrfmiddlewaretoken.value;
    var username;  //Recupere la value via getbyID de input
    var data = csrf+"&"+username;
    xhttp.send(data);
}