let savedNickname;
let chosenlanguage = "de";

const socket = new WebSocket("ws://localhost:9000");

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
    data = JSON.stringify(chatnachricht);
    
    socket.send(data)
}

function test() {
    
    // Connection opened
    socket.addEventListener("open", (event) => {
        //var data = JSON.stringify({"lang":"data"});
        data="test"
        console.log(data);
        socket.send(data);
    });

    
    // Listen for messages
    socket.addEventListener("message", (event) => {
        console.log("Message from server ", event.data);
        document.getElementById("chatTextArea").innerHTML = event.data;
    });

    
        
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