/* Blackjack rate value*/
let b = 0;

/* Roulette rate value*/
let r = 0;

/* Other Variables */

let m = 0; /*Budget*/

let h = 0; /*hours*/

/**
 * Update Budget Function
 * @param {number} amount - The new budget amount
 */
function updateBudget(amount) {
  m = amount;
  console.log(`Budget updated to: $${m}`);
}

/**
 * Update Time Function
 * @param {number} hours - The time in hours
 */

function updateHour(hours) {
  h = hours;
  console.log(`Time updated to: ${h}`);
}
