from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# --- Bankroll Coach Logic ---

GAME_HOUSE_EDGES = {
    "blackjack_basic": 0.005,
    "blackjack_no_strategy": 0.02,
    "roulette_european": 0.027,
    "roulette_american": 0.053,
    "slots_low": 0.04,
    "slots_high": 0.08,
    "craps_pass": 0.014,
    "baccarat": 0.011,
}

GAME_LABELS = {
    "blackjack_basic": "Blackjack (Basic Strategy)",
    "blackjack_no_strategy": "Blackjack (No Strategy)",
    "roulette_european": "Roulette (European)",
    "roulette_american": "Roulette (American)",
    "slots_low": "Slots (Low Volatility)",
    "slots_high": "Slots (High Volatility)",
    "craps_pass": "Craps (Pass Line)",
    "baccarat": "Baccarat (Banker Bet)",
}

RISK_MULTIPLIERS = {
    "conservative": 0.01,   # 1% of bankroll per bet
    "moderate": 0.025,      # 2.5%
    "aggressive": 0.05,     # 5%
}

STRATEGY_DESCRIPTIONS = {
    "conservative": "Flat betting at 1% of bankroll per hand. Maximizes session length and minimizes variance.",
    "moderate": "Flat betting at 2.5% of bankroll. Balanced risk — reasonable session length with moderate swings.",
    "aggressive": "Flat betting at 5% of bankroll. Short sessions with high variance — not recommended for entertainment play.",
}

def calculate_coach_advice(bankroll: float, game: str, risk: str, session_goal: float) -> dict:
    house_edge = GAME_HOUSE_EDGES.get(game, 0.03)
    bet_fraction = RISK_MULTIPLIERS.get(risk, 0.025)
    bet_size = round(bankroll * bet_fraction, 2)
    bet_size = max(bet_size, 1.0)

    # Expected hands before ruin using risk-of-ruin approximation
    # Using Kelly-based expected rounds to lose X% of bankroll
    # P(ruin before goal) approximation
    if house_edge > 0:
        expected_loss_per_hand = bet_size * house_edge
        expected_hands_to_lose_all = bankroll / expected_loss_per_hand if expected_loss_per_hand > 0 else float('inf')
        expected_session_hands = min(expected_hands_to_lose_all * 0.3, 500)
    else:
        expected_session_hands = 500

    # Probability of losing entire bankroll in a session (simplified)
    # Using normal approximation for even-money games
    variance_per_hand = bet_size ** 2  # approx for binary outcome
    std_per_hand = math.sqrt(variance_per_hand)
    total_std = std_per_hand * math.sqrt(expected_session_hands)
    total_expected_loss = expected_loss_per_hand * expected_session_hands if house_edge > 0 else 0

    ruin_probability = min(0.99, max(0.01, (total_expected_loss / bankroll) * (1 + {"conservative": 0, "moderate": 0.5, "aggressive": 1.5}.get(risk, 0.5))))

    # Time estimates (assume 40 hands/hour for table games, 300 spins/hour for slots)
    hands_per_hour = 300 if "slots" in game else 40
    expected_hours = round(expected_session_hands / hands_per_hour, 1)

    # Break-even hands needed to hit goal
    hands_to_goal = math.ceil(session_goal / (bet_size * 0.5)) if session_goal > 0 else None

    tips = []
    if house_edge > 0.05:
        tips.append(f"⚠️ This game has a high house edge ({house_edge*100:.1f}%). Consider a game with a lower edge like Blackjack or Baccarat.")
    if risk == "aggressive":
        tips.append("⚠️ Aggressive risk means you could lose your bankroll in under 20 hands. Consider Conservative or Moderate.")
    if session_goal > bankroll * 0.5:
        tips.append(f"⚠️ Winning ${session_goal:.0f} from ${bankroll:.0f} requires a {session_goal/bankroll*100:.0f}% gain — unlikely given the house edge.")
    tips.append(f"✅ Expected value per 100 hands: -${expected_loss_per_hand * 100:.2f}")
    tips.append(f"✅ Set a loss limit of ${bankroll * 0.5:.0f} (50% of bankroll). Walk away if you hit it.")
    if "blackjack" in game and "no_strategy" in game:
        tips.append("💡 Learning basic blackjack strategy cuts the house edge from 2% to 0.5% — worth it!")

    return {
        "game": GAME_LABELS.get(game, game),
        "bankroll": bankroll,
        "bet_size": bet_size,
        "risk_strategy": risk.capitalize(),
        "strategy_description": STRATEGY_DESCRIPTIONS.get(risk, ""),
        "house_edge_pct": round(house_edge * 100, 2),
        "expected_session_hands": round(expected_session_hands),
        "expected_hours": expected_hours,
        "ruin_probability_pct": round(ruin_probability * 100, 1),
        "session_goal": session_goal,
        "tips": tips,
    }

# Home
@app.route('/')
def home():
    return render_template('Home.html')

# Bankroll Coach
@app.route('/coach')
def coach():
    return render_template('Coach.html')

@app.route('/api/coach', methods=['POST'])
def coach_api():
    data = request.get_json(force=True)
    try:
        bankroll = float(data.get('bankroll', 0))
        game = data.get('game', 'blackjack_basic')
        risk = data.get('risk', 'moderate')
        session_goal = float(data.get('session_goal', 0))
        if bankroll <= 0:
            return jsonify({"error": "Bankroll must be greater than 0"}), 400
        result = calculate_coach_advice(bankroll, game, risk, session_goal)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# BlackJack Routes
@app.route('/blackjack')
def blackjack():
    return render_template('Blackjack.html')

@app.route('/blackjack-martingale')
def blackjack_martingale():
    return render_template('BJ/BJ-Martingale.html')

@app.route('/blackjack-reverse-martingale')
def blackjack_reverse_martingale():
    return render_template('BJ/BJ-RMartingale.html')

@app.route('/blackjack-flat')
def blackjack_flat():
    return render_template('BJ/BJ-Flat.html')

# Roulette Routes
@app.route('/roulette')
def roulette():
    return render_template('Roulette.html')

@app.route('/roulette-martingale')
def roulette_martingale():
    return render_template('Roulette/Roulette-Martingale.html')

@app.route('/roulette-reverse-martingale')
def roulette_reverse_martingale():
    return render_template('Roulette/Roulette-RMartingale.html')

@app.route('/roulette-flat')
def roulette_flat():
    return render_template('Roulette/Roulette-Flat.html')

# Slots Routes
@app.route('/slots')
def slots():
    return render_template('Slots.html')

@app.route('/slots-low-volatility')
def slots_lv():
    return render_template('Slots/Slot-LV.html')

@app.route('/slots-high-volatility')
def slots_hv():
    return render_template('Slots/Slot-HV.html')

if __name__ == '__main__':
    app.run(debug=True)
