#Martinez Benitez Dania Jazmin

import re

def is_valid_identifier(identifier):
    # Verificar que solo contenga letras, números y guion bajo
    pattern = r'^[a-zA-Z][a-zA-Z0-9_]*$'
    return bool(re.match(pattern, identifier))

def get_invalid_chars(identifier):
    # Obtener los caracteres inválidos en el identificador
    valid_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_')
    invalid_chars = [char for char in identifier if char not in valid_chars]
    return invalid_chars

def lexical_analysis(code):
    token_specs = [
        ('Número',        r'\d+'),
        ('Asignación',    r'='),
        ('Suma',          r'\bMAS\b'),
        ('Resta',         r'\bMENOS\b'),
        ('PuntoYComa',    r';'),
        ('ParéntesisIzq', r'\('),
        ('ParéntesisDer', r'\)'),
        ('TipoDato',      r'\b(?:Int|String)\b'),  
        ('Imprimir',      r'\bPRINT\b'),
        ('Texto',         r'(\".*?\"|\'.*?\')'),
        ('Identificador', r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('NuevaLinea',    r'\n'),
        ('Espacio',       r'[ \t]+'),
        ('Desconocido',   r'.'),  
    ]

    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specs)
    line_num = 1
    tokens = []
    errors = []

    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()

        if kind == 'NuevaLinea':
            line_num += 1
        elif kind == 'Espacio':
            continue
        elif kind == 'Desconocido':
            errors.append({
                'line': line_num, 
                'error': f"❌ Línea {line_num}: Caracter no reconocido '{value}'",
                'value': value
            })
        elif kind == 'Identificador':
            # Verificar palabras reservadas en minúsculas
            value_lower = value.lower()
            if value_lower in ['string', 'int']:
                errors.append({
                    'line': line_num,
                    'error': f"❌ Línea {line_num}: Error de sintaxis\n   Los tipos de datos deben escribirse en mayúscula\n   → Escribiste: '{value}'\n   → Debe ser: '{value.capitalize()}'",
                    'value': value
                })
            elif value_lower == 'print':
                errors.append({
                    'line': line_num,
                    'error': f"❌ Línea {line_num}: Error de sintaxis\n   La instrucción PRINT debe escribirse en mayúsculas\n   → Escribiste: '{value}'\n   → Debe ser: 'PRINT'",
                    'value': value
                })
            elif value_lower == 'mas':
                errors.append({
                    'line': line_num,
                    'error': f"❌ Línea {line_num}: Error de sintaxis\n   El operador MAS debe escribirse en mayúsculas\n   → Escribiste: '{value}'\n   → Debe ser: 'MAS'",
                    'value': value
                })
            elif value_lower == 'menos':
                errors.append({
                    'line': line_num,
                    'error': f"❌ Línea {line_num}: Error de sintaxis\n   El operador MENOS debe escribirse en mayúsculas\n   → Escribiste: '{value}'\n   → Debe ser: 'MENOS'",
                    'value': value
                })
            elif not is_valid_identifier(value):
                invalid_chars = get_invalid_chars(value)
                if invalid_chars:
                    chars_str = ', '.join([f"'{c}'" for c in invalid_chars])
                    errors.append({
                        'line': line_num,
                        'error': f"❌ Línea {line_num}: Nombre de variable inválido\n   El nombre '{value}' contiene caracteres no permitidos: {chars_str}\n   Solo se permiten letras, números y guion bajo (_)\n   El nombre debe comenzar con una letra",
                        'value': value
                    })
                else:
                    errors.append({
                        'line': line_num,
                        'error': f"❌ Línea {line_num}: Nombre de variable inválido\n   '{value}' debe comenzar con una letra\n   Solo se permiten letras, números y guion bajo (_)",
                        'value': value
                    })
            else:
                tokens.append({'type': kind, 'value': value, 'line': line_num})
        elif kind == 'Texto':
            value = value[1:-1]
            tokens.append({'type': kind, 'value': value, 'line': line_num})
        else:
            tokens.append({'type': kind, 'value': value, 'line': line_num})

    return tokens, errors
