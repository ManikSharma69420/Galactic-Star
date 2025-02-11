let isGamePaused = false;
let events = [];
let audio = new Audio("MoN_HHC.mp3");
audio.loop = true; // Enable looping

function setupEventListeners() {
    document.addEventListener('keydown', (event) => {
        events.push({ type: 'keydown', key: event.key });
    });

    document.addEventListener('keyup', (event) => {
        events.push({ type: 'keyup', key: event.key });
    });

    document.addEventListener("touchstart", function(event) {
        event.preventDefault();

        if (event.touches.length === 2) {
            // Two-finger tap toggles pause
            togglePause();
        } else if (event.touches.length === 1 && !isGamePaused) {
            // Single tap makes the player jump
            events.push({ type: 'touchstart' });
        }
    });
}

function togglePause() {
    isGamePaused = !isGamePaused;

    if (isGamePaused) {
        audio.pause(); // Pause music
    } else {
        audio.play(); // Resume music
    }
}

function getEvents() {
    let currentEvents = [...events];
    events = [];
    return currentEvents;
}

async function play() {
    document.body.innerHTML = ''; // Clear previous elements

    let score = 0;
    let speed = 6;

    const gameWindow = document.createElement('canvas');
    document.body.appendChild(gameWindow);
    const context = gameWindow.getContext('2d');
    gameWindow.width = 480;
    gameWindow.height = 640;

    const player = { x: 30, y: 320, width: 45, height: 60 };
    const pipe = { x: 480, y: Math.floor(Math.random() * 570), width: 45, height: 70 };
    let coins = { x: 480, y: Math.floor(Math.random() * 570), width: 35, height: 35 };

    // Ensure the coin is at least 75 pixels away from the pipe
    if (collides(pipe, coins)) {
        coins.y += 75;
        if (coins.y + coins.height > 570) {
            coins.y = pipe.y - 75 - coins.height; // Move it above instead
        }
    }

    let playerVelocity = 0;
    const gravity = 0.75;
    const jumpStrength = -12;

    function showScore() {
        context.font = "20px Consolas";
        context.fillStyle = "white";
        context.fillText(`Score: ${score}`, 10, 20);
    }

    function renderPauseScreen() {
        context.fillStyle = "rgba(50, 50, 50, 0.5)";
        context.fillRect(0, 0, gameWindow.width, gameWindow.height);
        context.font = "50px Consolas";
        context.fillStyle = "white";
        context.fillText("Paused", 150, 300);
        context.font = "16px Consolas";
        context.fillText("Two-Finger Tap or Press ESC or P to Resume", 50, 350);
    }

    audio.play(); // Start playing audio when the game starts

    while (true) {

        await new Promise(resolve => setTimeout(resolve, 1000 / 60));

        for (const event of getEvents()) {
            if (event.type === 'keydown') {
                if (event.key === ' ' || event.key === 'ArrowUp') {
                    if (!isGamePaused) playerVelocity = jumpStrength;
                }
                if (event.key === 'p' || event.key === 'Escape') {
                    togglePause();
                }
            }
            
            document.body.onmousedown = function(){
                if (!isGamePaused) playerVelocity = jumpStrength
            }

            if (event.type === 'touchstart') {
                if (!isGamePaused) playerVelocity = jumpStrength
            }
        }

        // Clear screen
        context.clearRect(0, 0, gameWindow.width, gameWindow.height);
        context.fillStyle = "rgb(50, 50, 50)";
        context.fillRect(0, 0, gameWindow.width, gameWindow.height);

        if (!isGamePaused) {
            playerVelocity += gravity;
            player.y += playerVelocity;

            if (player.y > 640) player.y = 0;
            if (player.y < 0) player.y = 640;

            pipe.x -= speed;
            if (pipe.x < -70) {
                pipe.x = 480;
                pipe.y = Math.floor(Math.random() * 570);
            }

            coins.x -= speed;
            if (coins.x < -70) {
                coins.x = 480;
                coins.y = Math.floor(Math.random() * 570);
            }

            if (collides(player, pipe)) {
                score = 0;
                pipe.x = 480;
                pipe.y = Math.floor(Math.random() * 570);
            }

            if (collides(player, coins)) {
                score += 1;
                coins.x = 480;
                coins.y = Math.floor(Math.random() * 570);
            }
        }

        context.fillStyle = "rgb(255, 0, 0)";
        context.fillRect(player.x, player.y, player.width, player.height);
        context.fillStyle = "rgb(0, 255, 0)";
        context.fillRect(pipe.x, pipe.y, pipe.width, pipe.height);
        context.fillStyle = "rgb(255, 255, 0)";
        context.fillRect(coins.x, coins.y, coins.width, coins.height);

        showScore();

        if (score >= 60) {
            context.font = "20px Consolas";
            context.fillStyle = "white";
            context.fillText("ENDLESS MODE", 150, 600);
        }

        if (playerVelocity > 75) {
            playerVelocity = 75;
        }

        if (isGamePaused) {
            renderPauseScreen(); // 🎯 Show pause screen when game is paused
        }
    }
}

async function main() {
    document.body.innerHTML = ''; // Clear previous elements

    const gameWindow = document.createElement('canvas');
    document.body.appendChild(gameWindow);
    const context = gameWindow.getContext('2d');
    gameWindow.width = 480;
    gameWindow.height = 640;

    setupEventListeners();

    // Determine font size based on screen width
    let titleFontSize = window.innerWidth <= 600 ? "40px" : "75px"; // Smaller font on mobile

    context.fillStyle = "rgb(50, 50, 50)";
    context.fillRect(0, 0, gameWindow.width, gameWindow.height);
    context.font = titleFontSize + " Consolas"; // Dynamic font size for title
    context.fillStyle = "white";
    context.fillText("Galactic\nStar", 35, 200);

    context.font = "20px Consolas";
    context.fillText("Press Enter or Tap to Play", 100, 600);

    while (true) {
        await new Promise(resolve => setTimeout(resolve, 100));
        for (const event of getEvents()) {
            if (event.type === 'keydown' && event.key === 'Enter') {
                play();
                return;
            }
            if (event.type === 'touchstart') {
                play();
                return;
            }
        }
    }
}

function collides(rect1, rect2) {
    return (
        rect1.x < rect2.x + rect2.width &&
        rect1.x + rect1.width > rect2.x &&
        rect1.y < rect2.y + rect2.height &&
        rect1.y + rect1.height > rect2.y
    );
}

main();
