<div align="center">


# 🔐 Password Security Assessment & Resilience Analyzer

**A sleek, dark-themed web app for analyzing, scoring, and generating secure passwords — built with Flask + vanilla JS.**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![zxcvbn](https://img.shields.io/badge/zxcvbn-powered-blueviolet?style=flat-square)](https://github.com/dwolfhub/zxcvbn-python)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)

</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔴 **Live Strength Meter** | Animated gradient bar — red → yellow → cyan/purple glow |
| ✅ **Security Checklist** | 7 real-time criteria checked as you type |
| 📐 **Entropy Calculator** | Backend-computed bits via charset × length formula |
| ⏱️ **Brute-Force Estimate** | Crack time via zxcvbn offline slow hash model |
| 💡 **Smart Suggestions** | Personalized improvement tips from zxcvbn feedback |
| ⚡ **Password Generator** | Cryptographically secure via Python `secrets` module |
| 📖 **Learn Section** | Expandable accordion with password security education |
| 🌟 **Cursor Glow Effect** | Ambient cyan glow that follows your mouse pointer |

---

## 🗂️ Project Structure

```
password-app/
│
├── app.py                  ← Flask backend (routes, logic)
│
├── templates/
│   └── index.html          ← Single-page frontend (HTML + JS)
│
└── static/
    └── style.css           ← Dark glass UI styles
```

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- **Python 3.8+** — [python.org](https://python.org)
- **pip** — comes with Python
- **Git Bash** (Windows) or any terminal

---

### 1 · Clone or Download

```bash
# If using Git
git clone https://github.com/yourname/password-app.git
cd password-app

# Or just navigate to your project folder
cd path/to/password-app
```

---

### 2 · Create a Virtual Environment

```bash
# Create the environment
python -m venv venv

# Activate it
source venv/Scripts/activate      # Git Bash on Windows
# source venv/bin/activate        # macOS / Linux
```

You should see `(venv)` appear in your terminal prompt.

---

### 3 · Install Dependencies

```bash
pip install flask zxcvbn
```

That's it — only two packages needed.

---

### 4 · Run the App

```bash
python app.py
```

Open your browser and go to:

```
http://127.0.0.1:5000
```

---

## 🔌 API Endpoints

The Flask backend exposes three routes:

### `GET /`
Serves the main HTML page.

---

### `POST /analyze`
Analyzes a password and returns security metrics.

**Request body:**
```json
{ "password": "myPassword123!" }
```

**Response:**
```json
{
  "entropy": 52.4,
  "crack_time": "3 hours",
  "score": 2,
  "feedback": ["Add another word or two.", "Avoid repeated words and characters."],
  "warning": "This is similar to a commonly used password."
}
```

| Field | Type | Description |
|---|---|---|
| `entropy` | `float` | Bits of entropy (charset size × log₂ formula) |
| `crack_time` | `string` | Human-readable crack estimate (offline slow hash) |
| `score` | `int` | zxcvbn score 0–4 (0 = very weak, 4 = very strong) |
| `feedback` | `array` | Actionable improvement suggestions |
| `warning` | `string` | zxcvbn pattern warning (empty string if none) |

---

### `POST /generate`
Generates a cryptographically secure random password.

**Request body:**
```json
{
  "length": 16,
  "uppercase": true,
  "lowercase": true,
  "numbers": true,
  "special": true
}
```

**Response:**
```json
{ "password": "Xk#9mP!vLq2@Yw7n" }
```

> The generator guarantees at least **one character from each enabled character set**, then fills remaining length randomly. Uses Python's `secrets` module — safe for cryptographic use.

---

## 🧠 How It Works

### Strength Scoring (Frontend)
The strength meter updates **instantly** in the browser using a point-based heuristic:

```
+1  length ≥ 8
+1  length ≥ 12
+1  length ≥ 16
+1  has uppercase
+1  has lowercase
+1  has numbers
+1  has special characters
```

Score is mapped to: `Weak → Fair → Good → Strong`

### Entropy (Backend)
Entropy is calculated server-side using the standard formula:

```
charset_size = (26 if lowercase) + (26 if uppercase) + (10 if digits) + (32 if special)
entropy = len(password) × log₂(charset_size)
```

Aim for **60+ bits** for strong security.

### Crack Time (Backend)
Uses [zxcvbn](https://github.com/dwolfhub/zxcvbn-python) with the `offline_slow_hashing_1e4_per_second` model — simulating a motivated attacker with a GPU running 10,000 hashes/second against a bcrypt/scrypt-protected hash.

---

## 🎨 UI Highlights

- **Font stack** — `Syne` (display) + `Space Mono` (monospace) from Google Fonts
- **Background** — Deep navy `#040810` with layered radial gradient mesh
- **Cards** — `rgba` glass with `backdrop-filter: blur(24px)` and subtle top-edge shimmer
- **Strength bar** — CSS transitions with `cubic-bezier` easing; glows cyan/purple at full strength
- **Toggle switches** — Pure CSS animated switches (no JS required)
- **Cursor glow** — A soft `radial-gradient` aura follows the mouse via `mousemove` listener, centered on your real OS pointer
- **Accordion** — Native HTML `<details>` + CSS arrow rotation for zero-JS expand/collapse

---

## 🛠️ Customization

### Change the glow color
In `style.css`, find `#mouseGlow::after` and update the `rgba` values:

```css
/* Default: cyan */
rgba(0, 229, 255, 0.20)

/* Purple alternative */
rgba(168, 85, 247, 0.20)

/* Green alternative */
rgba(34, 197, 94, 0.20)
```

### Adjust generator password length limits
In `app.py`, find the `/generate` route:

```python
length = max(8, min(32, data.get('length', 16)))
#              ↑ max length — change 32 to whatever you want
```

### Add more common password detection
`zxcvbn` already handles common dictionaries, but you can extend the `setCriterion('c-common', ...)` logic in `index.html` with your own wordlist check.

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `flask` | 2.x+ | Web framework & routing |
| `zxcvbn` | 4.4.28+ | Password strength analysis & crack time |
| `secrets` | stdlib | Cryptographically secure random generation |
| `math` | stdlib | Entropy calculation |
| `string` | stdlib | Character set definitions |

Install all at once:
```bash
pip install flask zxcvbn
```

---

## 🔒 Security Notes

> **Your password never leaves your device for strength scoring.**  
> The frontend JavaScript scores the strength bar in real-time locally.  
> The backend `/analyze` call is only made for entropy and crack time — and in a local dev setup, this never leaves `localhost`.

- No passwords are logged or stored
- No database required
- The generator uses `secrets.SystemRandom()` — not `random`
- For production deployment, add HTTPS and consider rate-limiting `/analyze` and `/generate`

---

## 🐛 Troubleshooting

**`ModuleNotFoundError: No module named 'zxcvbn'`**  
Make sure your virtual environment is activated: `source venv/Scripts/activate`

**Port 5000 already in use**  
Run on a different port:
```bash
python app.py --port 5001
# or edit app.py:
app.run(debug=True, port=5001)
```

**Fonts not loading**  
The app loads fonts from Google Fonts — you need an internet connection on first load. Fonts are cached by the browser after that.

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<div align="center">

Built with 🔐 and way too much attention to `box-shadow` layering.

</div>
