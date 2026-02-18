from flask import Flask, render_template, request, jsonify
import math
import secrets
import string
from zxcvbn import zxcvbn

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    password = data.get('password', '')

    if not password:
        return jsonify({
            'entropy': 0,
            'crack_time': 'instantly',
            'score': 0,
            'feedback': [],
            'warning': ''
        })

    # Calculate entropy
    charset_size = 0
    if any(c.islower() for c in password):
        charset_size += 26
    if any(c.isupper() for c in password):
        charset_size += 26
    if any(c.isdigit() for c in password):
        charset_size += 10
    if any(c in string.punctuation for c in password):
        charset_size += 32

    if charset_size == 0:
        charset_size = 26

    entropy = len(password) * math.log2(charset_size)

    # Use zxcvbn for crack time and feedback
    result = zxcvbn(password)
    crack_time = result['crack_times_display']['offline_slow_hashing_1e4_per_second']
    score = result['score']
    suggestions = result['feedback']['suggestions']
    warning = result['feedback']['warning']

    return jsonify({
        'entropy': round(entropy, 1),
        'crack_time': crack_time,
        'score': score,
        'feedback': suggestions,
        'warning': warning
    })

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    length = max(8, min(32, data.get('length', 16)))
    use_upper = data.get('uppercase', True)
    use_lower = data.get('lowercase', True)
    use_numbers = data.get('numbers', True)
    use_special = data.get('special', True)

    charset = ''
    required_chars = []

    if use_upper:
        charset += string.ascii_uppercase
        required_chars.append(secrets.choice(string.ascii_uppercase))
    if use_lower:
        charset += string.ascii_lowercase
        required_chars.append(secrets.choice(string.ascii_lowercase))
    if use_numbers:
        charset += string.digits
        required_chars.append(secrets.choice(string.digits))
    if use_special:
        special_chars = '!@#$%^&*()_+-=[]{}|;:,.<>?'
        charset += special_chars
        required_chars.append(secrets.choice(special_chars))

    if not charset:
        charset = string.ascii_letters + string.digits
        required_chars = [secrets.choice(charset)]

    remaining_length = length - len(required_chars)
    password_chars = required_chars + [secrets.choice(charset) for _ in range(remaining_length)]

    # Shuffle to avoid predictable positions
    secrets.SystemRandom().shuffle(password_chars)
    password = ''.join(password_chars)

    return jsonify({'password': password})

if __name__ == '__main__':
    app.run(debug=True)
