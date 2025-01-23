import re

op = ['+', '-', '*', '/', '|', '=']
specialop = {'&': '&amp;', '<': '&lt;', '>': '&gt;'}
unaryOp = ['-', '~']
keywordConstant = ['true', 'false', 'null', 'this']

integerConstant = '^[0-9]+'
stringConstant = '^".*"'
identifier = '[a-zA-Z](\w)*'

def expression(e, space=1):
    termPattern = f"{integerConstant}$|{stringConstant}$|{'^' + identifier}$|^(-$|~)\w+$|^({'$|'.join(keywordConstant)})"
    termLongPattern = r"^{identifier}\[.*\]$|^{identifier}\(.*\)$|^{identifier}\.{identifier}\(.*\)$|^\(.*\)".format(identifier=identifier)

    result = '  '*(space-1) + '<expression>\n'
    
    start = 0
    end = 0
    for letter in e:
        if letter in op + unaryOp + list(specialop):
            if re.search(termLongPattern +'|'+ termPattern, e[start:end].strip()) and re.search(termLongPattern +'|'+ termPattern, e[end+1:].strip()):
                
                result += term(e[start:end].strip(), space+1)
                
                if letter in specialop:
                    result += '  '*space + f'<symbol> {specialop[letter]} </symbol>\n' 

                else:
                    result += '  '*space + f'<symbol> {letter} </symbol>\n'  
                
                start = end+1
        end += 1

    result += term(e[start:].strip(), space+1)

    result += '  '*(space-1) + '</expression>\n'
    return result
        
def term(t, space=1):
    result = '  '*(space-1) + '<term>\n'

    # integerConstant
    if re.search(integerConstant, t):
        result += '  '*space + f'<integerConstant> {t} </integerConstant>\n'
    
    # stringConstant
    elif re.search(stringConstant, t):
        result += '  '*space + f'<stringConstant> {t[1:-1]} </stringConstant>\n'

    # keywordConstant
    elif t in keywordConstant:
        result += '  '*space + f'<keyword> {t} </keyword>\n'

    # varName[expression]
    elif re.search('^' + identifier + r'\[', t):
        startlist = re.search(identifier + r'\[', t).end()
        tokins = [t.strip()[:startlist-1], t.strip()[startlist:-1]]

        result += '  '*space + f'<identifier> {tokins[0]} </identifier>\n'
        result += '  '*space + f'<symbol> [ </symbol>\n'
        result += expression(tokins[1], space+1)
        result += '  '*space + f'<symbol> ] </symbol>\n'

    # subroutineCall
        # subroutineName(expressionList)
    elif re.search('^' + identifier + r'\(', t):
        result += subroutineCall(t, space)
        # (className|varName).subroutineName(expressionList)
    elif re.search('^' + identifier + r'\.' + identifier + r'\(', t):
        result += subroutineCall(t, space)

    # (expression)
    elif re.search(r'^\(', t):
        result += '  '*space + f'<symbol> ( </symbol>\n'
        result += expression(t[1:-1], space+1)
        result += '  '*space + f'<symbol> ) </symbol>\n'
    
    # varName
    elif re.search('^' + identifier, t):
        result += '  '*space + f'<identifier> {t} </identifier>\n'

    # unaryOp term
    elif t.strip()[0] in unaryOp:
        result += '  '*space + f'<symbol> {t.strip()[0]} </symbol>\n'    
        result += term(t.strip()[1:], space+1)

    result+= '  '*(space-1) + '</term>\n'
    return result

def expressionList(elist, space=1):
    result = '  '*(space-1) + '<expressionList>\n'

    expressions = re.split('\s*,\s*', elist.strip())
    if expressions != ['']:
        for e in expressions[:-1]:
            result += expression(e, space+1)
            result += '  '*space + f'<symbol> , </symbol>\n'

        result += expression(expressions[-1], space+1)

    result+= '  '*(space-1) + '</expressionList>\n'
    return result

def subroutineCall(s, space=1):
    result = ''
    # subroutineName(expressionList)
    if re.search('^' + identifier + r'\(', s):
        startlist = re.search(identifier + r'\(', s).end()
        tokins = [s.strip()[:startlist-1], s.strip()[startlist:-1]]

        result += '  '*space + f'<identifier> {tokins[0]} </identifier>\n'
        result += '  '*space + f'<symbol> ( </symbol>\n'
        result += expressionList(tokins[1], space+1)
        result += '  '*space + f'<symbol> ) </symbol>\n'

    # (className|varName).subroutineName(expressionList)
    elif re.search('^' + identifier + r'\.' + identifier + r'\(', s):
        varName = s.split('.')[0]
        subName = s.split('.')[1].split('(')[0]
        expName = s[re.search(r'\(', s).end():]
        
        result += '  '*space + f'<identifier> {varName} </identifier>\n'
        result += '  '*space + '<symbol> . </symbol>\n'
        result += '  '*space + f'<identifier> {subName} </identifier>\n'
        result += '  '*space + f'<symbol> ( </symbol>\n'
        result += expressionList(expName[:-1], space+1)
        result += '  '*space + f'<symbol> ) </symbol>\n'

    return result

