let savedNickname;
let chosenlanguage = "de";

function buttonSendAction(){
    const textFenster = document.getElementById("chatTextArea");
    const eingabeFester = document.getElementById("chatTextEingabe");
    
    let eingabeText = eingabeFester.value;
    textFenster.innerHTML = eingabeText;
    eingabeFester.value = "";

    //JSON String bilden
    const chatnachricht = {
        nickname: savedNickname,
        message: eingabeText,
        language: chosenlanguage
    }
    textFenster.innerHTML = JSON.stringify(chatnachricht);
}

function buttonNicknameSave(){
    const nicknameEingabe = document.getElementById("nicknameArea");
    savedNickname = nicknameEingabe.value;
    nicknameEingabe.readOnly = true;
}

function selectLanguageChange(){
    const selectLanguage = document.getElementById("dropdownOptions");
    chosenlanguage = selectLanguage.value;
}