tokens = (
    'NOMBRE', 'NUMERO',
    'SUMA', 'RESTA', 'MULTIPLICACION', 'DIVISION', 'IGUAL',
    'PARENTESIS_IZQ', 'PARENTESIS_DER',
)

# Tokens

t_SUMA    = r'\+'
t_RESTA   = r'-'
t_MULTIPLICACION   = r'\*'
t_DIVISION  = r'/'
t_IGUAL  = r'='
t_PARENTESIS_IZQ  = r'\('
t_PARENTESIS_DER  = r'\)'
t_NOMBRE    = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_NUMERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Valor entero demasiado grande %d", t.value)
        t.value = 0
    return t

# Caracteres ignorados
t_ignore = " \t"

def t_salto_de_linea(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Carácter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Construir el analizador léxico
import ply.lex as lex
lexer = lex.lex()

# Reglas de análisis sintáctico

precedence = (
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULTIPLICACION', 'DIVISION'),
    ('right', 'UMENOS'),
)

# Diccionario de nombres
nombres = { }

def p_sentencia_asignacion(t):
    'sentencia : NOMBRE IGUAL expresion'
    nombres[t[1]] = t[3]

def p_sentencia_expresion(t):
    'sentencia : expresion'
    print(t[1])

def p_expresion_binaria(t):
    '''expresion : expresion SUMA expresion
                  | expresion RESTA expresion
                  | expresion MULTIPLICACION expresion
                  | expresion DIVISION expresion'''
    if t[2] == '+': t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': t[0] = t[1] / t[3]

def p_expresion_umenos(t):
    'expresion : RESTA expresion %prec UMENOS'
    t[0] = -t[2]

def p_expresion_agrupacion(t):
    'expresion : PARENTESIS_IZQ expresion PARENTESIS_DER'
    t[0] = t[2]

def p_expresion_numero(t):
    'expresion : NUMERO'
    t[0] = t[1]

def p_expresion_nombre(t):
    'expresion : NOMBRE'
    try:
        t[0] = nombres[t[1]]
    except LookupError:
        print("Nombre no definido '%s'" % t[1])
        t[0] = 0

def p_error(t):
    print("Error de sintaxis en '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')   
    except EOFError:
        break
    parser.parse(s)
