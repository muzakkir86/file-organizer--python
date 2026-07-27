const gameArea = document.getElementById('gameArea');
const playerCar = document.getElementById('playerCar');
const scoreDisplay = document.getElementById('score');
const speedDisplay = document.getElementById('speed');
const message = document.getElementById('message');
const startButton = document.getElementById('startButton');

let gameData = {
  running: false,
  score: 0,
  speed: 5,
  keys: {
    ArrowUp: false,
    ArrowDown: false,
    ArrowLeft: false,
    ArrowRight: false,
  },
  enemies: [],
};

const player = {
  x: 130,
  y: 400,
  width: 40,
  height: 70,
};

function startGame() {
  gameData.running = true;
  gameData.score = 0;
  gameData.speed = 5;
  scoreDisplay.textContent = gameData.score;
  speedDisplay.textContent = gameData.speed;
  message.textContent = 'Race started!';

  player.x = 130;
  player.y = 400;
  playerCar.style.left = player.x + 'px';
  playerCar.style.top = player.y + 'px';

  gameData.enemies.forEach(enemy => enemy.element.remove());
  gameData.enemies = [];

  createEnemy();
  createEnemy();
  createEnemy();

  window.requestAnimationFrame(updateGame);
}

function updateGame() {
  if (!gameData.running) return;

  movePlayer();
  moveEnemies();
  updateScore();
  increaseSpeed();

  if (detectCollision()) {
    endGame();
    return;
  }

  window.requestAnimationFrame(updateGame);
}

function movePlayer() {
  if (gameData.keys.ArrowLeft && player.x > 10) {
    player.x -= 6;
  }
  if (gameData.keys.ArrowRight && player.x < 250) {
    player.x += 6;
  }
  if (gameData.keys.ArrowUp && player.y > 10) {
    player.y -= 6;
  }
  if (gameData.keys.ArrowDown && player.y < 430) {
    player.y += 6;
  }

  playerCar.style.left = player.x + 'px';
  playerCar.style.top = player.y + 'px';
}

function createEnemy() {
  const enemy = document.createElement('div');
  enemy.classList.add('enemy-car');
  enemy.style.left = Math.floor(Math.random() * 260) + 'px';
  enemy.style.top = -(Math.floor(Math.random() * 300) + 100) + 'px';
  gameArea.appendChild(enemy);

  gameData.enemies.push({ element: enemy, x: parseInt(enemy.style.left), y: parseInt(enemy.style.top) });
}

function moveEnemies() {
  gameData.enemies.forEach(enemy => {
    enemy.y += gameData.speed;
    enemy.element.style.top = enemy.y + 'px';

    if (enemy.y > 520) {
      enemy.y = -(Math.floor(Math.random() * 250) + 120);
      enemy.x = Math.floor(Math.random() * 260);
      enemy.element.style.left = enemy.x + 'px';
      enemy.element.style.top = enemy.y + 'px';
    }
  });
}

function detectCollision() {
  return gameData.enemies.some(enemy => {
    const enemyRect = {
      left: enemy.x,
      right: enemy.x + 40,
      top: enemy.y,
      bottom: enemy.y + 70,
    };

    const playerRect = {
      left: player.x,
      right: player.x + player.width,
      top: player.y,
      bottom: player.y + player.height,
    };

    return (
      playerRect.left < enemyRect.right &&
      playerRect.right > enemyRect.left &&
      playerRect.top < enemyRect.bottom &&
      playerRect.bottom > enemyRect.top
    );
  });
}

function updateScore() {
  gameData.score += 1;
  scoreDisplay.textContent = gameData.score;
}

function increaseSpeed() {
  if (gameData.score % 150 === 0) {
    gameData.speed += 1;
    speedDisplay.textContent = gameData.speed;
  }
}

function endGame() {
  gameData.running = false;
  message.textContent = 'Game over! Press Start to try again.';
}

window.addEventListener('keydown', event => {
  if (event.key in gameData.keys) {
    gameData.keys[event.key] = true;
  }
});

window.addEventListener('keyup', event => {
  if (event.key in gameData.keys) {
    gameData.keys[event.key] = false;
  }
});

startButton.addEventListener('click', startGame);
