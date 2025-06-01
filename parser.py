#Martinez Benitez Dania Jazmin

def syntactic_analysis(tokens):
    errors = []
    current_line = None
    current_tokens = []

    def analyze_statement(tokens_line, line_number):
        if not tokens_line:
            return

        first_type = tokens_line[0]['type']

        # Declaración variable
        if first_type == 'TipoDato':
            expected_format = "   Formato correcto: Int/String variable = valor;"
            expected_tokens = [
                ('TipoDato', 'tipo de dato (Int/String)'),
                ('Identificador', 'nombre de variable'),
                ('Asignación', 'símbolo ='),
                ('Número/Texto', 'valor'),
                ('PuntoYComa', 'símbolo ;')
            ]
            
            # Verificar si el tipo de dato está en minúsculas
            tipo_valor = tokens_line[0]['value']
            if tipo_valor in ['string', 'int']:
                return f"❌ Línea {line_number}: Error de sintaxis\n{expected_format}\n   Los tipos de datos deben comenzar con mayúscula\n   → Escribiste: '{tipo_valor}'\n   → Debe ser: '{tipo_valor.capitalize()}'"
            
            if len(tokens_line) < 5:
                missing = expected_tokens[len(tokens_line):]
                missing_str = '\n   → '.join(f"Falta {desc}" for _, desc in missing)
                return f"❌ Línea {line_number}: Declaración incompleta\n{expected_format}\n"
            elif len(tokens_line) > 5:
                return f"❌ Línea {line_number}: Tokens extra en la declaración\n{expected_format}"
            
            # Validar orden: TipoDato Identificador = (Número o Texto) ;
            if tokens_line[1]['type'] != 'Identificador':
                return f"❌ Línea {line_number}: Error de sintaxis\n{expected_format}\n   Se esperaba: nombre de variable\n   Se encontró: '{tokens_line[1]['value']}'"
            
            if tokens_line[2]['type'] != 'Asignación':
                return f"❌ Línea {line_number}: Error de sintaxis\n{expected_format}\n   Se esperaba: símbolo =\n   Se encontró: '{tokens_line[2]['value']}'"
            
            valor_tipo = tokens_line[3]['type']
            tipo_dato = tokens_line[0]['value']
            
            if tipo_dato == 'Int' and valor_tipo != 'Número':
                return f"❌ Línea {line_number}: Error de tipo\n{expected_format}\n   Variable '{tokens_line[1]['value']}' es de tipo Int\n   No se puede asignar: {valor_tipo} ('{tokens_line[3]['value']}')\n   → Int solo acepta números"
            
            if tipo_dato == 'String' and valor_tipo != 'Texto':
                return f"❌ Línea {line_number}: Error de tipo\n{expected_format}\n   Variable '{tokens_line[1]['value']}' es de tipo String\n   No se puede asignar: {valor_tipo} ('{tokens_line[3]['value']}')\n   → String solo acepta texto entre comillas"
            
            if tokens_line[4]['type'] != 'PuntoYComa':
                return f"❌ Línea {line_number}: Error de sintaxis\n{expected_format}\n   Falta punto y coma al final\n   Se encontró: '{tokens_line[4]['value']}'"

        # Imprimir
        elif first_type == 'Imprimir':
            expected_format = "   Formato correcto: PRINT(texto/variable);"
            
            if len(tokens_line) < 5:
                return f"❌ Línea {line_number}: Instrucción PRINT incompleta\n{expected_format}"
            elif len(tokens_line) > 5:
                return f"❌ Línea {line_number}: Tokens extra en PRINT\n{expected_format}"
            
            if tokens_line[1]['type'] != 'ParéntesisIzq':
                return f"❌ Línea {line_number}: Error de sintaxis en PRINT\n{expected_format}\n   Se esperaba: paréntesis (\n   Se encontró: '{tokens_line[1]['value']}'"
            
            if tokens_line[2]['type'] not in ['Identificador', 'Texto']:
                return f"❌ Línea {line_number}: Error en PRINT\n{expected_format}\n   Solo se puede imprimir texto o variables\n   No se permite: {tokens_line[2]['type']} ('{tokens_line[2]['value']}')"
            
            if tokens_line[3]['type'] != 'ParéntesisDer':
                return f"❌ Línea {line_number}: Error de sintaxis en PRINT\n{expected_format}\n   Se esperaba: paréntesis )\n   Se encontró: '{tokens_line[3]['value']}'"
            
            if tokens_line[4]['type'] != 'PuntoYComa':
                return f"❌ Línea {line_number}: Error de sintaxis en PRINT\n{expected_format}\n   Falta punto y coma al final\n   Se encontró: '{tokens_line[4]['value']}'"

        # Suma o Resta
        elif first_type == 'Identificador':
            expected_format = "   Formato correcto: variable = (número/variable) MAS/MENOS (número/variable);"
            
            if len(tokens_line) < 6:
                return f"❌ Línea {line_number}: Operación incompleta\n{expected_format}"
            elif len(tokens_line) > 6:
                return f"❌ Línea {line_number}: Tokens extra en la operación\n{expected_format}"
            
            if tokens_line[1]['type'] != 'Asignación':
                return f"❌ Línea {line_number}: Error de sintaxis\n{expected_format}\n   Se esperaba: símbolo =\n   Se encontró: '{tokens_line[1]['value']}'"
            
            # Validar primer operando (número o variable)
            if tokens_line[2]['type'] not in ['Número', 'Identificador']:
                return f"❌ Línea {line_number}: Error de tipo\n{expected_format}\n   Se esperaba: un número o variable\n   Se encontró: {tokens_line[2]['type']} ('{tokens_line[2]['value']}')"
            
            if tokens_line[3]['type'] not in ['Suma', 'Resta']:
                return f"❌ Línea {line_number}: Error de sintaxis\n{expected_format}\n   Se esperaba: operador MAS o MENOS\n   Se encontró: '{tokens_line[3]['value']}'"
            
            # Validar segundo operando (número o variable)
            if tokens_line[4]['type'] not in ['Número', 'Identificador']:
                return f"❌ Línea {line_number}: Error de tipo\n{expected_format}\n   Se esperaba: un número o variable\n   Se encontró: {tokens_line[4]['type']} ('{tokens_line[4]['value']}')"
            
            if tokens_line[5]['type'] != 'PuntoYComa':
                return f"❌ Línea {line_number}: Error de sintaxis\n{expected_format}\n   Falta punto y coma al final\n   Se encontró: '{tokens_line[5]['value']}'"

        else:
            return f"❌ Línea {line_number}: Instrucción no válida\n   Las instrucciones válidas son:\n   → Int/String variable = valor;\n   → PRINT(texto/variable);\n   → variable = número MAS/MENOS número;\n   Se encontró: {first_type} ('{tokens_line[0]['value']}')"

        return None  

    for token in tokens:
        if current_line is None:
            current_line = token['line']

        if token['line'] == current_line:
            current_tokens.append(token)
        else:
            err = analyze_statement(current_tokens, current_line)
            if err:
                errors.append({'line': current_line, 'error': err})
            current_tokens = [token]
            current_line = token['line']

    if current_tokens:
        err = analyze_statement(current_tokens, current_line)
        if err:
            errors.append({'line': current_line, 'error': err})

    result_msg = "✅ Análisis sintáctico completado sin errores." if not errors else "❌ Se encontraron errores sintácticos."

    return result_msg, errors
