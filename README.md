# Calc — Simple Python Calculator

This is a minimal Python calculator with a small frontend.

Quick start

1. Create a virtualenv and activate it:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python app.py
```

4. Open http://localhost:5000 in your browser.

Notes
- The server evaluates arithmetic expressions safely using Python's AST. Supported: `+ - * / ** %` and unary plus/minus and parentheses.
