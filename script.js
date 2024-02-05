function buttonSendAction(){
    const textFenster = document.getElementById("chatTextArea");
    const eingabeFester = document.getElementById("chatTextEingabe");
    
    var eingabeText = eingabeFester.value;
    textFenster.innerHTML = eingabeText;
    eingabeFester.value = "";
}