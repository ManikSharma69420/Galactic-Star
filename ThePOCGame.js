let isGamePaused = false;
let events = [];

function setupEventListeners() {
    document.addEventListener('keydown', (event) => {
        events.push({ type: 'keydown', key: event.key });
    });

    document.addEventListener('keyup', (event) => {
        events.push({ type: 'keyup', key: event.key });
    });
}

function getEvents() {
    let currentEvents = [...events];
    events = []; // Clear events after reading
    return currentEvents;
}

async function play() {
    document.body.innerHTML = ''; // Clear previous elements

    let score = 60;
    let speed = 6;

    const gameWindow = document.createElement('canvas');
    document.body.appendChild(gameWindow);
    const context = gameWindow.getContext('2d');
    gameWindow.width = 480;
    gameWindow.height = 640;

    const player = { x: 30, y: 320, width: 45, height: 60 };
    const pipe = { x: 480, y: Math.floor(Math.random() * 570), width: 45, height: 70 };

    let playerVelocity = 0;
    const gravity = 0.75;
    const jumpStrength = -12;

    function showScore() {
        context.font = "20px Consolas";
        context.fillStyle = "white";
        context.fillText(`Score: ${score}`, 10, 20);
    }

    function renderPauseScreen() {
        context.fillStyle = "rgba(0, 0, 0, 0.5)";
        context.fillRect(0, 0, gameWindow.width, gameWindow.height);
        context.font = "50px Consolas";
        context.fillStyle = "white";
        context.fillText("Paused", 150, 300);
        context.font = "20px Consolas";
        context.fillText("Press P or Escape to Continue", 75, 350);
    }

    while (true) {
        await new Promise(resolve => setTimeout(resolve, 1000 / 60));

        if (score < 10) {
            speed = 6;
        }

        if (score >= 10) {
            speed = 8;
        }

        if (score >= 20) {
            speed = 10;
        }

        if (score >= 30) {
            speed = 12;
        }

        if (score >= 40) {
            speed = 14;
        }

        if (score >= 50) {
            speed = 16;
        }

        if (score >= 100){
            speed = 20;
        }

        for (const event of getEvents()) {
            if (event.type === 'keydown') {
                if (event.key === ' ' || event.key === 'ArrowUp') {
                    playerVelocity = jumpStrength;
                }
                if (event.key === 'p' || event.key === 'Escape') {
                    isGamePaused = !isGamePaused;
                }
            }
        }

        context.clearRect(0, 0, gameWindow.width, gameWindow.height);
        context.fillStyle = "black";
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
                score++;
            }

            if (collides(player, pipe)) {
                score = 0;
                pipe.x = 480;
                pipe.y = Math.floor(Math.random() * 570);
            }
        }

        context.fillStyle = "red";
        context.fillRect(player.x, player.y, player.width, player.height);
        context.fillStyle = "yellow";
        context.fillRect(pipe.x, pipe.y, pipe.width, pipe.height);
        
        showScore();

        if (score >= 60) {
            context.font = "20px Consolas";
            context.fillStyle = "white";
            context.fillText("ENDLESS MODE", 150, 600);
        }
        
        if (isGamePaused) {
            renderPauseScreen();
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

    context.fillStyle = "black";
    context.fillRect(0, 0, gameWindow.width, gameWindow.height);
    context.font = "75px Consolas";
    context.fillStyle = "white";
    context.fillText("ThePOCGame", 35, 200);
    context.font = "20px Consolas";
    context.fillText("Press Enter to Play", 75, 600);

    while (true) {
        await new Promise(resolve => setTimeout(resolve, 100));
        for (const event of getEvents()) {
            if (event.type === 'keydown' && event.key === 'Enter') {
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
