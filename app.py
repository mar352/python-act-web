from flask import Flask, render_template, request, redirect, url_for, session, flash
import random
import os
from typing import Generator, Dict, List

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Global variables demonstration
global scores
scores = {'math_game': {}}

class MathGame:
    """Class demonstration with multiple keywords"""
    def __init__(self) -> None:
        self.operations = ['+', '-', '*']
        self.max_tries = 5
    
    def generate_problem(self) -> Dict:
        """Generator method using multiple keywords"""
        try:
            op = random.choice(self.operations)
            
            # Demonstrate if, elif, else
            if op == '*':
                num1 = random.randint(1, 10)
                num2 = random.randint(1, 10)
            elif op == '+':
                num1 = random.randint(1, 50)
                num2 = random.randint(1, 50)
            else:
                num1 = random.randint(10, 50)
                num2 = random.randint(1, num1)  # Ensure positive result for subtraction
            
            return {'num1': num1, 'num2': num2, 'op': op}
        
        except Exception as e:
            raise ValueError("Error generating problem")
        finally:
            pass  # Demonstrate finally and pass

    def calculate_score(self, tries_left: int) -> int:
        """Lambda and basic math demonstration"""
        # Demonstrate lambda
        score_multiplier = lambda x: x * 2
        return score_multiplier(tries_left)

    @staticmethod
    def generate_messages() -> Generator[str, None, None]:
        """Demonstrate yield keyword"""
        messages = ["Great job!", "Keep going!", "Almost there!"]
        for msg in messages:
            yield msg

def process_answer(answer: int, guess: int) -> bool:
    """Demonstrate assert and boolean operations"""
    try:
        assert isinstance(guess, int), "Guess must be an integer"
        return True if answer == guess else False
    except AssertionError:
        return False

@app.route('/')
def index():
    # Demonstrate while and break
    counter = 0
    while True:
        if counter >= 3:
            break
        counter += 1
        continue  # Demonstrate continue
    return redirect(url_for('math_game'))

@app.route('/login', methods=['POST'])
def login():
    name = request.form.get('name')
    if not name:
        flash('Hindi pwedeng walang pangalan!', 'error')
        return redirect(url_for('index'))
    
    if name not in global_players:
        global_players.append(name)
        global_scores['math_game'][name] = 0
    
    session['player_name'] = name
    return redirect(url_for('game_menu'))

@app.route('/game-menu')
def game_menu():
    if 'player_name' not in session:
        return redirect(url_for('index'))
    
    return render_template('game_menu.html', 
                         scores=global_scores, 
                         player=session['player_name'])

@app.route('/math-game')
def math_game():
    # Demonstrate with statement
    with open('game_log.txt', 'a') as f:
        f.write('New game started\n')
    
    # Initialize game state
    if 'math_tries' not in session:
        session['math_tries'] = 5
        session['math_score'] = 0
    
    # Create game instance
    game = MathGame()
    problem = game.generate_problem()
    
    # Store problem in session
    session['math_problem'] = problem
    session['math_answer'] = eval(f"{problem['num1']} {problem['op']} {problem['num2']}")
    
    # Demonstrate del
    temp_dict = {'temp': 'value'}
    del temp_dict['temp']
    
    return render_template('math_game.html',
                         num1=problem['num1'],
                         num2=problem['num2'],
                         op=problem['op'],
                         tries_left=session['math_tries'],
                         score=session['math_score'])

@app.route('/check-math', methods=['POST'])
def check_math():
    # Demonstrate nonlocal in nested function
    def update_score():
        nonlocal score
        score *= 2
    
    try:
        guess = int(request.form.get('guess', ''))
    except ValueError:
        flash('Number lang dapat!', 'error')
        return redirect(url_for('math_game'))
    
    answer = session['math_answer']
    tries_left = session['math_tries']
    score = session['math_score']
    
    # Demonstrate or and and
    if guess is None or not isinstance(guess, int):
        return redirect(url_for('math_game'))
    
    if process_answer(answer, guess) and tries_left > 0:
        update_score()
        session['math_score'] = score
        flash('Tama!', 'success')
    else:
        session['math_tries'] = tries_left - 1
        flash(f'Mali! Ang sagot ay {answer}', 'error')
    
    if session['math_tries'] <= 0:
        flash(f'Game Over! Final Score: {score}', 'info')
        session.pop('math_tries', None)
        session.pop('math_score', None)
    
    return redirect(url_for('math_game'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)