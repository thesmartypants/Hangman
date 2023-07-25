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
            var id = document.getElementById("gameIdLabel").textContent;

            fetch('http://localhost:5000/process_letter/' + id + '/' + letter)
                .then(response => response.json())
                .then(data => {
                    document.getElementById("currentWordLabel").textContent = "Current Word: " + data.current_word;
                    document.getElementById("attemptsLabel").textContent = "Attempts: " + data.attempts;
                    document.getElementById("gameStatusLabel").textContent = "Game Status: " + data.game_status;
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }