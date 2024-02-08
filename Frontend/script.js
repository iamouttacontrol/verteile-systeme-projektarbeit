let savedNickname;
let chosenlanguage = "de";

const socket = new WebSocket("wss://virtualmeet.social:9000");


function buttonSendAction() {
    const eingabeFenster = document.getElementById("chatTextEingabe");

    let eingabeText = eingabeFenster.value;

    if(eingabeText === '' || savedNickname ==='') {
        alert("Bitte Nachricht eingeben!")
    }else {

        // Entfernen Sie jede direkte Anzeige im Chatfenster hier.
        eingabeFenster.value = ""; // Eingabefeld leeren

        const now = new Date();

        const aktuelleStunde = now.getHours();
        const aktuelleMinute = now.getMinutes();
        const aktuelleSekunde = now.getSeconds();

        let timestamp = `${aktuelleStunde}:${aktuelleMinute}:${aktuelleSekunde}`;

        // JSON String bilden
        const chatnachricht = {
            nickname: savedNickname,
            message: eingabeText,
            timestamp: timestamp,
            language: chosenlanguage
        };
        let data = JSON.stringify(chatnachricht);


        document.getElementById("chatTextArea").innerHTML = data;
        socket.send(data);
    }
}

function establishConnection() {

    // Connection opened
    socket.addEventListener("open", (event) => {
        //var data = JSON.stringify({"lang":"data"});
        data = "test"
        console.log(data);
        socket.send(JSON.stringify(data));
    });


    socket.addEventListener("message", (event) => {
        console.log("Message from server ", event.data);
        const chatTextArea = document.getElementById("chatTextArea");
        // Parsen der empfangenen JSON-Nachricht
        const empfangeneNachricht = JSON.parse(event.data);

        // Formatierung der Nachricht: "nickname: nachricht (timestamp)"
        const formatierteNachricht = `(${empfangeneNachricht.timestamp}) ${empfangeneNachricht.username}: ${empfangeneNachricht.message}`;

        // Hinzufügen der formatierten Nachricht zum Chatfenster, mit Zeilenumbruch für jede neue Nachricht
        chatTextArea.value += (chatTextArea.value ? "\n" : "") + formatierteNachricht;
        scrollToBottom();
    });
}
function buttonNicknameSave() {

    const nicknameEingabe = document.getElementById("nicknameArea");

    if(nicknameEingabe.value === ''){
        alert("Bitte keinen leeren Nickname angeben!");
    }else{
      savedNickname = nicknameEingabe.value;
        nicknameEingabe.readOnly = true;
        nicknameEingabe.style.backgroundColor = "lightgrey";
    }
}

/**
 * Mit der Methode wird die Sprache festgelegt auf der man die Nachrichten übersetzt haben will.
 */
function selectLanguage() {
    switch (document.getElementById("dropdownValue").value){
        case "1": chosenlanguage ="de"; break;
        case "2": chosenlanguage ="en"; break;
        case "3": chosenlanguage ="es"; break
    }
}

function scrollToBottom() {
    const chatTextArea = document.getElementById("chatTextArea");
    chatTextArea.scrollTop = chatTextArea.scrollHeight; // Scrollt zum unteren Rand
}

//Abschicken mit der Enter-Taste
document.addEventListener('keydown', function(event){
   if(event.key === "Enter"){
       document.getElementById("sendButton").click();
   }
});


//Testbereich
document.addEventListener('DOMContentLoaded', function() {
  var dropdownLinks = document.querySelectorAll('.dropdown-content a');
  var dropbtn = document.querySelector('.dropdownBtn');
  var hiddenInput = document.getElementById('dropdownValue');

  // Initialisiere das Dropdown mit einem Standardwert
  setDropdownValue(dropdownLinks[0].getAttribute('data-value'), dropdownLinks[0].textContent); // Setzt Option 2 als Standard

  dropdownLinks.forEach(function(link) {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      var value = this.getAttribute('data-value');
      var text = this.textContent;
      setDropdownValue(value, text);
      selectLanguage();
    });
  });

  function setDropdownValue(value, text) {
    hiddenInput.value = value;
    dropbtn.textContent = text;

    //dropbtn.focus(); // Optional: Setze den Fokus auf den Button
  }
});



























