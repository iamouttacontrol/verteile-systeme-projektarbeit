let savedNickname;
let chosenlanguage = "de";

const socket = new WebSocket("ws://localhost:9000");

function buttonSendAction() {
    const eingabeFenster = document.getElementById("chatTextEingabe");

    let eingabeText = eingabeFenster.value;
    // Entfernen Sie jede direkte Anzeige im Chatfenster hier.
    eingabeFenster.value = ""; // Eingabefeld leeren

    const now = new Date();

    const aktuelleStunde = now.getHours();
    const aktuelleMinute = now.getMinutes();
    const aktuelleSekunde = now.getSeconds();

    let timestamp = `${aktuelleStunde}:${aktuelleMinute}:${aktuelleSekunde}`;

    // JSON String bilden
    const chatnachricht = {
        username: savedNickname,
        message: eingabeText,
        timestamp: timestamp,
        language: chosenlanguage
    };
    let data = JSON.stringify(chatnachricht);

    socket.send(data);
}

function test() {

    // Connection opened
    socket.addEventListener("open", (event) => {
        var data = JSON.stringify({"username":"test","message":"test message","timestamp":"14:42:21","language":chosenlanguage});
        //data = "test"
        //console.log(data);
        //socket.send(data);
    });


    socket.addEventListener("message", (event) => {
        console.log("Message from server ", event.data);
        const chatTextArea = document.getElementById("chatTextArea");
        // Parsen der empfangenen JSON-Nachricht
        const empfangeneNachricht = JSON.parse(event.data);

        // Formatierung der Nachricht: "nickname: nachricht (timestamp)"
        const formatierteNachricht = `(${empfangeneNachricht.timestamp}) ${empfangeneNachricht.nickname}: ${empfangeneNachricht.message}`;

        // Hinzufügen der formatierten Nachricht zum Chatfenster, mit Zeilenumbruch für jede neue Nachricht
        chatTextArea.value += (chatTextArea.value ? "\n" : "") + formatierteNachricht;
        scrollToBottom();
    });
}

function buttonNicknameSave() {
    const nicknameEingabe = document.getElementById("nicknameArea");
    savedNickname = nicknameEingabe.value;
    nicknameEingabe.readOnly = true;
    nicknameEingabe.style.backgroundColor = "blue";
}

function selectLanguageChange() {
    const selectLanguage = document.getElementById("dropdownOptions");
    chosenlanguage = selectLanguage.value;
}

function scrollToBottom() {
    const chatTextArea = document.getElementById("chatTextArea");
    chatTextArea.scrollTop = chatTextArea.scrollHeight; // Scrollt zum unteren Rand
}
//mit enter absenden