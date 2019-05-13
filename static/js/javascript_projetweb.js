var url;
var data;
var reponse;
var method;


function demande_amis_traitement(reponse){
    var feeback_html = document.getElementById("feedback_demande_ami");
    feeback_html.innerHTML = reponse.feedback;
}

//Résoudre le problème de value avec input
function recherche_amis_traitement(reponse){
    var feeback_html = document.getElementById("feedback_recherche_ami");
    feeback_html.innerHTML = reponse.feedback;
    if(reponse.succes){
        document.getElementById('id_demandeUsername').value=reponse.username;
    }
}

function accepter_amis_traitement(reponse){
    document.location.reload(true);
    var feeback_html = document.getElementById("feedback");
    feeback_html.innerHTML = reponse.feedback;
}

function supprimer_amis_traitement(reponse){
    document.location.reload(true);
    var feeback_html = document.getElementById("feedback_mesamis");
    feeback_html.innerHTML = reponse.feedback;
}

function inviter_amis_traitement(reponse){
    var feeback_html = document.getElementById("feedback");
    feeback_html.innerHTML = reponse.feedback;
}

function reponse_invit_traitement(reponse){
    document.location.reload(true);
    var feeback_html = document.getElementById("feedback_demande_reçue");
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
    var username = document.getElementById('id_demandeUsername').name+"="+document.getElementById('id_demandeUsername').value
    data = csrf+"&"+username;
    requeteAjax(url,data,demande_amis_traitement);
}

function recherche_amis_click(){
    url = "/friend/search/";
    var inputs = document.getElementsByTagName("input");
    var csrf = "csrfmiddlewaretoken="+inputs.csrfmiddlewaretoken.value;
    var username = document.getElementById('id_rechercheUsername').name+"="+document.getElementById('id_rechercheUsername').value
    data = csrf+"&"+username;
    requeteAjax(url,data,recherche_amis_traitement);
}


function accepter_amis(idUser){
    url = "/friend/accept/";
    var inputs = document.getElementsByTagName("input");
    var csrf = "csrfmiddlewaretoken="+inputs.csrfmiddlewaretoken.value;
    data = csrf+"&"+"User="+idUser;
    requeteAjax(url,data,accepter_amis_traitement);
}

function supprimer_amis(idUser){
    method = "DELETE"
    url = "/friend/delete/";
    var inputs = document.getElementsByTagName("input");
    var csrf = "csrfmiddlewaretoken="+inputs.csrfmiddlewaretoken.value;
    data = csrf+"&"+"User="+idUser;
    requeteAjax(url,data,supprimer_amis_traitement);
}

document.getElementById("btn_demande_usernameAmis").onclick = demande_amis_click;
document.getElementById("btn_rechercheUsername").onclick = recherche_amis_click;


//-----INVITER

function inviter_amis(idUser,idrencontre){
    url = "/rencontre/inviter/";
    var inputs = document.getElementsByTagName("input");
    var csrf = "csrfmiddlewaretoken="+inputs.csrfmiddlewaretoken.value;
    id_send = "User="+idUser;
    idrencontre_send = "idRencontre="+idrencontre;
    data = csrf+"&"+id_send+"&"+idrencontre_send;
    requeteAjax(url,data,inviter_amis_traitement);
}

function accepter_invit(idrencontre){
    url = "/rencontre/invitation/accept";
    var inputs = document.getElementsByTagName("input");
    var csrf = "csrfmiddlewaretoken="+inputs.csrfmiddlewaretoken.value;
    idrencontre_send = "idRencontre="+idrencontre;
    data = csrf+"&"+idrencontre_send;
    requeteAjax(url,data,reponse_invit_traitement);
}

function rejeter_invit(idJoueur,idrencontre){
    method = "DELETE"
    url = "/rencontre/invitation/rejeter";
    var inputs = document.getElementsByTagName("input");
    var csrf = "csrfmiddlewaretoken="+inputs.csrfmiddlewaretoken.value;
    id_send = "User="+idJoueur;
    idrencontre_send = "idRencontre="+idrencontre;
    data = csrf+"&"+id_send+"&"+idrencontre_send;
    reponse = requeteAjax(url,data,reponse_invit_traitement);
}

function annuler_invit(idJoueur,idrencontre){
    method = "DELETE"
    url = "/rencontre/invitation/annuler";
    var inputs = document.getElementsByTagName("input");
    var csrf = "csrfmiddlewaretoken="+inputs.csrfmiddlewaretoken.value;
    id_send = "User="+idJoueur;
    idrencontre_send = "idRencontre="+idrencontre;
    data = csrf+"&"+id_send+"&"+idrencontre_send;
    reponse = requeteAjax(url,data,reponse_invit_traitement);
}

//accepter_invit et rejeter_invit ont certainement les mêmes fonctions de traitement - A FAIRE