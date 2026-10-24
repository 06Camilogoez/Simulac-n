const CATEGORIES = [
  { id: "ACES", name: "Unos (1)", section: "upper" },
  { id: "TWOS", name: "Doses (2)", section: "upper" },
  { id: "THREES", name: "Treses (3)", section: "upper" },
  { id: "FOURS", name: "Cuatros (4)", section: "upper" },
  { id: "FIVES", name: "Cincos (5)", section: "upper" },
  { id: "SIXES", name: "Seises (6)", section: "upper" },
  { id: "THREE_OF_A_KIND", name: "Trío (3 iguales)", section: "lower" },
  { id: "FOUR_OF_A_KIND", name: "Póker (4 iguales)", section: "lower" },
  { id: "FULL_HOUSE", name: "Full House (25)", section: "lower" },
  { id: "SMALL_STRAIGHT", name: "Escalera Menor (30)", section: "lower" },
  { id: "LARGE_STRAIGHT", name: "Escalera Mayor (40)", section: "lower" },
  { id: "YAHTZEE", name: "Yahtzee (50)", section: "lower" },
  { id: "CHANCE", name: "Azar (Suma)", section: "lower" }
];

const gameState = {
  players: [
    { name: "Jugador 1", scores: {} },
    { name: "Jugador 2", scores: {} }
  ],
  currentPlayerIdx: 0,
  currentRound: 1,
  currentRoll: 0,
  dice: [1, 1, 1, 1, 1],
  held: [false, false, false, false, false],
  gameOver: false
};

function calculateScore(catId, dice) {
  const counts = {};
  let sum = 0;
  for (const d of dice) {
    counts[d] = (counts[d] || 0) + 1;
    sum += d;
  }
  const countVals = Object.values(counts).sort((a,b) => a-b);
  const sorted = [...dice].sort().join("");

  switch (catId) {
    case "ACES": return (counts[1] || 0) * 1;
    case "TWOS": return (counts[2] || 0) * 2;
    case "THREES": return (counts[3] || 0) * 3;
    case "FOURS": return (counts[4] || 0) * 4;
    case "FIVES": return (counts[5] || 0) * 5;
    case "SIXES": return (counts[6] || 0) * 6;
    case "THREE_OF_A_KIND":
      return countVals.some(c => c >= 3) ? sum : 0;
    case "FOUR_OF_A_KIND":
      return countVals.some(c => c >= 4) ? sum : 0;
    case "FULL_HOUSE":
      return (countVals.length === 2 && countVals[0] === 2 && countVals[1] === 3) || countVals[0] === 5 ? 25 : 0;
    case "SMALL_STRAIGHT": {
      const setD = new Set(dice);
      const s1 = [1,2,3,4].every(v => setD.has(v));
      const s2 = [2,3,4,5].every(v => setD.has(v));
      const s3 = [3,4,5,6].every(v => setD.has(v));
      return (s1 || s2 || s3) ? 30 : 0;
    }
    case "LARGE_STRAIGHT":
      return (sorted === "12345" || sorted === "23456") ? 40 : 0;
    case "YAHTZEE":
      return countVals.some(c => c === 5) ? 50 : 0;
    case "CHANCE":
      return sum;
    default:
      return 0;
  }
}

function initTables() {
  ["table-p1", "table-p2"].forEach((tableId, pIdx) => {
    const tbody = document.querySelector(`#${tableId} tbody`);
    tbody.innerHTML = "";

    CATEGORIES.filter(c => c.section === "upper").forEach(cat => {
      const tr = document.createElement("tr");
      tr.id = `row-${pIdx}-${cat.id}`;
      tr.innerHTML = `<td>${cat.name}</td><td class="score-cell">-</td>`;
      tr.addEventListener("click", () => selectCategory(pIdx, cat.id));
      tbody.appendChild(tr);
    });

    const trSubSup = document.createElement("tr");
    trSubSup.className = "summary-row";
    trSubSup.innerHTML = `<td>Subtotal Superior</td><td id="sub-sup-${pIdx}">0</td>`;
    tbody.appendChild(trSubSup);

    const trBonoSup = document.createElement("tr");
    trBonoSup.className = "summary-row";
    trBonoSup.innerHTML = `<td>Bono Superior (+35)</td><td id="bono-sup-${pIdx}">0</td>`;
    tbody.appendChild(trBonoSup);

    CATEGORIES.filter(c => c.section === "lower").forEach(cat => {
      const tr = document.createElement("tr");
      tr.id = `row-${pIdx}-${cat.id}`;
      tr.innerHTML = `<td>${cat.name}</td><td class="score-cell">-</td>`;
      tr.addEventListener("click", () => selectCategory(pIdx, cat.id));
      tbody.appendChild(tr);
    });

    const trSubInf = document.createElement("tr");
    trSubInf.className = "summary-row";
    trSubInf.innerHTML = `<td>Subtotal Inferior</td><td id="sub-inf-${pIdx}">0</td>`;
    tbody.appendChild(trSubInf);

    const trTotal = document.createElement("tr");
    trTotal.className = "total-row";
    trTotal.innerHTML = `<td>Total General</td><td id="total-${pIdx}">0</td>`;
    tbody.appendChild(trTotal);
  });
}

function updateUI() {
  const pIdx = gameState.currentPlayerIdx;
  const player = gameState.players[pIdx];

  document.getElementById("turn-text").innerText = `Turno: ${player.name} (Ronda ${gameState.currentRound}/13)`;
  document.getElementById("roll-count").innerText = `Lanzamiento: ${gameState.currentRoll} de 3`;

  const btnRoll = document.getElementById("btn-roll");
  if (gameState.currentRoll >= 3 || gameState.gameOver) {
    btnRoll.disabled = true;
    btnRoll.innerText = "Selecciona categoría";
  } else {
    btnRoll.disabled = false;
    btnRoll.innerText = gameState.currentRoll === 0 ? "Lanzar Dados" : `Relanzar (${gameState.currentRoll + 1}/3)`;
  }

  for (let i = 0; i < 5; i++) {
    const faceEl = document.getElementById(`die-${i}`);
    const cardEl = faceEl.parentElement;
    const statusEl = document.getElementById(`status-${i}`);
    faceEl.innerText = gameState.dice[i];

    if (gameState.held[i]) {
      cardEl.classList.add("held");
      statusEl.innerText = "Conservado";
    } else {
      cardEl.classList.remove("held");
      statusEl.innerText = "Lanzar";
    }
  }

  gameState.players.forEach((p, index) => {
    let sup = 0;
    let inf = 0;

    CATEGORIES.forEach(cat => {
      const row = document.getElementById(`row-${index}-${cat.id}`);
      const cell = row.querySelector(".score-cell");
      const isFilled = p.scores[cat.id] !== undefined;

      if (isFilled) {
        row.className = "";
        cell.innerText = p.scores[cat.id];
        if (cat.section === "upper") sup += p.scores[cat.id];
        if (cat.section === "lower") inf += p.scores[cat.id];
      } else {
        if (index === pIdx && gameState.currentRoll > 0) {
          row.className = "clickable highlight-pick";
          const pot = calculateScore(cat.id, gameState.dice);
          cell.innerText = `+${pot}`;
          cell.classList.add("preview-score");
        } else {
          row.className = "";
          cell.innerText = "-";
          cell.classList.remove("preview-score");
        }
      }
    });

    const bono = sup >= 63 ? 35 : 0;
    const total = sup + bono + inf;

    document.getElementById(`sub-sup-${index}`).innerText = sup;
    document.getElementById(`bono-sup-${index}`).innerText = bono;
    document.getElementById(`sub-inf-${index}`).innerText = inf;
    document.getElementById(`total-${index}`).innerText = total;
  });
}

function rollDice() {
  if (gameState.currentRoll >= 3 || gameState.gameOver) return;

  for (let i = 0; i < 5; i++) {
    if (gameState.currentRoll === 0 || !gameState.held[i]) {
      gameState.dice[i] = Math.floor(Math.random() * 6) + 1;
    }
  }
  gameState.currentRoll++;
  updateUI();
}

function toggleHold(idx) {
  if (gameState.currentRoll === 0 || gameState.currentRoll >= 3) return;
  gameState.held[idx] = !gameState.held[idx];
  updateUI();
}

function selectCategory(pIdx, catId) {
  if (pIdx !== gameState.currentPlayerIdx) return;
  if (gameState.currentRoll === 0) {
    alert("Debes lanzar los dados al menos una vez.");
    return;
  }
  const player = gameState.players[pIdx];
  if (player.scores[catId] !== undefined) return;

  const score = calculateScore(catId, gameState.dice);
  player.scores[catId] = score;

  gameState.currentRoll = 0;
  gameState.held = [false, false, false, false, false];

  if (gameState.currentPlayerIdx === 1) {
    gameState.currentPlayerIdx = 0;
    gameState.currentRound++;
  } else {
    gameState.currentPlayerIdx = 1;
  }

  if (gameState.currentRound > 13) {
    gameState.gameOver = true;
    const t1 = parseInt(document.getElementById("total-0").innerText, 10);
    const t2 = parseInt(document.getElementById("total-1").innerText, 10);
    let msg = `Partida finalizada.\nJugador 1: ${t1} pts\nJugador 2: ${t2} pts\n`;
    if (t1 > t2) msg += "Ganador: Jugador 1";
    else if (t2 > t1) msg += "Ganador: Jugador 2";
    else msg += "Resultado: Empate";
    alert(msg);
  }

  updateUI();
}

function restartGame() {
  gameState.players[0].scores = {};
  gameState.players[1].scores = {};
  gameState.currentPlayerIdx = 0;
  gameState.currentRound = 1;
  gameState.currentRoll = 0;
  gameState.dice = [1, 1, 1, 1, 1];
  gameState.held = [false, false, false, false, false];
  gameState.gameOver = false;
  updateUI();
}

function runMonteCarlo() {
  const n = parseInt(document.getElementById("mc-runs").value, 10);
  const loading = document.getElementById("mc-loading");
  loading.style.display = "block";

  setTimeout(() => {
    let p1Wins = 0, p2Wins = 0;
    let p1Sum = 0, p2Sum = 0;
    const s1Arr = [], s2Arr = [];
    let yTotal = 0;

    for (let i = 0; i < n; i++) {
      let p1 = 0, p2 = 0;
      let hadY = 0;
      for (let r = 0; r < 13; r++) {
        const d1 = [0,0,0,0,0].map(() => Math.floor(Math.random()*6)+1);
        const d2 = [0,0,0,0,0].map(() => Math.floor(Math.random()*6)+1);
        p1 += d1.reduce((a,b)=>a+b, 0) + (Math.random() < 0.12 ? 15 : 0);
        p2 += d2.reduce((a,b)=>a+b, 0) + (Math.random() < 0.12 ? 15 : 0);
        if (Math.random() < 0.046) hadY = 1;
      }
      p1Sum += p1;
      p2Sum += p2;
      s1Arr.push(p1);
      s2Arr.push(p2);
      if (p1 > p2) p1Wins++;
      else if (p2 > p1) p2Wins++;
      if (hadY) yTotal++;
    }

    const m1 = p1Sum / n;
    const m2 = p2Sum / n;
    const sd1 = Math.sqrt(s1Arr.reduce((acc, v) => acc + Math.pow(v - m1, 2), 0) / n);
    const sd2 = Math.sqrt(s2Arr.reduce((acc, v) => acc + Math.pow(v - m2, 2), 0) / n);

    document.getElementById("res-m1").innerText = `${m1.toFixed(1)} pts`;
    document.getElementById("res-m2").innerText = `${m2.toFixed(1)} pts`;
    document.getElementById("res-sd1").innerText = `±${sd1.toFixed(1)}`;
    document.getElementById("res-sd2").innerText = `±${sd2.toFixed(1)}`;
    document.getElementById("res-w1").innerText = `${((p1Wins / n) * 100).toFixed(1)}%`;
    document.getElementById("res-w2").innerText = `${((p2Wins / n) * 100).toFixed(1)}%`;
    document.getElementById("res-y1").innerText = `${((yTotal / n) * 100).toFixed(1)}%`;
    document.getElementById("res-y2").innerText = `${((yTotal / n) * 100).toFixed(1)}%`;

    loading.style.display = "none";
  }, 100);
}

document.addEventListener("DOMContentLoaded", () => {
  initTables();
  updateUI();

  document.getElementById("btn-roll").addEventListener("click", rollDice);
  document.getElementById("btn-restart").addEventListener("click", restartGame);
  document.getElementById("btn-run-sim").addEventListener("click", runMonteCarlo);

  document.querySelectorAll(".die-card").forEach(card => {
    card.addEventListener("click", () => {
      const idx = parseInt(card.dataset.index, 10);
      toggleHold(idx);
    });
  });

  const btnGame = document.getElementById("btn-tab-game");
  const btnMC = document.getElementById("btn-tab-mc");
  const pnlGame = document.getElementById("section-game");
  const pnlMC = document.getElementById("section-mc");

  btnGame.addEventListener("click", () => {
    btnGame.classList.add("active");
    btnMC.classList.remove("active");
    pnlGame.classList.add("active");
    pnlMC.classList.remove("active");
  });

  btnMC.addEventListener("click", () => {
    btnMC.classList.add("active");
    btnGame.classList.remove("active");
    pnlMC.classList.add("active");
    pnlGame.classList.remove("active");
  });
});
