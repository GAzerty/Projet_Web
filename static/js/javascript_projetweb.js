var url;
var data;
var reponse;

function demande_amis_traitement(reponse){
    var feeback_html = document.getElementById("feedback");
    feeback_html.innerHTML = reponse.feedback;
}

//Résoudre le problème de value avec input
function recherche_amis_traitement(reponse){
    var feeback_html = document.getElementById("feedback");
    feeback_html.innerHTML = reponse.feedback;
}

function accepter_amis_traitement(reponse){
    var feeback_html = document.getElementById("feedback");
    feeback_html.innerHTML = reponse.feedback;
}

function supprimer_amis_traitement(reponse){
    var feeback_html = document.getElementById("feedback");
    feeback_html.innerHTML = reponse.feedback;
}

function requeteAjax(url,data,fonction_succes){
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    console.log(data)
    xhttp.send(data);
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) { //readystate=4 : requête terminé, status=200 : Ok
            reponse = JSON.parse(this.response)
            fonction_succes(reponse);
        }
     };
}

function demande_amis_click(){
    url = "/friend/sendto/";
    var inputs = document.getElementsByTagName("input");
    var csrf = "csrfmiddlewaretoken="+inputs.csrfmiddlewaretoken.value;
    var username = document.getElementById('id_demande_usernameAmis').name+"="+document.getElementById('id_demande_usernameAmis').value
    data = csrf+"&"+username;
    requeteAjax(url,data,demande_amis_traitement);
}

function recherche_amis_click(){
    url = "/friend/search/";
    var inputs = document.getElementsByTagName("input");
    var csrf = "csrfmiddlewaretoken="+inputs.csrfmiddlewaretoken.value;
    var username = document.getElementById('id_rechercheUsername').name+"="+document.getElementById('id_rechercheUsername').value
    data = csrf+"&"+username;
    requeteAjax(url,data,demande_amis_traitement);
}


function accepter_amis(username){
    url = "/friend/accept/";
    var inputs = document.getElementsByTagName("input");
    var csrf = "csrfmiddlewaretoken="+inputs.csrfmiddlewaretoken.value;
    data = csrf+"&"+"username_sender="+username;
    requeteAjax(url,data,accepter_amis_traitement);
}

function supprimer_amis(username){
    url = "/friend/delete/";
    var inputs = document.getElementsByTagName("input");
    var csrf = "csrfmiddlewaretoken="+inputs.csrfmiddlewaretoken.value;
    data = csrf+"&"+"username="+username;
    requeteAjax(url,data,supprimer_amis_traitement);
}

document.getElementById("btn_demande_usernameAmis").onclick = demande_amis_click;
document.getElementById("btn_rechercheUsername").onclick = recherche_amis_click;

