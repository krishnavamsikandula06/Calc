from flask import Flask, request, jsonify
from calc.evaluator import evaluate

app = Flask(__name__, static_folder='static', static_url_path='/static')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/calc', methods=['POST'])
def calc_api():
    data = request.get_json() or {}
    expr = data.get('expr', '')
    try:
        result = evaluate(expr)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
