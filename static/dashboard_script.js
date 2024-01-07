// Update player count for a specific server
function updatePlayerCount(serverId) {
    fetch(`/player_count/${serverId}`)
        .then(response => response.json())
        .then(data => {
            const playerCountElement = document.getElementById(`player-count-${serverId}`);
            if (playerCountElement && data[0]) {
                playerCountElement.innerHTML = `Player Count: ${data[0]}`;
            }
        })
        .catch(error => {
            console.error('Error fetching player count:', error);
        });
}

// Update player count for all running servers initially
function updateAllPlayerCounts() {
    console.log("updating all player counts...")
    const runningServers = document.querySelectorAll('.server-list .player-count');
    runningServers.forEach(playerCountElement => {
        const serverId = playerCountElement.id.split('-')[2]; // Extract server ID from the element ID
        console.log(serverId);
        updatePlayerCount(serverId);
    });
    console.log("player counts updated");
}

// Fetch player counts for running servers every 3 minutes
setInterval(updateAllPlayerCounts, 3 * 60 * 1000);

console.log("Dashboard script loaded");