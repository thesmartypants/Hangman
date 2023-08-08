        function create_game() {
            fetch('http://localhost:5000/create_game')
                .then(response => response.json())
                .then(data => {
                    const jsn = JSON.parse(data);
                    document.getElementById("currentWordLabel").textContent = "Current Word: " + jsn.current_word;
                    document.getElementById("attemptsLabel").textContent = "Attempts: " + jsn.attempts;
                    document.getElementById("gameIdLabel").textContent = "Game ID: " + jsn.game_id;
                    document.getElementById("gameStatusLabel").textContent = "Game Status: " + jsn.game_status;
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
function submit() {
    var letter = document.getElementById("letter").value;
    var id = document.getElementById("gameIdLabel").textContent.replace('Game ID: ', '');

    fetch('http://localhost:5000/process_letter/' + id + '/' + letter)
        .then(response => response.text()) // Read the response as text
        .then(data => {
            console.log('Received Data:', data); // Log the received data
            var jsonData = JSON.parse(data); // Manually parse the JSON
            console.log('Parsed Data:', jsonData); // Log the parsed JSON data
            document.getElementById("currentWordLabel").textContent = "Current Word: " + jsonData.current_word;
            document.getElementById("attemptsLabel").textContent = "Attempts: " + jsonData.attempts;
            document.getElementById("gameStatusLabel").textContent = "Game Status: " + jsonData.game_status;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


