from flask import Flask, render_template, request, redirect, url_for, session, flash
from typing import Dict, List
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session management

# Global variables (in a real app, you'd want to use a database instead)
global_scores: Dict[str, Dict[str, int]] = {
    'number_game': {},
    'word_game': {},
    'math_game': {}
}
global_players: List[str] = []

class GameLevel:
    def __init__(self, is_advanced: bool = False):
        self.is_advanced = is_advanced
        self.range = (1, 100) if is_advanced else (1, 50)
        self.max_tries = 5 if is_advanced else 7

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    name = request.form.get('name')
    if not name:
        flash('Hindi pwedeng walang pangalan!', 'error')
        return redirect(url_for('index'))
    
    if name not in global_players:
        global_players.append(name)
        for game in global_scores:
            global_scores[game][name] = 0
    
    session['player_name'] = name
    return redirect(url_for('game_menu'))

@app.route('/game-menu')
def game_menu():
    if 'player_name' not in session:
        return redirect(url_for('index'))
    return render_template('game_menu.html', scores=global_scores, player=session['player_name'])

@app.route('/number-game')
def number_game():
    if 'player_name' not in session:
        return redirect(url_for('index'))
    
    # Initialize new game
    level = GameLevel()
    session['secret_number'] = random.randint(*level.range)
    session['tries_left'] = level.max_tries
    session['number_range'] = level.range
    
    return render_template('number_game.html', 
                         tries_left=session['tries_left'],
                         number_range=session['number_range'])

@app.route('/check-number', methods=['POST'])
def check_number():
    if 'player_name' not in session:
        return redirect(url_for('index'))
    
    guess = request.form.get('guess', type=int)
    if not guess:
        flash('Number lang dapat!', 'error')
        return redirect(url_for('number_game'))
    
    secret = session['secret_number']
    tries_left = session['tries_left'] - 1
    session['tries_left'] = tries_left
    
    if guess == secret:
        score = tries_left + 1
        player = session['player_name']
        global_scores['number_game'][player] = max(global_scores['number_game'][player], score)
        flash(f'Tama! Nakuha mo sa {7 - tries_left} tries!', 'success')
        return redirect(url_for('game_menu'))
    
    if tries_left <= 0:
        flash(f'Game Over! Ang number ay {secret}', 'error')
        return redirect(url_for('game_menu'))
    
    hint = 'Mas mataas pa!' if guess < secret else 'Mas mababa pa!'
    flash(hint, 'info')
    return redirect(url_for('number_game'))

@app.route('/word-game')
def word_game():
    if 'player_name' not in session:
        return redirect(url_for('index'))
    
    words = [
        ("bayani", "Taong magiting"),
        ("araw", "Nagbibigay liwanag"),
        ("dagat", "Malaking tubig na maalat"),
        ("bahaghari", "Makukulay na arko sa langit")
    ]
    
    word, hint = random.choice(words)
    session['secret_word'] = word
    session['word_tries'] = 5
    
    return render_template('word_game.html', 
                         hint=hint, 
                         word_length=len(word),
                         tries_left=session['word_tries'])

@app.route('/check-word', methods=['POST'])
def check_word():
    if 'player_name' not in session:
        return redirect(url_for('index'))
    
    guess = request.form.get('guess', '').lower()
    word = session['secret_word']
    tries_left = session['word_tries'] - 1
    session['word_tries'] = tries_left
    
    if guess == word:
        score = tries_left + 1
        player = session['player_name']
        global_scores['word_game'][player] = max(global_scores['word_game'][player], score)
        flash('Tama!', 'success')
        return redirect(url_for('game_menu'))
    
    if tries_left <= 0:
        flash(f"Game Over! Ang salita ay '{word}'", 'error')
        return redirect(url_for('game_menu'))
    
    flash('Mali!', 'error')
    return redirect(url_for('word_game'))

@app.route('/math-game')
def math_game():
    if 'player_name' not in session:
        return redirect(url_for('index'))
    
    if 'math_tries' not in session:
        session['math_tries'] = 5
        session['math_score'] = 0
    
    operations = ['+', '-', '*']
    op = random.choice(operations)
    
    if op == '*':
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
    else:
        num1 = random.randint(1, 50)
        num2 = random.randint(1, 50)
    
    session['math_problem'] = {'num1': num1, 'num2': num2, 'op': op}
    session['math_answer'] = eval(f"{num1} {op} {num2}")
    
    return render_template('math_game.html',
                         num1=num1,
                         num2=num2,
                         op=op,
                         tries_left=session['math_tries'],
                         score=session['math_score'])

@app.route('/check-math', methods=['POST'])
def check_math():
    if 'player_name' not in session:
        return redirect(url_for('index'))
    
    try:
        guess = int(request.form.get('guess', ''))
    except ValueError:
        flash('Number lang dapat!', 'error')
        return redirect(url_for('math_game'))
    
    answer = session['math_answer']
    tries_left = session['math_tries']
    score = session['math_score']
    
    if guess == answer:
        session['math_score'] = score + 1
        flash('Tama!', 'success')
    else:
        session['math_tries'] = tries_left - 1
        flash(f'Mali! Ang sagot ay {answer}', 'error')
    
    if session['math_tries'] <= 0:
        player = session['player_name']
        global_scores['math_game'][player] = max(global_scores['math_game'][player], score)
        session.pop('math_tries')
        session.pop('math_score')
        return redirect(url_for('game_menu'))
    
    return redirect(url_for('math_game'))

@app.route('/delete-scores')
def delete_scores():
    if 'player_name' not in session:
        return redirect(url_for('index'))
    
    player = session['player_name']
    if player in global_players:
        for game in global_scores:
            global_scores[game][player] = 0
        flash('Scores deleted!', 'success')
    
    return redirect(url_for('game_menu'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)