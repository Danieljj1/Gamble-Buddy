from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('Home.html')

#BlackJack Routes/Subroutes

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

#Roulette Routes/Subroutes

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

#Slot Routes/Subroutes

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
