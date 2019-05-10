

function demande_amis(){
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/friend/sendto/", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    var inputs = document.getElementsByTagName("input");
    var csrf = "csrfmiddlewaretoken="+inputs.csrfmiddlewaretoken.value;
    var username = document.getElementById('id_demande_usernameAmis').name+"="+document.getElementById('id_demande_usernameAmis').value
    var data = csrf+"&"+username;

    console.log(data)
    xhttp.send(data);
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) { //readystate=4 : requête terminé, status=200 : Ok
            var reponse = JSON.parse(this.response)
            console.log(reponse.feedback);
        }
     };
}