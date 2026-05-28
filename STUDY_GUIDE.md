# Gamble Buddy — Project Study Guide

Use this file to prepare to explain Gamble Buddy confidently to anyone: an interviewer, a friend, or a recruiter. Work through each section in order.

---

## 1. The 30-Second Pitch

> *What is it, who is it for, and what problem does it solve?*

**Gamble Buddy is a responsible gambling tool** — specifically a bankroll coach and strategy simulator. You enter your bankroll, pick a casino game (Blackjack, Roulette, Slots, etc.), and choose your risk tolerance. The app uses real casino math — house edges, Kelly criterion-style bet sizing, and statistical approximations — to calculate your optimal bet size, how long your session will realistically last, and what your probability of losing everything is. It also lets you simulate betting strategies like Martingale and Flat betting to see how they play out over time.

Practice saying this out loud until it takes under 30 seconds and feels natural.

---

## 2. Technical Architecture

```
User Browser (HTML templates + JS)
         |
         | HTTP / JSON
         v
   Flask Backend (Python)
         |
   Pure math calculations
   (no database, no external API)
         |
         v
   JSON response to browser
```

### Tech Stack at a Glance

| Layer | Technology | Why This Choice |
|---|---|---|
| Backend | Python + Flask | Simple route-serving; no database or async needed |
| Frontend | HTML + CSS + JS (Jinja2) | No framework needed for this level of interactivity |
| Math | Python's `math` module | All calculations are pure Python — no external libraries |
| Deployment | Render | Free tier, easy deploy from GitHub |

**Note**: No AI, no database, no external API. Everything is computed with math at request time. This was an intentional design decision — the app is about showing users the actual statistical reality of gambling, not a simulation or random outcome.

---

## 3. The Math — Know This Cold

The bankroll coach is the most technically interesting part of the app. Here's exactly what gets calculated:

### House Edge (built-in constants)
```python
GAME_HOUSE_EDGES = {
    "blackjack_basic":        0.005,   # 0.5% — with optimal strategy
    "blackjack_no_strategy":  0.02,    # 2% — average player
    "roulette_european":      0.027,   # 2.7% — single zero
    "roulette_american":      0.053,   # 5.3% — double zero
    "slots_low":              0.04,    # 4%
    "slots_high":             0.08,    # 8%
    "craps_pass":             0.014,   # 1.4% — pass line bet
    "baccarat":               0.011,   # 1.1% — banker bet
}
```
These are real, documented casino statistics — not made up.

### Bet Sizing (Kelly-style fractions)
```python
RISK_MULTIPLIERS = {
    "conservative": 0.01,   # 1% of bankroll per bet
    "moderate":     0.025,  # 2.5%
    "aggressive":   0.05,   # 5%
}
bет_size = bankroll * bet_fraction
```

### Key Calculations in `calculate_coach_advice()`

| What | How |
|---|---|
| Expected loss per hand | `bet_size × house_edge` |
| Expected hands until broke | `bankroll ÷ expected_loss_per_hand` |
| Session length (hands) | `(hands until broke) × 0.3`, capped at 500 |
| Session length (hours) | Table games = 40 hands/hr; Slots = 300 spins/hr |
| Ruin probability | Simplified estimate: `(total expected loss ÷ bankroll) × risk multiplier` |

### The Key Insight to Communicate
The house edge is small per hand but compounds over hundreds of hands. Even 0.5% house edge on Blackjack means that over 500 hands at $10/bet, you're expected to lose $25. The app makes this concrete and visible.

---

## 4. The Three Betting Strategies

The app simulates three strategies across Blackjack, Roulette, and Slots:

### Martingale
- **Rule**: Double your bet after every loss. Return to base bet after a win.
- **The trap**: A 6-loss streak turns a $10 bet into $640. Most players hit the table maximum or go broke before recovering.
- **What the simulation shows**: Short-term it looks like it works (you always win back losses), but one bad streak wipes out all gains.

### Reverse Martingale (Paroli)
- **Rule**: Double your bet after every win. Return to base bet after a loss.
- **The idea**: Ride winning streaks and protect your bankroll during losing streaks.
- **Reality**: Winning streaks are just as random as losing streaks — the house edge still applies to every single hand.

### Flat Betting
- **Rule**: Always bet the same amount.
- **Why it's actually best**: Minimizes variance, maximizes session length. Given that you'll lose in the long run regardless, flat betting just means you lose more slowly.

---

## 5. App Routes — Know the Structure

```python
GET  /              → Home.html
GET  /coach         → Coach.html
POST /api/coach     → JSON response (the bankroll calculator)

GET  /blackjack              → Blackjack strategy selection
GET  /blackjack-martingale   → Martingale simulator
GET  /blackjack-reverse-martingale
GET  /blackjack-flat

GET  /roulette               → Roulette strategy selection
GET  /roulette-martingale
GET  /roulette-reverse-martingale
GET  /roulette-flat

GET  /slots                  → Slots selection
GET  /slots-low-volatility
GET  /slots-high-volatility
```

The pattern is consistent: game selection page → strategy-specific simulator page.

---

## 6. The Tips System

The bankroll coach also generates personalized tips based on the inputs:

```python
if house_edge > 0.05:  # High house edge game
    tips.append("⚠️ This game has a high house edge...")
if risk == "aggressive":
    tips.append("⚠️ Aggressive risk means you could lose your bankroll in under 20 hands...")
if session_goal > bankroll * 0.5:
    tips.append("⚠️ Winning X from Y requires a Z% gain — unlikely given the house edge.")
tips.append(f"✅ Expected value per 100 hands: -${expected_loss * 100:.2f}")
tips.append(f"✅ Set a loss limit of ${bankroll * 0.5:.0f} (50% of bankroll). Walk away if you hit it.")
```

This is rule-based logic — not AI. Each tip checks a specific mathematical condition.

---

## 7. Concepts You Can Explain

- **House edge**: The casino's mathematical advantage built into every game. It's a percentage of each bet that the casino expects to keep over time.
- **Kelly criterion**: A mathematical formula for optimal bet sizing based on your edge and bankroll. Gamble Buddy uses a simplified version (fixed percentages) since players always have a negative edge.
- **Expected value (EV)**: The average outcome over many trials. All casino games have negative EV for the player.
- **Variance**: How much actual results deviate from expected. Slots have high variance (big swings), flat blackjack has low variance (steady, slow loss).
- **Flask routing**: `@app.route()` maps URLs to Python functions; routes can serve HTML pages or return JSON for API endpoints.
- **Separation of concerns**: The calculation logic (`calculate_coach_advice`) is separate from the Flask route (`/api/coach`), making it easy to test and maintain.
- **Template rendering**: `render_template('Coach.html')` passes data to Jinja2 HTML templates.

---

## 8. Interview Q&A — Practice These Out Loud

**Q: Walk me through what Gamble Buddy does.**
> A: It's a responsible gambling app with two main sections. The Bankroll Coach takes your bankroll, game choice, and risk level, then calculates the mathematically optimal bet size, how many hands you can expect to play, your probability of losing everything, and gives specific tips. The Strategy Simulator lets you actually play through hands of Blackjack or Roulette using Martingale, Reverse Martingale, or Flat betting strategies so you can see how they behave in practice.

**Q: What math is behind the bankroll calculations?**
> A: The core formula is simple: expected loss per hand equals bet size times house edge. For example, with a $100 bankroll, $5 bets, and a 2.7% house edge on European Roulette, you expect to lose about $0.135 per hand. From there I can estimate how many hands before the bankroll is gone, scale that to realistic session lengths (40 hands/hour for table games), and calculate a rough ruin probability. The bet sizing uses Kelly-style fractions — 1%, 2.5%, or 5% of bankroll depending on risk tolerance.

**Q: Why Flask and not FastAPI for this project?**
> A: This app is simpler — no database, no user accounts, no async operations. Flask's simplicity is an advantage here. I reach for FastAPI when I need automatic request validation with Pydantic or async support. Gamble Buddy just needs to receive some numbers, do math, and return a JSON response — Flask handles that with less overhead.

**Q: What is the Martingale strategy and why do people think it works?**
> A: Martingale is a betting system where you double your bet after every loss. The intuition is that you can't lose forever — eventually you'll win and recover everything. The flaw is that losing streaks happen, and the required bet size grows exponentially: 6 losses in a row turns a $10 bet into a $640 bet. At that point you either hit the table maximum or run out of money. The house edge applies to every single bet, so Martingale just concentrates the inevitable loss into one catastrophic hand.

**Q: The app doesn't use a database — why not?**
> A: There's nothing to persist. The bankroll calculations are stateless — you send inputs, get outputs, done. No user accounts, no saved sessions. Adding a database would be over-engineering. If I wanted to add a feature like "save your session history," that would justify a database.

**Q: What would you add next?**
> A: A Monte Carlo simulation — instead of showing a single expected value, run 10,000 simulated sessions and show a distribution of outcomes. That would make the variance and ruin probability much more visceral and concrete than a single number.

---

## 9. Weak Points & Honest Answers

- **Simplified ruin probability**: The ruin probability calculation is an approximation, not a rigorous formula. A proper calculation would use the exact risk-of-ruin formula from probability theory.
- **No actual game randomness in the coach**: The coach gives expected values, not simulated outcomes. The strategy simulators are where the actual randomness lives.
- **Static house edge values**: Real-world house edges vary slightly by casino rules (number of decks, dealer stands on soft 17, etc.). The app uses single representative values.
- **No mobile optimization**: The UI was designed for desktop.

---

## 10. Self-Test Checklist

- [ ] Can I explain what house edge is in one sentence?
- [ ] Can I explain the math behind the expected loss calculation?
- [ ] Can I explain why Martingale doesn't beat the house edge?
- [ ] Can I name all three betting strategies and explain the difference?
- [ ] Can I explain why I chose Flask over FastAPI for this project?
- [ ] Can I describe one limitation and what I'd improve?
- [ ] Can I give the 30-second pitch without notes?

---

## 11. One-Line Answers for Small Talk

- **"What's Gamble Buddy?"** → "A tool that uses casino math to show you how long your bankroll will last, what bet size to use, and why certain betting strategies that sound clever don't actually work."
- **"What tech did you use?"** → "Python Flask backend, HTML/CSS/JavaScript frontend — all pure math, no AI or database."
- **"What did you learn building it?"** → "The actual probability math behind casino games — house edge, expected value, variance — and how to turn that into something visual and useful."
