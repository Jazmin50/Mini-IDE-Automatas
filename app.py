#Martinez Benitez Dania Jazmin

from flask import Flask, render_template, request, jsonify
from lexer import lexical_analysis
from parser import syntactic_analysis
from turing_machine import simulate_turing_machine

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    code = data['code']
    mode = data.get('mode')  

    result = {
        'tokens': [],
        'lex_errors': [],
        'parse_result': '',
        'parse_errors': [],
        'tm_result': ''
    }

    # Análisis léxico
    if mode == 'lexico':
        result['tokens'], result['lex_errors'] = lexical_analysis(code)

    # Análisis sintáctico
    elif mode == 'sintactico':
        tokens, lex_errors = lexical_analysis(code)
        if lex_errors:
            result['parse_result'] = '❌ Error léxico: no se puede realizar análisis sintáctico.'
            result['lex_errors'] = lex_errors
        else:
            result['parse_result'], result['parse_errors'] = syntactic_analysis(tokens)

    # Máquina de Turing
    elif mode == 'turing':
        cadena = code.strip().replace('\n', '').replace(' ', '')
        if not cadena:
            result['tm_result'] = "❌ Error: La cadena no puede estar vacía. Por favor, ingrese una cadena de 0s y 1s."
        else:
            result['tm_result'] = simulate_turing_machine(cadena)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
