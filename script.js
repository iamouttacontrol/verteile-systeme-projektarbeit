var nickname;
var chosenlanguage = "de";

function buttonSendAction(){
    const textFenster = document.getElementById("chatTextArea");
    const eingabeFester = document.getElementById("chatTextEingabe");
    
    var eingabeText = eingabeFester.value;
    textFenster.innerHTML = eingabeText;
    eingabeFester.value = "";

    //JSON String absenden
    const chatnachricht = {
        name: nickname,
        message: eingabeText,
        language: chosenlanguage
    }

    const messageAsJsonString = JSON.stringify(chatnachricht);

    textFenster.innerHTML = messageAsJsonString;

}

function buttonNicknameSave(){
    const nicknameEingabe = document.getElementById("nicknameArea");
    nickname = nicknameEingabe.value;
    nicknameEingabe.readOnly = true;
}

function dropdownLanguageChange(){
    
}