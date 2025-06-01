#Martinez Benitez Dania Jazmin

def simulate_turing_machine(input_string):
    # Verificar que la cadena no esté vacía
    if not input_string:
        return "❌ Cadena rechazada: la cadena está vacía."
    
    # Verificar que la cadena solo contenga 0s y 1s
    if not all(c in ['0', '1'] for c in input_string):
        return "❌ Cadena rechazada: la cadena solo puede contener 0s y 1s."
    
    # Verificar que la cadena inicie con 1
    if input_string[0] != '1':
        return "❌ Cadena rechazada: la cadena debe iniciar con 1."

    # Contar 0s y 1s
    count_0 = input_string.count('0')
    count_1 = input_string.count('1')

    # Verificar que haya pares de 0s y 1s
    if count_0 % 2 == 0 and count_1 % 2 == 0:
        return f"✅ Cadena aceptada: hay {count_0} ceros y {count_1} unos (ambos son pares) y la cadena inicia con 1."
    else:
        return f"❌ Cadena rechazada: hay {count_0} ceros y {count_1} unos (deben ser pares) y la cadena debe iniciar con 1."
