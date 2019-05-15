var url;
var data;
var reponse;
var method;

//Fonction de traitement, après que la requête Ajax

function demande_amis_traitement(reponse){
    var feeback_html = document.getElementById("feedback_demande_ami");
    feeback_html.innerHTML = reponse.feedback;
}


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


//Fonction qui réalise une requête Ajax
//Prend en paramètre la methode, l'url, les données et la fonction à appeler.
function requeteAjax(method,url,data,fonction_succes){
    var xhttp = new XMLHttpRequest();
    xhttp.open(method, url, true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send(data);
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) { //readystate=4 : requête terminé, status=200 : Ok
            reponse = JSON.parse(this.response)
            fonction_succes(reponse);
        }
     };
}

function demande_amis_click(){
    method = "POST";
    url = "/friend/sendto/";
    var inputs = document.getElementsByTagName("input");
    var csrf = "csrfmiddlewaretoken="+inputs.csrfmiddlewaretoken.value;
    var username = document.getElementById('id_demandeUsername').name+"="+document.getElementById('id_demandeUsername').value
    data = csrf+"&"+username;
    requeteAjax(method,url,data,demande_amis_traitement);
}

function recherche_amis_click(){
    method = "POST";
    url = "/friend/search/";
    var inputs = document.getElementsByTagName("input");
    var csrf = "csrfmiddlewaretoken="+inputs.csrfmiddlewaretoken.value;
    var username = document.getElementById('id_rechercheUsername').name+"="+document.getElementById('id_rechercheUsername').value
    data = csrf+"&"+username;
    requeteAjax(method,url,data,recherche_amis_traitement);
}


function accepter_amis(idUser){
    method = "POST";
    url = "/friend/accept/";
    var inputs = document.getElementsByTagName("input");
    var csrf = "csrfmiddlewaretoken="+inputs.csrfmiddlewaretoken.value;
    data = csrf+"&"+"User="+idUser;
    requeteAjax(method,url,data,accepter_amis_traitement);
}

//A TESTER
function supprimer_amis(idUser){
    method = "POST"
    url = "/friend/delete/";
    var inputs = document.getElementsByTagName("input");
    var csrf = "csrfmiddlewaretoken="+inputs.csrfmiddlewaretoken.value;
    data = csrf+"&"+"User="+idUser;
    requeteAjax(method,url,data,supprimer_amis_traitement);
}

document.getElementById("btn_demande_usernameAmis").onclick = demande_amis_click;
document.getElementById("btn_rechercheUsername").onclick = recherche_amis_click;


//-----INVITER

function inviter_amis(idUser,idrencontre){
    method = "POST";
    url = "/game/invitation/new/";
    var inputs = document.getElementsByTagName("input");
    var csrf = "csrfmiddlewaretoken="+inputs.csrfmiddlewaretoken.value;
    id_send = "User="+idUser;
    idrencontre_send = "idRencontre="+idrencontre;
    data = csrf+"&"+id_send+"&"+idrencontre_send;
    requeteAjax(method,url,data,inviter_amis_traitement);
}

function accepter_invit(idrencontre){
    method = "POST";
    url = "/game/invitation/accept/";
    var inputs = document.getElementsByTagName("input");
    var csrf = "csrfmiddlewaretoken="+inputs.csrfmiddlewaretoken.value;
    idrencontre_send = "idRencontre="+idrencontre;
    data = csrf+"&"+idrencontre_send;
    requeteAjax(method,url,data,reponse_invit_traitement);
}

//A TESTER
function rejeter_invit(idJoueur,idrencontre){
    method = "POST"
    url = "/game/invitation/reject/";
    var inputs = document.getElementsByTagName("input");
    var csrf = "csrfmiddlewaretoken="+inputs.csrfmiddlewaretoken.value;
    id_send = "User="+idJoueur;
    idrencontre_send = "idRencontre="+idrencontre;
    data = csrf+"&"+id_send+"&"+idrencontre_send;
    reponse = requeteAjax(method,url,data,reponse_invit_traitement);
}

//A TESTER
function annuler_invit(idJoueur,idrencontre){
    method = "POST"
    url = "/game/invitation/cancel/";
    var inputs = document.getElementsByTagName("input");
    var csrf = "csrfmiddlewaretoken="+inputs.csrfmiddlewaretoken.value;
    id_send = "User="+idJoueur;
    idrencontre_send = "idRencontre="+idrencontre;
    data = csrf+"&"+id_send+"&"+idrencontre_send;
    reponse = requeteAjax(method,url,data,reponse_invit_traitement);
}
