from Expressions import *

keyword = ['let', 'do', 'if', 'else', 'while', 'return']

def statements(file, cursor, space=1):
    file.seek(cursor)
    line = file.readline()
       
    def endExpression(line, file, cursor):
        endExp = re.search(';',line)
        if endExp:
            line = line[:endExp.end()]
            file.seek(cursor + endExp.end())

        return line
        
    result = ''

    if re.search('^\s*let', line):
        line = endExpression(line, file, cursor)
        result += letStatement(line, space+1)

    elif re.search('^\s*if', line):
        # print(line) 
        result += ifStatement(file, cursor, space+1)

    elif re.search('^\s*while', line):
        result += whileStatement(file, cursor, space+1)

    elif re.search('^\s*do', line):
        line = endExpression(line, file, cursor)
        result += doStatement(line, space+1)

    elif re.search('^\s*return', line):
        line = endExpression(line, file, cursor)
        result += returnStatement(line, space+1)

    return result


def letStatement(s, space=1):
    s = s.strip()
    result = '  '*(space-1) + '<letStatement>\n'
    varName = re.search(identifier, s[3:])
    startExpression = re.search('=', s).end()

    result += '  '*space + f'<keyword> let </keyword>\n'
    result += '  '*space + f'<identifier> {varName.group()} </identifier>\n'

    if s[3 + varName.end()] == '[':
        result += '  '*space + f'<symbol> [ </symbol>\n'

        endlist = re.search(r'\]', s).start()
        result += expression(s[3 + varName.end()+1:endlist].strip(), space+1)
        result += '  '*space + f'<symbol> ] </symbol>\n'

    result += '  '*space + f'<symbol> = </symbol>\n'

    endExpression = re.search(';',s).start()
    result += expression(s[startExpression:endExpression].strip(), space+1)
    result += '  '*space + f'<symbol> ; </symbol>\n'

    result += '  '*(space-1) + '</letStatement>\n'
    return result

def ifStatement(file, cursor, space=1):
    file.seek(cursor)

    result = '  '*(space-1) + '<ifStatement>\n'
    result += '  '*space + '<keyword> if </keyword>\n'

    lineExpression = re.search(r'\(.*\)\s*\{', file.readline())
    endExpression = lineExpression.end()
    lineExpression = lineExpression.group()[:-1].strip()

    result += '  '*space + '<symbol> ( </symbol>\n'
    result += expression(lineExpression[1:-1].strip(), space+1)
    result += '  '*space + '<symbol> ) </symbol>\n'
    
    result += '  '*space + '<symbol> { </symbol>\n'
    cursor = cursor + endExpression
    result += '  '*(space) + '<statements>\n'

    while True:
        result += statements(file, cursor, space+1)
        cursor = file.tell()

        endif = re.search(r'^\s*\}', file.readline())
        if endif:
            cursor = cursor + endif.end()
            break

    result += '  '*(space) + '</statements>\n'
    result += '  '*space + '<symbol> } </symbol>\n'

    while True:
        line = file.readline()
        if re.search('^\s*(\n)?$', line) and cursor != file.tell():
             cursor = file.tell()
             continue
        else:break

    elsestatement = re.search('else', line)
    if elsestatement:
        cursor = cursor + elsestatement.end()
        file.seek(cursor)
        while True:
            line = file.readline()
            if re.search(r'\{', line):
                break
            else: cursor += 1
        cursor += 1

        result += '  '*space + '<keyword> else </keyword>\n'
        result += '  '*space + '<symbol> { </symbol>\n'

        result += '  '*(space) + '<statements>\n'
        while True:
            result += statements(file, cursor, space+1)
            cursor = file.tell()

            endif = re.search(r'\}', file.readline())
            if endif:
                cursor = file.tell()
                break
        result += '  '*(space) + '</statements>\n'
        result += '  '*space + '<symbol> } </symbol>\n'

    file.seek(cursor)
    result += '  '*(space-1) + '</ifStatement>\n'
    return result

def whileStatement(file, cursor, space=1):
    file.seek(cursor)

    result = '  '*(space-1) + '<whileStatement>\n'
    result += '  '*space + '<keyword> while </keyword>\n'

    lineExpression = re.search(r'\(.*\)\s*\{', file.readline())
    endExpression = lineExpression.end()
    lineExpression = lineExpression.group()[:-1].strip()
    
    result += '  '*space + '<symbol> ( </symbol>\n'
    result += expression(lineExpression[1:-1].strip(), space+1)
    result += '  '*space + '<symbol> ) </symbol>\n'
    
    result += '  '*space + '<symbol> { </symbol>\n'

    cursor = cursor + endExpression
    result += '  '*(space) + '<statements>\n'

    while True:
        result += statements(file, cursor, space+1)
        cursor = file.tell()
        
        endif = re.search(r'^\s*\}', file.readline())
        if endif:
            cursor = cursor + endif.end()
            break
    
    result += '  '*(space) + '</statements>\n'

    result += '  '*space + '<symbol> } </symbol>\n'
    result += '  '*(space-1) + '</whileStatement>\n'
    return result

def doStatement(s, space=1):
    s = s.strip()
    result = '  '*(space-1) + '<doStatement>\n'

    result += '  '*space + f'<keyword> do </keyword>\n'
    result += subroutineCall(s[2:-1].strip(), space)
    result += '  '*space + f'<symbol> ; </symbol>\n'

    result += '  '*(space-1) + '</doStatement>\n'
    return result

def returnStatement(s, space=1):
    s = s.strip()
    result = '  '*(space-1) + '<returnStatement>\n'

    result += '  '*space + f'<keyword> return </keyword>\n'
    
    if s[6:].strip() != ';':
        result += expression(s[6:-1].strip(), space+1)
    result += '  '*space + f'<symbol> ; </symbol>\n'

    result += '  '*(space-1) + '</returnStatement>\n'
    return result
