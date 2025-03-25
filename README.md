# Math Game with Python Keywords Demonstration

This project is a simple math game that demonstrates the use of various Python keywords in a practical application.

## Project Description
A web-based math game that:
- Generates random math problems
- Tracks score and remaining tries
- Provides immediate feedback
- Demonstrates all required Python keywords

## Python Keywords Used

1. **Control Flow Keywords**
   - `if`, `elif`, `else`: Used in problem generation and answer checking
   ```python
   if op == '*':
       num1 = random.randint(1, 10)
   elif op == '+':
       num1 = random.randint(1, 50)
   else:
       num1 = random.randint(10, 50)
   ```

   - `while`, `break`, `continue`: Used in game loop control
   ```python
   while True:
       if counter >= 3:
           break
       counter += 1
       continue
   ```

2. **Function and Class Keywords**
   - `def`, `class`, `return`: Used in game structure
   ```python
   class MathGame:
       def generate_problem(self) -> Dict:
           return {'num1': num1, 'num2': num2, 'op': op}
   ```

3. **Exception Handling Keywords**
   - `try`, `except`, `finally`, `raise`: Used in error management
   ```python
   try:
       assert isinstance(guess, int)
   except AssertionError:
       return False
   finally:
       pass
   ```

4. **Module and Import Keywords**
   - `from`, `import`, `as`: Used for importing required modules
   ```python
   from flask import Flask, render_template
   from typing import Generator, Dict, List
   ```

5. **Variable and Scope Keywords**
   - `global`, `nonlocal`: Used for scope management
   ```python
   global scores
   def update_score():
       nonlocal score
       score *= 2
   ```

6. **Context Management Keywords**
   - `with`: Used for file operations
   ```python
   with open('game_log.txt', 'a') as f:
       f.write('New game started\n')
   ```

7. **Generator Keywords**
   - `yield`: Used in message generation
   ```python
   def generate_messages():
       for msg in messages:
           yield msg
   ```

8. **Boolean Keywords**
   - `and`, `or`, `not`, `True`, `False`: Used in logical operations
   ```python
   if guess is None or not isinstance(guess, int):
       return False
   ```

9. **Other Keywords**
   - `assert`: Used for validation
   - `del`: Used for dictionary manipulation
   - `in`, `is`: Used for comparisons
   - `lambda`: Used for simple functions
   - `None`: Used for null values
   - `pass`: Used as placeholder

## How to Run
1. Install requirements: