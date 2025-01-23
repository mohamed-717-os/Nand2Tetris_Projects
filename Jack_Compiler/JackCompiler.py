keyword = [
        'class', 'constructor', 'function', 'method', 'field', 'static', 'var',
        'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this',
        'let', 'do', 'if', 'else', 'while', 'return'
]

symbol = [
        '{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/',
        '&', '|', '<', '>', '=', '~'
]

integerConstant = '[0-9]+'
stringConstant = '".*"'
identifier = '[a-zA-Z](\w)*'

import re
import programStructure 
filename = r'test.jack'
jackfile = open(filename)
xmlfile = open(r'test.xml', 'w')

cursor = jackfile.tell()

while True:
    line = jackfile.readline()

    if cursor == jackfile.tell():
        break

    # comments
    comments = re.search('//',line)
    if comments:
        line = line[:comments.start()]

    # multiline comment
    comment = re.search(r'/\*\*', line)
    if comment:
        jackfile.seek(cursor + comment.start())
        while True:
            line = jackfile.readline()
            commentEnd = re.search(r'\*/', line)
            if commentEnd:
                cursor = cursor + commentEnd.end()
                jackfile.seek(cursor)
                break
        continue

    # new lines
    new_lines = re.search('^\s*(\n)?$', line)
    if new_lines:
        cursor = jackfile.tell()
        continue


    if re.search('^class',line):
        line = programStructure.classCombile(jackfile, cursor)
    
        xmlfile.write(line)
        
    cursor = jackfile.tell()

