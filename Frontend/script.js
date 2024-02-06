let savedNickname;
let chosenlanguage = "de";

function buttonSendAction(){
    const textFenster = document.getElementById("chatTextArea");
    const eingabeFester = document.getElementById("chatTextEingabe");
    
    let eingabeText = eingabeFester.value;
    textFenster.innerHTML = eingabeText;
    eingabeFester.value = "";

    const now = new Date();
    
    const aktuelleHour = now.getHours();
    const aktuelleMinutes = now.getMinutes(); 
    const aktuelleSeconds = now.getSeconds();
    
    let timestamp = `${aktuelleHour}:${aktuelleMinutes}:${aktuelleSeconds}`;
    
    //JSON String bilden
    const chatnachricht = {
        nickname: savedNickname,
        message: eingabeText,
        timestamp: timestamp,
        language: chosenlanguage
    }
    textFenster.innerHTML = JSON.stringify(chatnachricht);
}

function buttonNicknameSave(){
    const nicknameEingabe = document.getElementById("nicknameArea");
    savedNickname = nicknameEingabe.value;
    nicknameEingabe.readOnly = true;
    nicknameEingabe.style.backgroundColor = "grey";
}

function selectLanguageChange(){
    const selectLanguage = document.getElementById("dropdownOptions");
    chosenlanguage = selectLanguage.value;
}