// Blackjack rate value
const b = 80;
// Average time is about 80 blackjack hands per hour

// Roulette rate value
const r = 40;
// Average time is about 40 roulette spins per hour

// Other Variables

let m = 0; //Budget

let h = 0; //hours

// Update Budget Function
function updateBudget(amount) {
  localStorage.setItem("budget", amount);
}

// Update Time Function

function updateHour(hours) {
  localStorage.setItem("hours", hours);
}

// Blackjack Rate Function

function bjRate() {
  const budget = parseFloat(localStorage.getItem("budget"));
  const hours = parseFloat(localStorage.getItem("hours"));
  if (isNaN(budget) || isNaN(hours) || hours === 0) {
    console.log("Error: Budget or hours not set or hours is zero");
    return 0;
  }
  return budget / (b * hours);
}

// Roulette Rate Function

function rlRate() {
  const budget = parseFloat(localStorage.getItem("budget"));
  const hours = parseFloat(localStorage.getItem("hours"));
  if (isNaN(budget) || isNaN(hours) || hours === 0) {
    console.log("Error: Budget or hours not set or hours is zero");
    return 0;
  }
  return budget / (r * hours);
}

// Budget Equations

function calculateHVBudget() {
  let slotHrs = Number(document.getElementById("hours").value);
  let betPerSpin = Number(document.getElementById("bet").value);

  let HVBudget = slotHrs * 300 * betPerSpin; // 300 spins per hour

  document.getElementById("highVol").textContent =
    "High Volatility Slots: $" + HVBudget.toLocaleString();
}

function calculateLVBudget() {
  let slotHrs = Number(document.getElementById("hours").value);
  let betPerSpin = Number(document.getElementById("bet").value);

  let LVBudget = slotHrs * 600 * betPerSpin; // 600 spins per hour

  document.getElementById("lowVol").textContent =
    "Low Volatility Slots: $" + LVBudget.toLocaleString();
}
