let savedNickname;
let chosenlanguage = "de";

let socket;

function buttonSendAction() {
    const eingabeFenster = document.getElementById("chatTextEingabe");

    let eingabeText = eingabeFenster.value;

    if(eingabeText === '' || savedNickname ==='') {
        alert("Bitte Nachricht eingeben!")
    }else {

        // Entfernen Sie jede direkte Anzeige im Chatfenster hier.
        eingabeFenster.value = ""; // Eingabefeld leeren

        const now = new Date();

        var hour = now.getHours().toString().padStart(2, '0');
        var minute = now.getMinutes().toString().padStart(2, '0');
        var second = now.getSeconds().toString().padStart(2, '0');

        let timestamp = `${hour}:${minute}:${second}`;

        // JSON String bilden
        const chatnachricht = {
            username: savedNickname,
            message: eingabeText,
            timestamp: timestamp,
            language: chosenlanguage
        };
        let data = JSON.stringify(chatnachricht);


        //document.getElementById("chatTextArea").innerHTML = data;
        socket.send(data);
    }
}

function establishConnection() {
    socket = new WebSocket("ws://localhost:9000");
    
    // Connection opened
    socket.addEventListener("open", (event) => {
        //var data = JSON.stringify({"lang":"data"});
        data = "test"
        console.log(data);
    });


    socket.addEventListener("message", (event) => {
        //console.log("Message from server ", event.data);
        // Parsen der empfangenen JSON-Nachricht
        const receivedMessage = JSON.parse(event.data);

        if(receivedMessage.numOfClients) {
            const currentUsersList = document.getElementById("currentUsers");
            currentUsersList.innerHTML = '';

            for (const user in receivedMessage.clientsOnline) {
                const listItem = document.createElement("li");
                listItem.textContent = `${receivedMessage.clientsOnline[user].username}: ${receivedMessage.clientsOnline[user].language}`;
                currentUsersList.appendChild(listItem)
            }
        }
        else {
            const chatTextArea = document.getElementById("chatTextArea");
            // Formatierung der Nachricht: "nickname: nachricht (timestamp)"
            const formatMessage = `(${receivedMessage.timestamp}) ${receivedMessage.username}: ${receivedMessage.message}`;

            // Hinzufügen der formatierten Nachricht zum Chatfenster, mit Zeilenumbruch für jede neue Nachricht
            chatTextArea.value += (chatTextArea.value ? "\n" : "") + formatMessage;
            scrollToBottom();
        }
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



























